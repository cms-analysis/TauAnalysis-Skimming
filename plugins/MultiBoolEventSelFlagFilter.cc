#include "TauAnalysis/Skimming/plugins/MultiBoolEventSelFlagFilter.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <TPRegexp.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TString.h>

#include <iostream>
#include <fstream>

const int noMatchRequired = -1;

MultiBoolEventSelFlagFilter::MultiBoolEventSelFlagFilter(const edm::ParameterSet& cfg)
{
  //std::cout << "<MultiBoolEventSelFlagFilter::MultiBoolEventSelFlagFilter>:" << std::endl;

  cfgError_ = 0;

  flags_ = cfg.getParameter<vInputTag>("flags");
  if ( !flags_.size() >= 1 ) {
    edm::LogError ("MultiBoolEventSelFlagFilter") << " List of BoolEventSelFlags must not be empty !!";
    cfgError_ = 1;
  }
}

MultiBoolEventSelFlagFilter::~MultiBoolEventSelFlagFilter()
{
//--- nothing to be done yet...
}

bool MultiBoolEventSelFlagFilter::filter(edm::Event& evt, const edm::EventSetup& es)
{
//--- check that configuration parameters contain no errors
  if ( cfgError_ ) {
    edm::LogError ("filter") << " Error in Configuration ParameterSet --> skipping !!";
    return false;
  }

//--- check values of boolean flags;
//    return true only if **all** flags evaluate to true,
//    otherwise return false
  for ( vInputTag::const_iterator flag = flags_.begin();
	flag != flags_.end(); ++flag ) {
    edm::Handle<bool> value;
    evt.getByLabel(*flag, value);

//--- return immediately once one flag evaluates to false
    if ( (*value) == false ) return false;
  }

//--- all flags evaluate to true
  return true;
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(MultiBoolEventSelFlagFilter);

