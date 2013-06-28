#!/usr/bin/env python

from TauAnalysis.Skimming.recoSampleDefinitionsGoldenZmumu_7TeV_grid_cfi import recoSampleDefinitionsGoldenZmumu_7TeV
from TauAnalysis.Configuration.submitAnalysisToGrid import submitAnalysisToGrid
from TauAnalysis.Configuration.userRegistry import getJobId

import os
import subprocess

configFile = 'skimGoldenZmumu_cfg.py'
jobId = '2013Feb14'

outputFilePath = 'CMSSW_5_3_x/skims/GoldenZmumu/%s/' % jobId
##outputFilePath = ''

samplesToAnalyze = [
    #'Data_runs190456to193621',
    #'Data_runs193834to196531',
    #'Data_runs190782to190949_recover',
    #'Data_runs198022to198523',
    #'Data_runs198934to202016',
    #'Data_runs202044to203002',
    #'Data_runs203894to208686',
    'Data_runs190456to193621_ReReco',
    'Data_runs193833to196531_ReReco',
    'Data_runs198022to203742_ReReco',
    'Data_runs203777to208686_ReReco'
    #'ZplusJets_madgraph',
    #'Zmumu_pythia',
    #'Zmumu_powheg',
    #'TTplusJets_madgraph',
    #'Tbar_tW',
    #'T_tW',
    #'PPmuXptGt20Mu15',
    #'WW',
    #'WZ',
    #'ZZ',
    #'WplusJets_madgraph'
]

# Define what output file name a skimmed sample will have
def output_mapper(channel, sample, jobId):
    output_file = "goldenZmumuEvents_%s_%s_AOD.root" % (sample, jobId)
    return output_file

# Function to prepare customized config files specific to TauIdEff. skim 
def customizeConfigFile(sampleName, cfgFileName_original, cfgFileName_modified = None):
    cfgFile_original = open(cfgFileName_original, "r")
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()

    cfg_modified = cfg_original.replace("#__", "")
    isMC = "False"
    if recoSampleDefinitionsGoldenZmumu_7TeV['RECO_SAMPLES'][sampleName]['type'] != 'Data':
        isMC = "True"
    cfg_modified = cfg_modified.replace("#isMC#", isMC)
    custom_globaltag = "None"
    if 'conditions' in recoSampleDefinitionsGoldenZmumu_7TeV['RECO_SAMPLES'][sampleName]:
        custom_globaltag = recoSampleDefinitionsGoldenZmumu_7TeV['RECO_SAMPLES'][sampleName]['conditions']
    cfg_modified = cfg_modified.replace("#custom_globaltag#", "'%s'" % custom_globaltag)

    if cfgFileName_modified is None:
        cfgFileName_modified = cfgFileName_original.replace("_cfg.py", "_customized_%s_cfg.py" % sampleName)
    cfgFile_modified = open(cfgFileName_modified, "w")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()

    return cfgFileName_modified

if len(samplesToAnalyze) == 0:
    samplesToAnalyze = recoSampleDefinitionsGoldenZmumu_7TeV['SAMPLES_TO_ANALYZE']

for sampleToAnalyze in samplesToAnalyze:

    # prepare customized config file as basis for further modifications by "TauAnalysis machinery"...
    configFile_customized = customizeConfigFile(sampleToAnalyze, configFile)

    # apply further modifications and submit job to grid
    submitAnalysisToGrid(configFile = configFile_customized, channel = "goldenZmumu", jobId = jobId,
                         samples = recoSampleDefinitionsGoldenZmumu_7TeV,
                         samplesToAnalyze = [ sampleToAnalyze ],
                         disableFactorization = True, disableSysUncertainties = True, disableZrecoilCorrections = True,
                         outputFilePath = outputFilePath, outputFileMap = output_mapper, savePlots = False)

    # move customized config file to "./crab" subdirectory
    #
    # NOTE: "TauAnalysis machinery" does not work if customized config file
    #       is created in "./crab" subdirectory from the start
    #
    subprocess.call("mv %s crab" % configFile_customized, shell = True)





