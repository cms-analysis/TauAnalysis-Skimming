import FWCore.ParameterSet.Config as cms

process = cms.Process("printRunLumiSectionEventNumbers")

# import of standard configurations for RECOnstruction
# of electrons, muons and tau-jets with non-standard isolation cones
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.load('Configuration/Geometry/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('START53_V15::All')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/afs/cern.ch/user/i/inaranjo/public/ForChristian/patTuples_LepTauStream_175_1_EMp.root'
    )
)

process.printRunLumiSectionEventNumbers = cms.EDAnalyzer("PrintRunLumiSectionEventNumber",
    output = cms.string('printRunLumiSectionEventNumbers.txt'),
    separator = cms.string('\t')
)

process.o = cms.EndPath(process.printRunLumiSectionEventNumbers)

