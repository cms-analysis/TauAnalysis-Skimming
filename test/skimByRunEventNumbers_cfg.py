import FWCore.ParameterSet.Config as cms

process = cms.Process("skimByRunEventNumber")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FakeConditions_cff")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_1.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_2.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_3.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_4.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_5.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_6.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_7.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_8.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_9.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_10.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_11.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_12.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_13.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_14.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_15.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_16.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_17.root',
        'rfio:/castor/cern.ch/user/l/lusito/SkimJanuary09/ZtautauSkimMuPFCaloTau2/muTauSkim_18.root'
    )                          
)

process.selectEventsByRunEventNumber = cms.EDFilter("RunEventNumberFilter",
    runEventNumberFileName = cms.string('selEvents.txt')
)

process.skimPath = cms.Path( process.selectEventsByRunEventNumber )

eventSelection = cms.untracked.PSet(
    SelectEvents = cms.untracked.PSet(
      SelectEvents = cms.vstring('skimPath')
    )
)

process.skimOutputModule = cms.OutputModule("PoolOutputModule",
    eventSelection,                                 
    fileName = cms.untracked.string('selEvents.root')
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

#--------------------------------------------------------------------------------
# define "hooks" for replacing configuration parameters
# in case running jobs on the CERN batch system
#
# import configuration parameters for submission of jobs to CERN batch system
# (running over skimmed samples stored on CASTOR)
#__from TauAnalysis.Configuration.#recoSampleDefinitionsFileName# import *
#
#__process.source.fileNames = #inputFileNames#
#__process.maxEvents.input = cms.untracked.int32(#maxEvents#)
#__process.selectEventsByRunEventNumber.runEventNumberFileName = cms.string('#runEventNumberFileName#')
#__process.skimOutputModule.fileName = cms.untracked.string('#outputFileName#')
#
#--------------------------------------------------------------------------------

process.o = cms.EndPath( process.skimOutputModule )

