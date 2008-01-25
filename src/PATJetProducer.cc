//
// $Id: PATJetProducer.cc,v 1.6 2008/01/23 16:45:36 lowette Exp $
//

#include "PhysicsTools/PatAlgos/interface/PATJetProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfoFwd.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfoFwd.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfoFwd.h"
#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "PhysicsTools/Utilities/interface/DeltaR.h"

#include "PhysicsTools/PatUtils/interface/ObjectResolutionCalc.h"

#include <vector>
#include <memory>


using namespace pat;


PATJetProducer::PATJetProducer(const edm::ParameterSet& iConfig) {
  // initialize the configurables
  jetsSrc_                 = iConfig.getParameter<edm::InputTag>            ( "jetSource" );
  getJetMCFlavour_         = iConfig.getParameter<bool>                     ( "getJetMCFlavour" );
  jetPartonMapSource_      = iConfig.getParameter<edm::InputTag>            ( "JetPartonMapSource" );
  addGenPartonMatch_       = iConfig.getParameter<bool>                     ( "addGenPartonMatch" );
  genPartonSrc_            = iConfig.getParameter<edm::InputTag>            ( "genPartonSource" );
  addGenJetMatch_          = iConfig.getParameter<bool>                     ( "addGenJetMatch" );
  genJetSrc_               = iConfig.getParameter<edm::InputTag>            ( "genJetSource" );
  addPartonJetMatch_       = iConfig.getParameter<bool>                     ( "addPartonJetMatch" );
  partonJetSrc_            = iConfig.getParameter<edm::InputTag>            ( "partonJetSource" );
  addResolutions_          = iConfig.getParameter<bool>                     ( "addResolutions" );
  useNNReso_               = iConfig.getParameter<bool>                     ( "useNNResolutions" );
  caliJetResoFile_         = iConfig.getParameter<std::string>              ( "caliJetResoFile" );
  caliBJetResoFile_        = iConfig.getParameter<std::string>              ( "caliBJetResoFile" );
  addBTagInfo_             = iConfig.getParameter<bool>                     ( "addBTagInfo" );
  addDiscriminators_       = iConfig.getParameter<bool>                     ( "addDiscriminators" );
  addJetTagRefs_           = iConfig.getParameter<bool>                     ( "addJetTagRefs" );
  tagModuleLabelsToKeep_   = iConfig.getParameter<std::vector<std::string> >( "tagModuleLabelsToKeep" );
  addAssociatedTracks_     = iConfig.getParameter<bool>                     ( "addAssociatedTracks" ); 
  trackAssociationPSet_    = iConfig.getParameter<edm::ParameterSet>        ( "trackAssociation" );
  addJetCharge_            = iConfig.getParameter<bool>                     ( "addJetCharge" ); 
  jetChargePSet_           = iConfig.getParameter<edm::ParameterSet>        ( "jetCharge" );

   
  // construct resolution calculator
  if (addResolutions_) {
    theResoCalc_ = new ObjectResolutionCalc(edm::FileInPath(caliJetResoFile_).fullPath(), useNNReso_);
    theBResoCalc_ = new ObjectResolutionCalc(edm::FileInPath(caliBJetResoFile_).fullPath(), useNNReso_);
  }

  // construct Jet Track Associator
  simpleJetTrackAssociator_ = ::helper::SimpleJetTrackAssociator(trackAssociationPSet_);
  // construct Jet Charge Computer
  if (addJetCharge_) jetCharge_ = new JetCharge(jetChargePSet_);
 
  // produces vector of jets
  produces<std::vector<Jet> >();
}


PATJetProducer::~PATJetProducer() {
  if (addResolutions_) {
    delete theResoCalc_;
    delete theBResoCalc_;
  }
  if (addJetCharge_) delete jetCharge_;
}


void PATJetProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // Get the vector of jets
  edm::Handle<edm::View<JetType> > jets;
  iEvent.getByLabel(jetsSrc_, jets);

  // for jet flavour
  edm::Handle<reco::CandMatchMap> JetPartonMap;
  if (getJetMCFlavour_) iEvent.getByLabel (jetPartonMapSource_, JetPartonMap);

  // Get the vector of generated particles from the event if needed
  edm::Handle<edm::View<reco::Candidate> > particles;
  if (addGenPartonMatch_) iEvent.getByLabel(genPartonSrc_, particles);
  // Get the vector of GenJets from the event if needed
  edm::Handle<edm::View<reco::GenJet> > genJets;
  if (addGenJetMatch_) iEvent.getByLabel(genJetSrc_, genJets);
