import FWCore.ParameterSet.Config as cms

allLayer1Muons = cms.EDProducer("PATMuonProducer",

    # General configurables
    muonSource = cms.InputTag("muons"),
    pfMuonSource = cms.InputTag("pfMuons"),
    useParticleFlow =  cms.bool( False ),

    # user data to add
    userData = cms.PSet(
      # add custom classes here
      userClasses = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add doubles here
      userFloats = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add ints here
      userInts = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add "inline" functions here
      userFunctions = cms.vstring(""),
      userFunctionLabels = cms.vstring("")
    ),
                                
    embedTrack          = cms.bool(False), ## whether to embed in AOD externally stored tracker track
    embedCombinedMuon   = cms.bool(False), ## whether to embed in AOD externally stored combined muon track
    embedStandAloneMuon = cms.bool(False), ## whether to embed in AOD externally stored standalone muon track
    embedPFCandidate = cms.bool(False),

    # isolation configurables
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowershcal"),
            deltaR = cms.double(0.3)
        ),
        tracker = cms.PSet(
            src = cms.InputTag("patMuonIsolations","muIsoDepositTk"),
            deltaR = cms.double(0.3)
        ),
        user = cms.VPSet(cms.PSet(
            src = cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowersho"),
            deltaR = cms.double(0.3)
        ), 
            cms.PSet(
                src = cms.InputTag("patMuonIsolations","muIsoDepositJets"),
                deltaR = cms.double(0.3)
            )),
        ecal = cms.PSet(
            src = cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowersecal"),
            deltaR = cms.double(0.3)
        )
    ),
    # embed IsoDeposits to recompute isolation easily
    isoDeposits = cms.PSet(
        tracker = cms.InputTag("patMuonIsolations","muIsoDepositTk"),
        ecal    = cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowersecal"),
        hcal    = cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowershcal"),
        user    = cms.VInputTag(
                     cms.InputTag("patMuonIsolations","muIsoDepositCalByAssociatorTowersho"), 
                     cms.InputTag("patMuonIsolations","muIsoDepositJets")
                  ),
    ),

    # Muon ID configurables
    addMuonID = cms.bool(False), ## DEPRECATED OLD TQAF muon ID. 

    # Resolution configurables
    addResolutions = cms.bool(True),
    muonResoFile = cms.string('PhysicsTools/PatUtils/data/Resolutions_muon.root'),
    useNNResolutions = cms.bool(False), ## use the neural network approach?

    # Trigger matching configurables
    addTrigMatch = cms.bool(True),
    trigPrimMatch = cms.VInputTag(cms.InputTag("muonTrigMatchHLT1MuonNonIso"), cms.InputTag("muonTrigMatchHLT1MET65")),

    # MC matching configurables
    addGenMatch = cms.bool(True),
    embedGenMatch = cms.bool(False),
    genParticleMatch = cms.InputTag("muonMatch"), ## particles source to be used for the matching

    # Efficiencies
    addEfficiencies = cms.bool(False),
    efficiencies    = cms.PSet(),

)


