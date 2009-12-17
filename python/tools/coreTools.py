import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import *

def restrictInputToAOD(process,
                   names=['All']
                   ):
    """
    ------------------------------------------------------------------
    remove pat object production steps which rely on RECO event
    content:

    process : process
    name    : list of collection names; supported are 'Photons', 
              'Electrons',, 'Muons', 'Taus', 'Jets', 'METs', 'All'
    ------------------------------------------------------------------    
    """
    for obj in range(len(names)):
        print "---------------------------------------------------------------------"
        print "WARNING: the following additional information can only be used on "
        print "         RECO format:"
        if( names[obj] == 'Photons' or names[obj] == 'All' ):
            print "          * nothing needs to be done for Photons"
        if( names[obj] == 'Electrons' or names[obj] == 'All' ):
            print "          * nothing needs to be done for Electrons"            
        if( names[obj] == 'Muons' or names[obj] == 'All' ):
            print "          * nothing needs to be done for Muons"            
        if( names[obj] == 'Taus' or names[obj] == 'All' ):
            print "          * nothing needs to be done for Taus"            
        if( names[obj] == 'Jets' or names[obj] == 'All' ):
            print "          * nothing needs to be done for Jets"            
        if( names[obj] == 'METs' or names[obj] == 'All' ):
            print "          * nothing needs to be done for METs"            
    print "---------------------------------------------------------------------"
    

def removeMCMatching(process,
                     name
                     ):
    """
    ------------------------------------------------------------------
    remove monte carlo matching from a given collection or all PAT
    candidate collections:

    process : process
    name    : collection name; supported are 'Photons', 'Electrons',
              'Muons', 'Taus', 'Jets', 'METs', 'All'
    ------------------------------------------------------------------    
    """
    if( name == 'Photons'   or name == 'All' ):
        _removeMCMatchingForPATObject(process, 'photonMatch', 'patPhotons') 
    if( name == 'Electrons' or name == 'All' ):
        _removeMCMatchingForPATObject(process, 'electronMatch', 'patElectrons') 
    if( name == 'Muons'     or name == 'All' ):
        _removeMCMatchingForPATObject(process, 'muonMatch', 'patMuons') 
    if( name == 'Taus'      or name == 'All' ):
        _removeMCMatchingForPATObject(process, 'tauMatch', 'patTaus')
        ## remove mc extra modules for taus
        process.patDefaultSequence.remove(process.tauGenJets)
        process.patDefaultSequence.remove(process.tauGenJetMatch)
        ## remove mc extra configs for taus
        tauProducer = getattr(process, 'patTaus')
        tauProducer.addGenJetMatch      = False
        tauProducer.embedGenJetMatch    = False
        tauProducer.genJetMatch         = ''         
    if( name == 'Jets'      or name == 'All' ):
        ## remove mc extra modules for jets
        process.patDefaultSequence.remove(process.jetPartonMatch)
        process.patDefaultSequence.remove(process.jetGenJetMatch)
        process.patDefaultSequence.remove(process.jetFlavourId)
        ## remove mc extra configs for jets
        jetProducer = getattr(process, jetCollectionString())
        jetProducer.addGenPartonMatch   = False
        jetProducer.embedGenPartonMatch = False
        jetProducer.genPartonMatch      = ''
        jetProducer.addGenJetMatch      = False
        jetProducer.genJetMatch         = ''
        jetProducer.getJetMCFlavour     = False
        jetProducer.JetPartonMapSource  = ''       
    if( name == 'METs'      or name == 'All' ):
        ## remove mc extra configs for jets
        metProducer = getattr(process, 'patMETs')        
        metProducer.addGenMET           = False
        metProducer.genMETSource        = ''       
    if( name == 'PFElectrons' or name == 'PFAll' ):
        _removeMCMatchingForPATObject(process, 'electronMatch', 'pfLayer1Electrons') 
    if( name == 'PFMuons'     or name == 'PFAll' ):
        _removeMCMatchingForPATObject(process, 'pfMuonMatch', 'pfLayer1Muons') 
    if( name == 'PFTaus'      or name == 'PFAll' ):
        _removeMCMatchingForPATObject(process, 'pfTauMatch', 'pfLayer1Taus')
        process.PFPATafterPAT.remove(process.pfTauGenJetMatch)
        ## remove mc extra configs for taus
        tauProducer = getattr(process, 'pfLayer1Taus')
        tauProducer.addGenJetMatch      = False
        tauProducer.embedGenJetMatch    = False
        tauProducer.genJetMatch         = ''         
    if( name == 'PFJets'      or name == 'PFAll' ):
        ## remove mc extra modules for jets
        process.PFPATafterPAT.remove(process.pfJetPartonMatch)
        process.PFPATafterPAT.remove(process.pfJetGenJetMatch)
        process.PFPATafterPAT.remove(process.pfJetPartonAssociation)
        process.PFPATafterPAT.remove(process.pfJetFlavourAssociation)     
        ## remove mc extra configs for jets
        jetProducer = getattr(process, 'pfLayer1Jets')
        jetProducer.addGenPartonMatch   = False
        jetProducer.embedGenPartonMatch = False
        jetProducer.genPartonMatch      = ''
        jetProducer.addGenJetMatch      = False
        jetProducer.genJetMatch         = ''
        jetProducer.getJetMCFlavour     = False
        jetProducer.JetPartonMapSource  = ''       
    if( name == 'PFMETs'      or name == 'PFAll' ):
        ## remove mc extra configs for jets
        metProducer = getattr(process, 'pfLayer1METs')        
        metProducer.addGenMET           = False
        metProducer.genMETSource        = ''      



