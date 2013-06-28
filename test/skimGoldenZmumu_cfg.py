import FWCore.ParameterSet.Config as cms

#--------------------------------------------------------------------------------
# skim Z --> mu+ mu- candidate events passing "golden" VTBF selection
#--------------------------------------------------------------------------------

process = cms.Process("skimGoldenZmumu2")

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
process.load('Configuration/Geometry/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

#--------------------------------------------------------------------------------
# define configuration parameter default values

isMC = True # use for MC
##isMC = False # use for Data
custom_globaltag = None
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# define "hooks" for replacing configuration parameters
# in case running jobs on the CERN batch system/grid
#
#__isMC = #isMC#
#__custom_globaltag = #custom_globaltag#
#
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# define GlobalTag to be used for event reconstruction

if isMC:
    process.GlobalTag.globaltag = cms.string('START53_V11::All')
else:
    process.GlobalTag.globaltag = cms.string('GR_R_53_V21::All')

if custom_globaltag:
    process.GlobalTag.globaltag = cms.string(custom_globaltag)    
#--------------------------------------------------------------------------------    

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        ##'/store/user/veelken/CMSSW_5_3_x/skims/simZmumu_madgraph_RECO_1_1_lTW.root'
        'file:/data1/veelken/CMSSW_5_3_x/skims/goldenZmumuEvents_ZplusJets_madgraph_RECO_205_1_XhE.root'                       
    ),
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop recoPFTaus_*_*_*'                      
    )
)

# import event content definition:
# keep full FEVT (RAW + RECO) event content
# plus collections of goodMuons, goldenZmumuCandidates and "tag" & "probe" flags
from TauAnalysis.Skimming.goldenZmmEventContent_cff import *

# load definition of VBTF Z --> mu+ mu- event selection
# (with no isolation cuts applied on one of the two muons)
process.load("TauAnalysis.Skimming.goldenZmmSelectionVBTFnoMuonIsolation_cfi")

# load definitions of data-quality filters
process.load("TauAnalysis.TauIdEfficiency.filterDataQuality_cfi")
if isMC:
    process.dataQualityFilters.remove(process.hltPhysicsDeclared)
    process.dataQualityFilters.remove(process.dcsstatus)
    process.dataQualityFilters.remove(process.hcalLaserEventFilter)
    process.dataQualityFilters.remove(process.ecalLaserCorrFilter)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

#--------------------------------------------------------------------------------
# select events passing "golden" VTBF Z --> mu+ mu- selection
#--------------------------------------------------------------------------------

process.goldenZmumuSkimPath = cms.Path(
    process.dataQualityFilters 
   + process.goldenZmumuSelectionSequence
)

# add event counter for Mauro's "self baby-sitting" technology
process.processedEventsSkimming = cms.EDProducer("EventCountProducer")
process.eventCounterPath = cms.Path(process.processedEventsSkimming)

#--------------------------------------------------------------------------------
# save events passing "golden" VTBF Z --> mu+ mu- selection
#--------------------------------------------------------------------------------

process.skimOutputModule = cms.OutputModule("PoolOutputModule",                                 
    ##goldenZmumuEventContent,
     outputCommands = cms.untracked.vstring(                                    
        'drop *',
        'keep EventAux_*_*_*',
        'keep LumiSummary_*_*_*',                       
        'keep edmMergeableCounter_*_*_*',
        'keep *_gtDigis_*_*',
        'keep *_hltL1GtObjectMap_*_*',
        'keep *_TriggerResults_*_*',
        'keep *_l1extraParticles_*_*',                                        
        'keep *_addPileupInfo_*_*',  
        'keep *_muons_*_*',
        'keep *_muonMETValueMapProducer_*_*',
        'keep *_muonTCMETValueMapProducer_*_*',     
        'keep *_standAloneMuons_*_*',
        'keep *_globalMuons_*_*',
        'keep *_tevMuons_*_*',                        
        'keep *_goodMuons_*_*',
        'keep *_goodIsoMuons_*_*',                                
        'keep *_goldenZmumuCandidatesGe0IsoMuons_*_*',
        'keep *_goldenZmumuCandidatesGe1IsoMuons_*_*',
        'keep *_goldenZmumuCandidatesGe2IsoMuons_*_*',                              
        'keep *_gsfElectrons_*_*',
        'keep *_gsfElectronCores_*_*',
        'keep *_electronGsfTracks_*_*',
        'keep *_reducedEcalRecHitsEB_*_*',
        'keep *_reducedEcalRecHitsEE_*_*',
        'keep *_correctedMulti5x5SuperClustersWithPreshower_*_*',
        'keep *_multi5x5SuperClusters_*_*',
        'keep *_towerMaker_*_*',                  
        'keep *_eidTight_*_*',
        'keep *_eidLoose_*_*',
        'keep *_eidRobustTight_*_*',
        'keep *_eidRobustHighEnergy_*_*',
        'keep *_eidRobustLoose_*_*',
        'keep *_photons_*_*',
        'keep *_hpsPFTauProducer*_*_*',
        'keep *_hpsPFTauDiscrimination*_*_*',
        'keep *_particleFlow_*_*',                        
        'keep *_particleFlowDisplacedVertex_*_*',
        'keep *_ak5PFJets_*_*',
        'keep *_kt6PFJets_*_*',                                        
        'keep *_ak5CaloJets_*_*',        
        'keep *_generalTracks_*_*',
        'keep *_allConversions_*_*',          
        'keep *_generalV0Candidates_*_*',
        'keep *_offlinePrimaryVertices_*_*',
        'keep *_offlineBeamSpot_*_*',
        'keep *_pfMet_*_*',
        'keep *_metJESCorAK5PFJet_*_*',                       
        'keep *_met_*_*',
        'keep *_corMetGlobalMuons_*_*',                        
        'keep *_metNoHF_*_*',
        'keep *_corMetGlobalMuonsNoHF_*_*',
        'keep *_genParticles_*_*',
        'keep *_ak5GenJets_*_*',              
        'keep *_genMetTrue_*_*',                 
        'keep *_genMetCalo_*_*'
    ),                                                
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('goldenZmumuSkimPath')
    ),
    fileName = cms.untracked.string('goldenZmumuEvents_AOD.root')
    ##fileName = cms.untracked.string('/data1/veelken/CMSSW_5_3_x/skims/goldenZmumuEvents_AOD.root')                                      
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath(process.skimOutputModule)

processDumpFile = open('skimGoldenZmumu.dump' , 'w')
print >> processDumpFile, process.dumpPython()

