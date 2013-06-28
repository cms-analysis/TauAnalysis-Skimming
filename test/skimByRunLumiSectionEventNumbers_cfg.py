import FWCore.ParameterSet.Config as cms

import copy
import os
import re

process = cms.Process("skimByRunLumiSectionEventNumbers2")

# import of standard configurations for RECOnstruction
# of electrons, muons and tau-jets with non-standard isolation cones
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.load('Configuration/Geometry/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('START53_V11::All')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(25000)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
##        'rfio:/castor/cern.ch/user/v/veelken/CMSSW_5_2_x/skims/GoldenZmumu/2012Apr12/goldenZmumuEvents_ZplusJets_madgraph2_2012Apr12_AOD_183_2_KFf.root'
##        'file:/data1/veelken/CMSSW_5_3_x/skims/smearcheckPat.root'
        'file:/data1/veelken/CMSSW_5_3_x/skims/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_AOD.root'
    ),
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop recoPFTaus_*_*_*'                      
    )
)

#--------------------------------------------------------------------------------
# set input files
##inputFilePath = '/store/user/fromeo/SIG/ZprimeSSMToTauTau_M2500_TuneZ2star_8TeVpythia6tauola_Summer12_DR53XPU_S10_START53_V7Av1_AODSIM/'
##inputFilePath = '/data2/veelken/CMSSW_5_3_x/PATtuples/TauEnReconstruction/ZprimeSSMToTauTau_M2500_TuneZ2star_8TeVpythia6tauola_Summer12_DR53XPU_S10_START53_V7Av1_AODSIM/'
##inputFile_regex = r"[a-zA-Z0-9_/:.]*[A-Z0-9-]+.root"
inputFilePath = '/data1/veelken/CMSSW_5_3_x/skims/simZprime2500toTauTau_RECO/'
inputFile_regex = r"[a-zA-Z0-9_/:.]*[A-Z0-9-]+.root"

# check if name of inputFile matches regular expression
inputFileNames = []
files = None
if inputFilePath.startswith('/castor/'):
    files = [ "".join([ "rfio:", file_info['path'] ]) for file_info in castor.nslsl(inputFilePath) ]
elif inputFilePath.startswith('/store/'):
    files = [ "".join([ "root://eoscms.cern.ch//eos/cms", file_info['path'] ]) for file_info in eos.lsl(inputFilePath) ]    
else:
    files = [ "".join([ "file:", inputFilePath, file ]) for file in os.listdir(inputFilePath) ]
for file in files:
    #print "file = %s" % file
    inputFile_matcher = re.compile(inputFile_regex)
    if inputFile_matcher.match(file):
        inputFileNames.append(file)
print "inputFileNames = %s" % inputFileNames 

process.source.fileNames = cms.untracked.vstring(inputFileNames)
#--------------------------------------------------------------------------------

process.selectEventsByRunLumiSectionEventNumber = cms.EDFilter("RunLumiSectionEventNumberFilter",
    runLumiSectionEventNumberFileName = cms.string(
        ##'/afs/cern.ch/work/c/calpas/CMSSW/FWliteHisto_v1_6_CaloMet20/debug_C1f.txt'
        ##'debug_C1f.txt'
        ##'/afs/cern.ch/user/v/veelken/scratch0/CMSSW_5_2_3_patch3/src/TauAnalysis/Test/test/debugMEtSys_selEvents.txt'
        ##'/afs/cern.ch/user/v/veelken/scratch0/CMSSW_5_2_3_patch3/src/TauAnalysis/Test/test/runPATTauDEBUGGERforSimon_selEvents.txt'
        ##'/afs/cern.ch/user/v/veelken/scratch0/CMSSW_5_3_3_patch2/src/TauAnalysis/Skimming/test/selEvents_highNoPileUpMEt_fromBrian.txt'
        ##'/afs/cern.ch/user/v/veelken/scratch0/CMSSW_5_3_3_patch2/src/TauAnalysis/Skimming/test/selEvents_pfCandCaloEnNan.txt'
        '/afs/cern.ch/user/v/veelken/scratch0/CMSSW_5_3_3_patch2/src/TauAnalysis/Test/test/selEvents_simZprime2500toTauTau_recTauPtDivGenTauJetPtLt0_7.txt'
    ),
    separator = cms.string(':')
)

process.skimPath = cms.Path( process.selectEventsByRunLumiSectionEventNumber )

eventSelection = cms.untracked.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('skimPath')
    )
)

process.load("Configuration.EventContent.EventContent_cff")
process.origFEVTSIMEventContent = copy.deepcopy(process.FEVTSIMEventContent)
##process.origFEVTSIMEventContent.outputCommands.extend(    
##    cms.untracked.vstring(
##        'drop LumiDetails_lumiProducer_*_*',
##        'drop LumiSummary_lumiProducer_*_*',
##        'drop RunSummary_lumiProducer_*_*',
##        'drop *_MEtoEDMConverter_*_*',
##        'drop *_*_*_skim*',
##        'keep *_*_*_*' # CV: only for Testing !!
##    )
##)    

process.skimOutputModule = cms.OutputModule("PoolOutputModule",
    eventSelection,
    process.origFEVTSIMEventContent,
    fileName = cms.untracked.string(
        #'/data1/veelken/CMSSW_4_2_x/skims/selEvents_checkMEtSmearing_unclusteredEnDown_AOD.root'
        #'/data1/veelken/CMSSW_4_2_x/skims/selEvents_Ztautau_tauIdPassed_but_loosePFIsoFailed_AOD.root'
        #'/data1/veelken/CMSSW_5_2_x/skims/selEvents_bettysTauIdEff_WplusJets_madgraph_AOD.root'
        #'/data1/veelken/CMSSW_5_2_x/skims/selEvents_debugMEtSys_ZplusJets_madgraph_AOD.root'
        #'/data1/veelken/CMSSW_5_2_x/skims/selEvents_debugPATTaus_forSimon_AOD.root'
        #'/data1/veelken/CMSSW_5_3_x/skims/selEvents_highNoPileUpMEt_fromBrian_AOD.root'
        #'/data1/veelken/CMSSW_5_3_x/skims/selEvents_pfCandCaloEnNan_AOD.root'
        '/data1/veelken/CMSSW_5_3_x/skims/selEvents_simZprime2500toTauTau_recTauPtDivGenTauJetPtLt0_7_RECO.root'                                    
    )
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

process.o = cms.EndPath(process.skimOutputModule)