def _removeMCMatchingForPATObject(process, matcherName, producerName):
    ## remove mcMatcher from the default sequence
    objectMatcher = getattr(process, matcherName)
    if (producerName=='pfLayer1Muons'or producerName=='pfLayer1Taus'):
        process.PFPATafterPAT.remove(objectMatcher)
    if (producerName=='patMuons'or producerName=='patTaus'or
        producerName=='patPhotons' or producerName=='patElectrons'):
        process.patDefaultSequence.remove(objectMatcher)
    ## straighten photonProducer
    objectProducer = getattr(process, producerName)
    objectProducer.addGenMatch      = False
    objectProducer.embedGenMatch    = False
    objectProducer.genParticleMatch = ''    


def removeAllPATObjectsBut(process,
                           names,
                           outputInProcess=True
                           ):
    """
    ------------------------------------------------------------------
    remove all PAT objects from the default sequence but a specific
    one:

    process         : process
    name            : list of collection names; supported are
                      'Photons', 'Electrons', 'Muons', 'Taus',
                      'Jets', 'METs'
    outputInProcess : indicate whether there is an output module
                      specified for the process (default is True)            
    ------------------------------------------------------------------    
    """
    removeTheseObjectCollections = ['Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs']
    for obj in range(len(names)):
        removeTheseObjectCollections.remove(names[obj])
    removeSpecificPATObjects(process, removeTheseObjectCollections, outputInProcess)


