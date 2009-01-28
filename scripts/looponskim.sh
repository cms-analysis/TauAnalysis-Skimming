#!/bin/sh
 

for dataset in `less datasetpathskim.txt`;do

echo $dataset
mass=`echo $dataset | awk -F "/" '{print $2}' `
echo $mass
cat  /afs/cern.ch/user/l/lusito/scratch0/CMSSW_2_2_3/src/TauAnalysis/Skimming/test/crab_skim.cfg | sed "s?skimdataset?$dataset?g" | sed "s?skimdir?${mass}?g" > crab_${mass}.cfg
cp crab_${mass}.cfg crab.cfg
#srmcp file:////home/cmsprod/NewAnalysis/CRAB_1_5_2/python/crab_${mass}.cfg srm://pccms2.cmsfarm1.ba.infn.it:8443/pnfs/cmsfarm1.ba.infn.it/data/cms/nicola/Higgs/${mass}/crab_${mass}.cfg  sed "s?datasetpath=skim?$dataset?g"



rfmkdir /castor/cern.ch/user/l/lusito/SkimJanuary09/test2/${mass}
rfchmod 777 /castor/cern.ch/user/l/lusito/SkimJanuary09/test2/${mass}

#cd /home/cmsprod/NewAnalysis/official/CMSSW_1_3_1_HLT6/src

cd /afs/cern.ch/user/l/lusito/scratch0/CMSSW_2_2_3/src/

eval `scramv1 runtime -sh`
#cmsenv
cd /afs/cern.ch/user/l/lusito/scratch0/CMSSW_2_2_3/src/TauAnalysis/Skimming/test/
#source ../crab.sh
source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh



crab -create -submit all

done
