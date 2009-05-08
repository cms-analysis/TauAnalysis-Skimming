#ifndef TauAnalysis_Skimming_MultiBoolEventSelFlagFilter_h
#define TauAnalysis_Skimming_MultiBoolEventSelFlagFilter_h

/** \class MultiBoolEventSelFlagFilter
 *
 * Select events based boolean (event selection) flags
 * (produced by TauAnalysis/RecoTools/plugins/BoolEventSelFlagProducer)
 * 
 * \author Christian Veelken, UC Davis
 *
 * \version $Revision: 1.4 $
 *
 * $Id: MultiBoolEventSelFlagFilter.h,v 1.4 2009/04/24 13:47:17 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include <vector>

class MultiBoolEventSelFlagFilter : public edm::EDFilter
{
 public:
  // constructor 
  explicit MultiBoolEventSelFlagFilter(const edm::ParameterSet&);
    
  // destructor
  virtual ~MultiBoolEventSelFlagFilter();
    
 private:
  bool filter(edm::Event&, const edm::EventSetup&);

//--- read ASCII file containing run and event numbers
  typedef std::vector<edm::InputTag> vInputTag;
  vInputTag flags_;

  int cfgError_;
};

#endif   
