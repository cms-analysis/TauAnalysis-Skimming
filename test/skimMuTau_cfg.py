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

process.selectedMuons = cms.EDFilter("MuonSelector",
  src = cms.InputTag('muons'),
  cut = cms.string("pt > 8 & abs(eta) < 2.5"),
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
# combine selected muons and tau-jets into pairs;
# require muons and tau-jets to be separated by dR > 0.7 in eta-phi,
# in order to reject events in which the tau-jet refers to the same physical
# particle as the muon (note that almost all muons get selected as tau-jets !!)
#--------------------------------------------------------------------------------

process.muCaloTauPairs = cms.EDProducer("DiCandidatePairProducer",
  useLeadingTausOnly = cms.bool(False),
  srcLeg1 = cms.InputTag('selectedCaloTaus'),
  srcLeg2 = cms.InputTag('selectedMuons'),
  dRmin12 = cms.double(0.3),
  srcMET = cms.InputTag(''),
  recoMode = cms.string(""),
  verbosity = cms.untracked.int32(0)                                       
)

process.selectedMuCaloTauPairs = cms.EDFilter("DiCandidatePairSelector",
  src = cms.InputTag('muCaloTauPairs'),
  cut = cms.string("dR12 > 0.7"),
  filter = cms.bool(True)                                     
)

process.muPFTauPairs = cms.EDProducer("DiCandidatePairProducer",
  useLeadingTausOnly = cms.bool(False),
  srcLeg1 = cms.InputTag('selectedPFTaus'),
  srcLeg2 = cms.InputTag('selectedMuons'),
  dRmin12 = cms.double(0.3),
  srcMET = cms.InputTag(''),
  recoMode = cms.string(""),
  verbosity = cms.untracked.int32(0)
)

process.selectedMuPFTauPairs = cms.EDFilter("DiCandidatePairSelector",
  src = cms.InputTag('muPFTauPairs'),
  cut = cms.string("dR12 > 0.7"),
  filter = cms.bool(True)                                     
)

#--------------------------------------------------------------------------------
# keep event in case it passed either the muon + pfTau or muon + caloTau selection
#--------------------------------------------------------------------------------

process.muPFTauSkimPath = cms.Path(
  (process.selectedPFTaus + process.selectedMuons)
 * process.muPFTauPairs
 * process.selectedMuPFTauPairs
)

process.muCaloTauSkimPath = cms.Path(
  (process.selectedCaloTaus + process.selectedMuons)
 * process.muCaloTauPairs
 * process.selectedMuCaloTauPairs
)

muTauEventSelection = cms.untracked.PSet(
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('muPFTauSkimPath','muCaloTauSkimPath')
  )
)
process.muTauSkimOutputModule = cms.OutputModule("PoolOutputModule",                                 
  tauAnalysisEventContent,                                               
  muTauEventSelection,
  fileName = cms.untracked.string('muTauSkim.root')
)

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath( process.muTauSkimOutputModule )

