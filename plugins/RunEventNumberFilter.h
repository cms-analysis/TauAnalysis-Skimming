#ifndef TauAnalysis_Skimming_RunEventNumberFilter_h
#define TauAnalysis_Skimming_RunEventNumberFilter_h

/** \class RunEventNumberFilter
 *
 * Select events based on run + event number pairs
 * written (a two separate columns) into an ASCII file
 * 
 * \author Christian Veelken, UC Davis
 *
 * \version $Revision: 1.3 $
 *
 * $Id: RunEventNumberFilter.h,v 1.3 2009/03/23 08:16:26 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <string>
#include <map>

class RunEventNumberFilter : public edm::EDFilter
{
 public:
  // constructor 
  explicit RunEventNumberFilter(const edm::ParameterSet&);
    
  // destructor
  virtual ~RunEventNumberFilter();
    
 private:
  bool filter(edm::Event&, const edm::EventSetup&);

//--- read ASCII file containing run and event numbers
  void readRunEventNumberFile();
  
  std::string runEventNumberFileName_;

  typedef std::set<int> lumiSectionNumberSet;
  typedef std::map<edm::EventNumber_t, lumiSectionNumberSet> eventLumiSectionNumberMap;
  std::map<edm::RunNumber_t, eventLumiSectionNumberMap> runEventLumiSectionNumbers_;
  
  typedef std::map<int, int> matchedLumiSectionNumbersMap;
  typedef std::map<edm::EventNumber_t, matchedLumiSectionNumbersMap> matchedEventLumiSectionNumberMap;
  std::map<edm::RunNumber_t, matchedEventLumiSectionNumberMap> matchedRunEventLumiSectionNumbers_;

  int cfgError_;

  long numEventsProcessed_;
  long numEventsToBeSelected_;
  long numEventsSelected_;
};

#endif   