def removeSpecificPATObjects(process,
                             names,
                             outputInProcess=True
                            ):
    """
    ------------------------------------------------------------------
    remove a specific PAT object from the default sequence:

    process         : process
    names           : listr of collection names; supported are
                      'Photons', 'Electrons', 'Muons', 'Taus', 'Jets',
                      'METs'
    outputInProcess : indicate whether there is an output module
                      specified for the process (default is True)
    ------------------------------------------------------------------    
    """
    ## remove pre object production steps from the default sequence
    for obj in range(len(names)):
        if( names[obj] == 'Photons' ):
            process.patDefaultSequence.remove(getattr(process, 'patPhotonIsolation'))
            process.patDefaultSequence.remove(getattr(process, 'photonMatch'))            
        if( names[obj] == 'Electrons' ):
            process.patDefaultSequence.remove(getattr(process, 'patElectronId'))
            process.patDefaultSequence.remove(getattr(process, 'patElectronIsolation'))
            process.patDefaultSequence.remove(getattr(process, 'electronMatch'))        
        if( names[obj] == 'Muons' ):
            process.patDefaultSequence.remove(getattr(process, 'muonMatch'))
        if( names[obj] == 'Taus' ):
            process.patDefaultSequence.remove(getattr(process, 'patPFCandidateIsoDepositSelection'))
            process.patDefaultSequence.remove(getattr(process, 'patPFTauIsolation'))
            process.patDefaultSequence.remove(getattr(process, 'tauMatch'))
            process.patDefaultSequence.remove(getattr(process, 'tauGenJets'))
            process.patDefaultSequence.remove(getattr(process, 'tauGenJetMatch'))
        if( names[obj] == 'Jets' ):
            process.patDefaultSequence.remove(getattr(process, 'patJetCharge'))
            process.patDefaultSequence.remove(getattr(process, 'patJetCorrections'))
            process.patDefaultSequence.remove(getattr(process, 'jetPartonMatch'))
            process.patDefaultSequence.remove(getattr(process, 'jetGenJetMatch'))
            process.patDefaultSequence.remove(getattr(process, 'jetFlavourId'))                
        if( names[obj] == 'METs' ):
            process.patDefaultSequence.remove(getattr(process, 'patMETCorrections'))
        
        ## remove object production steps from the default sequence    
        if( names[obj] == 'METs' ):
            process.patCandidates.remove( getattr(process, 'pat'+names[obj]) )
        else:
            if( names[obj] == 'Jets' ):
                process.patCandidates.remove( getattr(process, jetCollectionString()) )
                process.selectedPatCandidates.remove( getattr(process, jetCollectionString('selected')) )
                process.countPatCandidates.remove( getattr(process, jetCollectionString('count')) )
            else:
                process.patCandidates.remove( getattr(process, 'pat'+names[obj]) )
                process.selectedPatCandidates.remove( getattr(process, 'selectedPat'+names[obj]) )
                process.countPatCandidates.remove( getattr(process, 'countPat'+names[obj]) )
        ## in the case of leptons, the lepton counter must be modified as well
        if( names[obj] == 'Electrons' ):
            print 'removed from lepton counter: electrons'
            process.countPatLeptons.countElectrons = False
        elif( names[obj] == 'Muons' ):
            print 'removed from lepton counter: muons'
            process.countPatLeptons.countMuons = False
        elif( names[obj] == 'Taus' ):
            print 'removed from lepton counter: taus'
            process.countPatLeptons.countTaus = False
        ## remove from summary
        if( names[obj] == 'METs' ):
            process.patCandidateSummary.candidates.remove( cms.InputTag('pat'+names[obj]) )
        else:
            if( names[obj] == 'Jets' ):
                process.patCandidateSummary.candidates.remove( cms.InputTag(jetCollectionString()) )
                process.selectedPatCandidateSummary.candidates.remove( cms.InputTag(jetCollectionString('selected')) )
                process.cleanPatCandidateSummary.candidates.remove( cms.InputTag(jetCollectionString('clean')) )
            else:
                process.patCandidateSummary.candidates.remove( cms.InputTag('pat'+names[obj]) )
                process.selectedPatCandidateSummary.candidates.remove( cms.InputTag('selectedPat'+names[obj]) )
                process.cleanPatCandidateSummary.candidates.remove( cms.InputTag('cleanPat'+names[obj]) )
    ## remove cleaning for the moment; in principle only the removed object
    ## could be taken out of the checkOverlaps PSet
    if ( outputInProcess ):
        print "---------------------------------------------------------------------"
        print "INFO   : some objects have been removed from the sequence. Switching "
        print "         off PAt cross collection cleaning, as it might be of limited"
        print "         sense now. If you still want to keep object collection cross"
        print "         cleaning within PAT you need to run and configure it by hand"
        removeCleaning(process)
    

def removeCleaning(process, outputInProcess=True):
    """
    ------------------------------------------------------------------
    remove PAT cleaning from the default sequence:

    process         : process
    outputInOricess : indicate whether there is an output module
                      specified for the process (default is True)
    ------------------------------------------------------------------    
    """
    ## adapt single object counters
    for m in listModules(process.countPatCandidates):
        if hasattr(m, 'src'): m.src = m.src.value().replace('cleanPat','selectedPat')
    ## adapt lepton counter
    countLept = process.countPatLeptons
    countLept.electronSource = countLept.electronSource.value().replace('cleanPat','selectedPat')
    countLept.muonSource = countLept.muonSource.value().replace('cleanPat','selectedPat')
    countLept.tauSource = countLept.tauSource.value().replace('cleanPat','selectedPat')
    process.patDefaultSequence.remove(process.cleanPatCandidates)
    if ( outputInProcess ):
        print "---------------------------------------------------------------------"
        print "INFO   : cleaning has been removed. Switch output from clean PAT     "
        print "         candidates to selected PAT candidates."
        ## add selected layer1 objects to the pat output
        from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
        process.out.outputCommands = patEventContentNoCleaning


def addCleaning(process, outputInProcess=True):
    """
    ------------------------------------------------------------------
    add PAT cleaning from the default sequence:

    process : process
    ------------------------------------------------------------------    
    """
    ## adapt single object counters
    process.patDefaultSequence.replace(process.countPatCandidates, process.cleanPatCandidates * process.countPatCandidates)
    for m in listModules(process.countPatCandidates):
        if hasattr(m, 'src'): m.src = m.src.value().replace('selectedPat','cleanPat')
    ## adapt lepton counter
    countLept = process.countPatLeptons
    countLept.electronSource = countLept.electronSource.value().replace('selectedPat','cleanPat')
    countLept.muonSource = countLept.muonSource.value().replace('selectedPat','cleanPat')
    countLept.tauSource = countLept.tauSource.value().replace('selectedPat','cleanPat')
    if ( outputInProcess ):
        print "---------------------------------------------------------------------"
        print "INFO   : cleaning has been added. Switch output from selected PAT    "
        print "         candidates to clean PAT candidates."
        ## add clean layer1 objects to the pat output
        from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
        process.out.outputCommands = patEventContent               
