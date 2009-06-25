//
// $Id: PATPFParticleProducer.h,v 1.5 2009/03/26 20:44:37 vadler Exp $
//

#ifndef PhysicsTools_PatAlgos_PATPFParticleProducer_h
#define PhysicsTools_PatAlgos_PATPFParticleProducer_h

/**
  \class    pat::PATPFParticleProducer PATPFParticleProducer.h "PhysicsTools/PatAlgos/interface/PATPFParticleProducer.h"
  \brief    Produces pat::PFParticle's

   The PATPFParticleProducer produces analysis-level pat::PFParticle's starting from
   a collection of objects of reco::PFCandidate.

  \author   Steven Lowette, Roger Wolf
  \version  $Id: PATPFParticleProducer.h,v 1.5 2009/03/26 20:44:37 vadler Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"

#include "CommonTools/Utils/interface/PtComparator.h"

#include "DataFormats/PatCandidates/interface/PFParticle.h"

#include "PhysicsTools/PatAlgos/interface/MultiIsolator.h"
#include "PhysicsTools/PatAlgos/interface/EfficiencyLoader.h"
#include "PhysicsTools/PatAlgos/interface/KinResolutionsLoader.h"

#include <string>


namespace pat {

  class LeptonLRCalc;

  class PATPFParticleProducer : public edm::EDProducer {

    public:

      explicit PATPFParticleProducer(const edm::ParameterSet & iConfig);
      ~PATPFParticleProducer();

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

    private:
      void 
	fetchCandidateCollection(edm::Handle< edm::View<reco::PFCandidate> >& c, 
				 const edm::InputTag& tag, 
				 const edm::Event& iSetup) const;

      // configurables
      edm::InputTag pfCandidateSrc_;
      bool          embedPFCandidate_;
      bool          addGenMatch_;
      bool          embedGenMatch_;
      std::vector<edm::InputTag> genMatchSrc_;
      // tools
      GreaterByPt<PFParticle>      pTComparator_;

      bool addEfficiencies_;
      pat::helper::EfficiencyLoader efficiencyLoader_;
      
      bool addResolutions_;
      pat::helper::KinResolutionsLoader resolutionLoader_;

 
  };


}

#endif
