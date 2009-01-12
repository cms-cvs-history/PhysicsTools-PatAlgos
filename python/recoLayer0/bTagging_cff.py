import FWCore.ParameterSet.Config as cms

# Labels of Discriminators to use
patBTaggingDiscriminatorLabels = cms.VInputTag(
    cms.InputTag("combinedSecondaryVertexBJetTags"),
    cms.InputTag("combinedSecondaryVertexMVABJetTags"),
    cms.InputTag("coneIsolationTauJetTags"),
    cms.InputTag("impactParameterMVABJetTags"),
    cms.InputTag("jetBProbabilityBJetTags"),
    cms.InputTag("jetProbabilityBJetTags"),
    cms.InputTag("simpleSecondaryVertexBJetTags"),
    cms.InputTag("softElectronBJetTags"),
    cms.InputTag("softMuonBJetTags"),
    cms.InputTag("softMuonNoIPBJetTags"),
    cms.InputTag("trackCountingHighEffBJetTags"),
    cms.InputTag("trackCountingHighPurBJetTags"),
)
# Labels of TagInfos  to use
patBTaggingTagInfoLabels = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos"),
    cms.InputTag("softElectronTagInfos"), 
    cms.InputTag("softMuonTagInfos"),
    cms.InputTag("impactParameterTagInfos"),
)

# Need to convert all JetTags to ValueMap<double>
patBTags = cms.EDFilter("MultipleDiscriminatorsToValueMaps",
    collection   = cms.InputTag("iterativeCone5CaloJets"),
    associations = patBTaggingDiscriminatorLabels,
    failSilently = cms.untracked.bool(True) 
)

# Need to convert all JetTagInfoss to ValueMap<Ptr<BaseTagInfo>>
patBTagInfos = cms.EDFilter("MultipleTagInfosToValueMaps",
    collection   = cms.InputTag("iterativeCone5CaloJets"),
    associations = patBTaggingTagInfoLabels,
    failSilently = cms.untracked.bool(True) 
)

patBTagging    = cms.Sequence(patBTags * patBTagInfos)
