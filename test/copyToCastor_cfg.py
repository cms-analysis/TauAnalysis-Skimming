import FWCore.ParameterSet.Config as cms

process = cms.Process("copyToCastor")

from TauAnalysis.Skimming.EventContent_cff import *

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
process.load('Configuration/Geometry/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('START53_V15::All')
##process.GlobalTag.globaltag = cms.string('GR_P_V42_AN3::All')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "root://gfe02.grid.hep.ph.ic.ac.uk:1097//store/mc/Summer12_DR53X/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/C6A7552D-0607-E211-9C6E-001A928116DA.root"
    ),
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop recoPFTaus_*_*_*'                      
    ),                        
    ##eventsToProcess = cms.untracked.VEventRange(
    ##    '1:521195:1563272921'
    ##)
)

# Get all the skim files from the castor directory
#sourceFilePath = "/castor/cern.ch/user/f/friis/Run50plainharvest/"
#sourceFilePath = "/castor/cern.ch/user/v/veelken/CMSSW_4_2_x/skims/ZtoMuTau/GenZtoMuTauWithinAcc/"
#sourceFilePath = "/castor/cern.ch/user/v/veelken/CMSSW_5_2_x/skims/data/"
#sourceFilePath = "/tmp/veelken/pickEvents/user/v/veelken/CMSSW_5_2_x/skims/data/"
##sourceFilePath = "/afs/cern.ch/user/k/knutzen/public/WToTauNu_ptmin500_TuneZ2Star_8TeV-pythia6-tauola_Summer12-START50_V13-v1_GEN-SIM_ptgreater300/"
##sourceFilePath = "/store/user/chayanit/NoPUbugCheck/"
##
##jobId = "2011Jun30v2"
##jobId = "pickevents_"
##
##source_files = []
##if sourceFilePath.find("/castor/cern.ch/") != -1:
##    import TauAnalysis.Configuration.tools.castor as castor
##    source_files = [ 'rfio:%s' % file_info['path'] for file_info in castor.nslsl(sourceFilePath) ]
##elif sourceFilePath.find("/store/") != -1:
##    import TauAnalysis.Configuration.tools.eos as eos
##    source_files = [ file_info['path'] for file_info in eos.lsl(sourceFilePath) ]
##else:
##    import os
##    source_files = [ "".join([ "file:", sourceFilePath, file ]) for file in os.listdir(sourceFilePath) ]
##
##source_files_matched = []
##for source_file in source_files:
##   if source_file.find(jobId) != -1:
##	source_files_matched.append(source_file)
##print "source_files_matched", source_files_matched
##
##setattr(process.source, "fileNames", cms.untracked.vstring(source_files_matched))

dummyEventSelection = cms.untracked.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('')
    )
)

originalEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring(
        'keep *_*_*_*'
    )
) 

process.copyToCastorOutputModule = cms.OutputModule("PoolOutputModule",
    #AODSIMEventContent,
    originalEventContent,
    fileName = cms.untracked.string(
        ##'/data1/veelken/CMSSW_5_2_x/skims/selEvents_WToTauNu_tauPtGt300_lowTriggerEff_GENSIM.root'
        ##'simZplusJets_madgraph_AOD.root'
        ##'/data1/veelken/CMSSW_5_3_x/skims/simZee_fromChayanit_AOD.root'
        ##'/data1/veelken/CMSSW_5_3_x/skims/simW4JetsToLNu_fromLuigi_AOD.root'
        ##'simZprime2500toTauTau_RECO.root'
        ##'simZprime2500toTauTau_GENSIM.root'
        ##'simQCD_Pt-600to800_AOD.root'
        ##'simDYtoMuMu_embedEqRH_cleanEqDEDX_replaceRecMuons_by_muPt7to25tauPtGt15_embedAngleEq90_noPolarization_wTauSpinner_AOD.root'
        'simTTplusJets_madgraph_AOD.root'                                                
    ),
    maxSize = cms.untracked.int32(1000000000)                                                
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath(process.copyToCastorOutputModule)

