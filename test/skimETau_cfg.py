import FWCore.ParameterSet.Config as cms

process = cms.Process("muTauSkim")

from TauAnalysis.Skimming.EventContent_cff import *

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FakeConditions_cff")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
#
# Z --> tau tau (all decay modes; simulated with TAUOLA)
# 9k events CMSSW_2_2_3 RelVal sample
#
    '/store/relval/CMSSW_2_2_3/RelValZTT/GEN-SIM-RECO/STARTUP_V7_v4/0003/A4A3988A-BCCB-DD11-A103-001617E30E28.root',
    '/store/relval/CMSSW_2_2_3/RelValZTT/GEN-SIM-RECO/STARTUP_V7_v4/0003/D412FFFC-BCCB-DD11-8B20-000423D952C0.root',
    '/store/relval/CMSSW_2_2_3/RelValZTT/GEN-SIM-RECO/STARTUP_V7_v4/0003/F01E4F34-BDCB-DD11-B87D-001617C3B77C.root',
    '/store/relval/CMSSW_2_2_3/RelValZTT/GEN-SIM-RECO/STARTUP_V7_v4/0004/1CAA08F8-D3CB-DD11-ADF9-000423D6B358.root',
    '/store/relval/CMSSW_2_2_3/RelValZTT/GEN-SIM-RECO/STARTUP_V7_v4/0004/2800478C-08CC-DD11-94BB-0019B9F72BAA.root'
  )
)

#--------------------------------------------------------------------------------
# select muons and tau-jets
#--------------------------------------------------------------------------------

process.selectedElectrons = cms.EDFilter("GsfElectronSelector",
      src = cms.InputTag("pixelMatchGsfElectrons"),
      cut = cms.string("pt > 8 & abs(eta) < 2.5 & eSuperClusterOverP>0.8 & eSuperClusterOverP<1.25"),
      filter = cms.bool(True)
 )

process.selectedPFTaus = cms.EDFilter("PFTauSelector",
  src = cms.InputTag('pfRecoTauProducer'),
  discriminators = cms.VPSet(
    cms.PSet(
      discriminator = cms.InputTag("pfRecoTauDiscriminationByLeadingPionPtCut"),
      selectionCut = cms.double(0.5)
    )
  ),
  filter = cms.bool(True)
)

process.selectedCaloTaus = cms.EDFilter("CaloTauSelector",
  src = cms.InputTag('caloRecoTauProducer'),
  discriminators = cms.VPSet(
    cms.PSet(
      discriminator = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut"),
      selectionCut = cms.double(0.5)
    )
  ),
  filter = cms.bool(True)
)

#--------------------------------------------------------------------------------
# combine selected muons and tau-jets into pairs
#--------------------------------------------------------------------------------

process.eCaloTauPairs = cms.EDProducer("DiTauProducer",
  hadronicTaus = cms.InputTag('selectedCaloTaus'),
  leptonicTaus = cms.InputTag('selectedElectrons'),
  METs = cms.InputTag(''),
  metMode = cms.int32(1),
  useLeadingTaus = cms.bool(False),
  verbose =  cms.untracked.bool(False)
)

process.ePFTauPairs = cms.EDProducer("DiTauProducer",
  hadronicTaus = cms.InputTag('selectedPFTaus'),
  leptonicTaus = cms.InputTag('selectedElectrons'),
  METs = cms.InputTag(''),
  metMode = cms.int32(1),
  useLeadingTaus = cms.bool(False),
  verbose =  cms.untracked.bool(False)
)

#--------------------------------------------------------------------------------
# discard tau-jets that pass muon identification criteria
# (in order to reject events in which there is only one muon and no tau-jet;
#  note that almost all muons get selected as tau-jets !!)
#--------------------------------------------------------------------------------

process.selectedElecPFTauPairs = cms.EDFilter("DiTauAntiOverlapSelector",
  src = cms.InputTag('ePFTauPairs'),
  dRmin = cms.double(0.7),
  filter = cms.bool(True)                                     
)

process.selectedElecCaloTauPairs = cms.EDFilter("DiTauAntiOverlapSelector",
  src = cms.InputTag('eCaloTauPairs'),
  dRmin = cms.double(0.7),
  filter = cms.bool(True)                                     
)

process.ePFTauSkimPath = cms.Path(
    (process.selectedPFTaus + process.selectedElectrons) *
    process.ePFTauPairs *
    process.selectedElecPFTauPairs
    )

process.eCaloTauSkimPath = cms.Path(
    (process.selectedCaloTaus + process.selectedElectrons) *
    process.eCaloTauPairs *
    process.selectedElecCaloTauPairs
    )

eTauEventSelection = cms.untracked.PSet(
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('ePFTauSkimPath','eCaloTauSkimPath')
  )
)
process.eTauSkimOutputModule = cms.OutputModule("PoolOutputModule",                                 
  tauAnalysisEventContent,                                               
  eTauEventSelection,
  fileName = cms.untracked.string('eTauSkim.root')
)

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath( process.eTauSkimOutputModule )