/* TO BE IMPLEMENTED FOR >= 1_5_X
  // Get the vector of PartonJets from the event if needed
  edm::Handle<edm::View<reco::SomePartonJetType> > partonJets;
  if (addPartonJetMatch_) iEvent.getByLabel(partonJetSrc_, partonJets);
*/

  // Get the vector of jet tags with b-tagging info
  std::vector<edm::Handle<std::vector<reco::JetTag> > > jetTags_testManyByType ;
  iEvent.getManyByType(jetTags_testManyByType);
  // Define the handles for the specific algorithms
  edm::Handle<reco::SoftLeptonTagInfoCollection> jetsInfoHandle_sl;
  edm::Handle<reco::TrackProbabilityTagInfoCollection> jetsInfoHandleTP;
  edm::Handle<reco::TrackCountingTagInfoCollection> jetsInfoHandleTC;

  // tracks Jet Track Association, by hand in CMSSW_1_3_X
  edm::Handle<reco::TrackCollection> hTracks;
  iEvent.getByLabel(trackAssociationPSet_.getParameter<edm::InputTag>("tracksSource"), hTracks);


  // loop over jets
  std::vector<Jet> * patJets = new std::vector<Jet>(); 
  for (edm::View<JetType>::const_iterator itJet = jets->begin(); itJet != jets->end(); itJet++) {

    // define the jet correctors
    const JetCorrector * defaultJetCorr = JetCorrector::getJetCorrector("MCJetCorrectorIcone5", iSetup);
    const JetCorrector * udsJetCorr     = JetCorrector::getJetCorrector("L5FlavorJetCorrectorUds", iSetup);
    const JetCorrector * gluJetCorr     = JetCorrector::getJetCorrector("L5FlavorJetCorrectorGluon", iSetup);
    const JetCorrector * cJetCorr       = JetCorrector::getJetCorrector("L5FlavorJetCorrectorC", iSetup);
    const JetCorrector * bJetCorr       = JetCorrector::getJetCorrector("L5FlavorJetCorrectorB", iSetup);
    // calculate the energy correction factors
    float scaleDefault = defaultJetCorr->correction(*itJet);
    float scaleUds     = scaleDefault * udsJetCorr->correction(*itJet);
    float scaleGlu     = scaleDefault * gluJetCorr->correction(*itJet);
    float scaleC       = scaleDefault * cJetCorr->correction(*itJet);
    float scaleB       = scaleDefault * bJetCorr->correction(*itJet);

    // construct the Jet from the ref -> save ref to original object
    unsigned int idx = itJet - jets->begin();
    edm::Ref<std::vector<JetType> > jetsRef = jets->refAt(idx).castTo<edm::Ref<std::vector<JetType> > >();
    Jet ajet(jetsRef);
    ajet.setP4(scaleDefault * itJet->p4());
    ajet.setScaleCalibFactors(1./scaleDefault, scaleUds, scaleGlu, scaleC, scaleB);

    // get the MC flavour information for this jet
    if (getJetMCFlavour_) {
      for (reco::CandMatchMap::const_iterator f = JetPartonMap->begin(); f != JetPartonMap->end(); f++) {
        const reco::Candidate * jetClone = f->key->masterClone().get();
        // if (jetClone == &(*itJet) { // comparison by address doesn't work
        if (fabs(jetClone->eta() - itJet->eta()) < 0.001 &&
            fabs(jetClone->phi() - itJet->phi()) < 0.001) {
          ajet.setPartonFlavour(f->val->pdgId());
        }
      }
    }
    // do the parton matching
    if (addGenPartonMatch_) {
      // initialize best match as null
      reco::GenParticleCandidate bestParton(0, reco::Particle::LorentzVector(0, 0, 0, 0), reco::Particle::Point(0,0,0), 0, 0, true);
      float bestDR = 0;
      // find the closest parton
      for (edm::View<reco::Candidate>::const_iterator itParton = particles->begin(); itParton != particles->end(); ++itParton) {
        reco::GenParticleCandidate aParton = *(dynamic_cast<reco::GenParticleCandidate *>(const_cast<reco::Candidate *>(&*itParton)));
        if (aParton.status()==3 &&
            (abs(aParton.pdgId())==1 || abs(aParton.pdgId())==2 ||
             abs(aParton.pdgId())==3 || abs(aParton.pdgId())==4 ||
             abs(aParton.pdgId())==5 || abs(aParton.pdgId())==21)) {
          float currDR = DeltaR<reco::Candidate>()(aParton, ajet);
          // matching with hard-cut at 0.4
          // can be improved a la muon-electron, such that each parton
          // maximally matches 1 jet, but this requires two loops
          if (bestDR == 0 || (currDR < bestDR || currDR < 0.4)) {
            bestParton = aParton;
            bestDR = currDR;
          }
        }
      }
      ajet.setGenParton(bestParton);
    }
    // do the GenJet matching
    if (addGenJetMatch_) {
      // initialize best match as null
//NEED TO INITIALIZE TO ZERO
      reco::GenJet bestGenJet;//0, reco::Particle::LorentzVector(0, 0, 0, 0), reco::Particle::Point(0,0,0), 0, 0);
      float bestDR = 0;
      // find the closest parton
      for (edm::View<reco::GenJet>::const_iterator itGenJet = genJets->begin(); itGenJet != genJets->end(); ++itGenJet) {
// do we need some criteria?      if (itGenJet->status()==3) {
          float currDR = DeltaR<reco::Candidate>()(*itGenJet, ajet);
          // matching with hard-cut at 0.4
          // can be improved a la muon-electron, such that each genjet
          // maximally matches 1 jet, but this requires two loops
          if (bestDR == 0 || (currDR < bestDR || currDR < 0.4)) {
            bestGenJet = *itGenJet;
            bestDR = currDR;
          }
//          }
      }
      ajet.setGenJet(bestGenJet);
    }
    // TO BE IMPLEMENTED FOR >=1_5_X: do the PartonJet matching
    if (addPartonJetMatch_) {
    }

    // add resolution info if demanded
    if (addResolutions_) {
      (*theResoCalc_)(ajet);
      Jet abjet(ajet.bCorrJet());
      (*theBResoCalc_)(abjet);
      ajet.setBResolutions(abjet.resolutionET(), abjet.resolutionEta(), abjet.resolutionPhi(), abjet.resolutionA(), abjet.resolutionB(), abjet.resolutionC(), abjet.resolutionD(), abjet.resolutionTheta());
    }

    // add b-tag info if available & required
    if (addBTagInfo_) {
      for (size_t k=0; k<jetTags_testManyByType.size(); k++) {
        edm::Handle<std::vector<reco::JetTag> > jetTags = jetTags_testManyByType[k];

        //get label and module names
        std::string moduleLabel = (jetTags).provenance()->moduleLabel();

        //look only at the tagger present in tagModuleLabelsToKeep_
        for (unsigned int i = 0; i < tagModuleLabelsToKeep_.size(); ++i) {
          if (moduleLabel == tagModuleLabelsToKeep_[i]) {
            for (size_t t = 0; t < jetTags->size(); t++) {
              edm::RefToBase<reco::Jet> jet_p = (*jetTags)[t].jet();
              if (jet_p.isNull()) {
                /*std::cout << "-----------> JetTag::jet() returned null reference" << std::endl; */
                continue;
              }
              if (DeltaR<reco::Candidate>()(*itJet, *jet_p) < 0.00001) {
                //********store discriminators*********
                if (addDiscriminators_) {
                  std::pair<std::string, float> pairDiscri;
                  pairDiscri.first = moduleLabel;
                  pairDiscri.second = (*jetTags)[t].discriminator();
                  ajet.addBDiscriminatorPair(pairDiscri);
                  continue;
                }
              }
              //********store jetTagRef*********
              if (addJetTagRefs_) {
                std::pair<std::string, reco::JetTagRef> pairjettagref;
                pairjettagref.first = moduleLabel;
                pairjettagref.second = reco::JetTagRef(jetTags, t);
                ajet.addBJetTagRefPair(pairjettagref);
              }
            }
          }
        }
      }
    }

    // Associate tracks with jet (at least temporary)
    simpleJetTrackAssociator_.associate(ajet.momentum(), hTracks, ajet.associatedTracks_);

    // PUT HERE EVERYTHING WHICH NEEDS TRACKS
    if (addJetCharge_) {
      ajet.setJetCharge(static_cast<float>(jetCharge_->charge(ajet.p4(), ajet.associatedTracks())));
    }

    // drop jet track association if the user does not want it
    if (!addAssociatedTracks_) ajet.associatedTracks_.clear();

    patJets->push_back(ajet);
  }

  // sort jets in ET
  std::sort(patJets->begin(), patJets->end(), eTComparator_);

  // put genEvt  in Event
  std::auto_ptr<std::vector<Jet> > myJets(patJets);
  iEvent.put(myJets);

}

