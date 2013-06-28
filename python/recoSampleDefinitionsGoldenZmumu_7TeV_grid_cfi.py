import FWCore.ParameterSet.Config as cms

import copy

import TauAnalysis.Configuration.plotterProcessDefinitions_cfi as plotter
import TauAnalysis.DQMTools.plotterStyleDefinitions_cfi as styles
from TauAnalysis.Configuration.recoSampleDefaults_cfi import SAMPLE_DEFAULTS

# List of samples to run in the analysis
SAMPLES_TO_ANALYZE = [
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
    ##'WplusJets_madgraph'
]

_millibarns = 1.0e+9
_picobarns =  1.0
_femtobarns = 1.0e-3

TARGET_LUMI = 10./_femtobarns # CV: estimated luminosity of 2012 run A+B+C data

RECO_SAMPLES = {
    'Data_runs190456to193621' : {
        'datasetpath'      : '/DoubleMu/Run2012A-13Jul2012-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 4913546, # 2012/09/12
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt",
        'runselection'     : "190456-193621",
        'conditions'       : 'FT_53_V6_AN2::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs193834to196531' : {
        'datasetpath'      : '/DoubleMu/Run2012B-13Jul2012-v4/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 22786354, # 2012/09/12
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt",
        'runselection'     : "193834-196531",
        'conditions'       : 'FT_53_V6_AN2::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs190782to190949_recover' : {
        'datasetpath'      : '/DoubleMu/Run2012A-recover-06Aug2012-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 722728, # 2012/09/12
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON.txt",
        'runselection'     : "190782-190949",
        'conditions'       : 'FT_53_V6C_AN2::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs198022to198523' : {
        'datasetpath'      : '/DoubleMu/Run2012C-24Aug2012-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 2181586, # 2012/09/28
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt",
        'runselection'     : "198022-198523",
        'conditions'       : 'FT_53_V10_AN2::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs198934to202016' : {
        'datasetpath'      : '/DoubleMu/Run2012C-PromptReco-v2/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 24775919, # 2012/09/12
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-203853_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'runselection'     : "198934-202016",
        'conditions'       : 'GR_P_V40::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs202044to203002' : {
        'datasetpath'      : '/DoubleMu/Run2012C-PromptReco-v2/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 24775919, # 2012/09/12
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-203853_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'runselection'     : "202044-203002",
        'conditions'       : 'GR_P_V40::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs203894to208686' : {
        'datasetpath'      : '/DoubleMu/Run2012D-PromptReco-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 30748995, # 2013/01/30
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt",
        'runselection'     : "203894-208686",
        'conditions'       : 'GR_P_V40::All', # tag for anomalous ECAL laser correction filter, taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/%20MissingETOptionalFilters
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs190456to193621_ReReco' : {
        'datasetpath'      : '/DoubleMu/Run2012A-22Jan2013-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 5636274, # 2013/05/17
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
        'runselection'     : "190456-193621",
        'conditions'       : 'FT_53_V6_AN2::All',
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs193833to196531_ReReco' : {
        'datasetpath'      : '/DoubleMuParked/Run2012B-22Jan2013-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 29282993, # 2013/05/17
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
        'runselection'     : "193833-196531",
        'conditions'       : 'FT_53_V6_AN2::All',
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs198022to203742_ReReco' : {
        'datasetpath'      : '/DoubleMuParked/Run2012C-22Jan2013-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 36820243, # 2013/05/17
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
        'runselection'     : "198022-203742",
        'conditions'       : 'GR_P_V40::All',
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'Data_runs203777to208686_ReReco' : {
        'datasetpath'      : '/DoubleMuParked/Run2012D-22Jan2013-v1/AOD',
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",        
        'events_processed' : 38006513, # 2013/05/17
        'lumi_mask'        : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
        'runselection'     : "203777-208686",
        'conditions'       : 'GR_P_V40::All',
        'lumis_per_job'    : "25",
        'type'             : 'Data'
    },
    'ZplusJets_madgraph' : {
        'datasetpath'      : "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 30459503,
        'events_subset'    : 20000000, # CV: process subset of 20 million events only, in order to save disk space on EOS
        'x_sec'            : 3503.71*_picobarns, # Note: Madgraph samples are generated for M > 50 GeV      
        'type'             : 'smMC'
    },
    'Zmumu_pythia' : {
        'datasetpath'      : "/DYToMuMu_M_20_TuneZ2star_8TeV_pythia6_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 19995104,
        'events_subset'    : 5000000, # CV: only process 5 million events 
        'x_sec'            : 5745.25*_picobarns, # Note: Pythia samples are generated for M > 20 GeV      
        'type'             : 'smMC'
    },
    'Zmumu_powheg' : {
        'datasetpath'      : "/DYToMuMu_M-20_CT10_TuneZ2star_v2_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 48819386,
        'x_sec'            : 5745.25*_picobarns, # Note: Powheg samples are generated for M > 20 GeV      
        'type'             : 'smMC'
    },
    'TTplusJets_madgraph' : {
        'datasetpath'      : "/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 6923750,
        'x_sec'            : 234.*_picobarns, # CV: taken from arXiv:1205.3453
        'type'             : 'smMC'
    },
    'Tbar_tW' : {
        'datasetpath'      : "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 493460,
        'x_sec'            : 11.1*_picobarns, # NLO cross-section @ 8 TeV,
                                              # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    },
    'T_tW' : {
        'datasetpath'      : "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 497658,
        'x_sec'            : 11.1*_picobarns, # NLO cross-section @ 8 TeV,
                                              # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    },
    'PPmuXptGt20Mu15' : {
        'datasetpath'      : "/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          :  "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 7529312,
        'x_sec'            : 0.364*_millibarns*3.7e-4, # x-sec * gen filter efficiency,
                                                       # taken from http://cms.cern.ch/iCMS/prep/requestmanagement?campid=Summer12_DR52X
        'type'             : 'smMC'
    },
    'WW' : {
        'datasetpath'      : "/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          :  "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 10000431,
        'x_sec'            : 57.11*_picobarns, # NLO cross-section @ 8 TeV,
                                               # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    },
    'WZ' : {
        'datasetpath'      : "/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          :  "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 10000283,
        'x_sec'            : 32.32*_picobarns, # NLO cross-section @ 8 TeV,
                                               # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    },
    'ZZ' : {
        'datasetpath'      : "/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        'dbs_url'          :  "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 9799908,
        'x_sec'            : 8.26*_picobarns, # NLO cross-section @ 8 TeV,
                                              # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    },
    'WplusJets_madgraph' : {
        'datasetpath'      : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
        'dbs_url'          : "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet",
        'events_processed' : 57709905,
        'x_sec'            : 36257.2*_picobarns, # NLO cross-section @ 8 TeV,
                                                 # taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'type'             : 'smMC'
    }
}

# Update to use the defaults if necessary
for sample in RECO_SAMPLES.keys():
    defaults = copy.copy(SAMPLE_DEFAULTS)
    defaults.update(RECO_SAMPLES[sample])
    RECO_SAMPLES[sample] = defaults
    
recoSampleDefinitionsGoldenZmumu_7TeV = {
    'SAMPLES_TO_ANALYZE' : SAMPLES_TO_ANALYZE,
    'TARGET_LUMI'        : TARGET_LUMI,
    'RECO_SAMPLES'       : RECO_SAMPLES
}
