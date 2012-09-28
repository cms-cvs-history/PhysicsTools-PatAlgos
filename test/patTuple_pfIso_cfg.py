## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.pfTools import *
usePFIso( process )

# process.patElectrons.pfElectronSource = 'particleFlow'

## let it run
process.p = cms.Path(
    process.patDefaultSequence
    #process.pfParticleSelectionSequence +
    #process.eleIsoSequence +
    #process.makePatElectrons +
    #process.selectedPatElectrons
    )

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#   process.source.fileNames =  ['/store/cmst3/group/cmgtools/CMG/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM/V4/PFAOD_0.root']
#                                         ##
process.maxEvents.input = 10
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'patTuple_pfIso.root'
#                                         ##
# process.options.wantSummary = False     ##  (to suppress the long output at the end of the job)

