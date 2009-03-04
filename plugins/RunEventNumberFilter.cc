#include "TauAnalysis/Skimming/plugins/RunEventNumberFilter.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <TPRegexp.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TString.h>

#include <iostream>
#include <fstream>

RunEventNumberFilter::RunEventNumberFilter(const edm::ParameterSet& cfg)
{
  //std::cout << "<RunEventNumberFilter::RunEventNumberFilter>:" << std::endl;

  cfgError_ = 0;

  runEventNumberFileName_ = cfg.getParameter<std::string>("runEventNumberFileName");
  if ( runEventNumberFileName_ != "" ) {
    readRunEventNumberFile();
  } else {
    edm::LogError ("RunEventNumberFilter") << " Configuration Parameter runEventNumberFileName = " << runEventNumberFileName_ 
					   << " invalid --> no Events will be selected !!";
    cfgError_ = 1;
  }

  numEventsProcessed_ = 0;
  numEventsSelected_ = 0;
}

RunEventNumberFilter::~RunEventNumberFilter()
{
  std::string matchRemark = ( numEventsSelected_ == numEventsToBeSelected_ ) ? "matches" : "does NOT match";
  edm::LogInfo ("~RunEventNumberFilter") << " Number of Events processed = " << numEventsProcessed_ << std::endl
					 << " Number of Events selected = " << numEventsSelected_ << ","
					 << " " << matchRemark << " Number of Events to be selected = " << numEventsToBeSelected_ << ".";
}

void RunEventNumberFilter::readRunEventNumberFile()
{
  TPRegexp regexpParser_line("[[:digit:]]+[[:space:]]+[[:digit:]]+");
  TPRegexp regexpParser_number("([[:digit:]]+)[[:space:]]+([[:digit:]]+)");

  ifstream runEventNumberFile(runEventNumberFileName_.data());
  int iLine = 0;
  numEventsToBeSelected_ = 0;
  while ( !(runEventNumberFile.eof() || runEventNumberFile.bad()) ) {
    std::string line;
    getline(runEventNumberFile, line);
    ++iLine;

//--- skip empty lines
    if ( line == "" ) continue;

    bool parseError = false;

    TString line_tstring = line.data();
//--- check if line matches two columns of numbers format
    if ( regexpParser_line.Match(line_tstring) == 1 ) {
      //std::cout << "line = '" << line << "'" << std::endl;

//--- match individual run and event numbers;
//    require three matches (first match refers to entire line)
      TObjArray* subStrings = regexpParser_number.MatchS(line_tstring);
      int numSubStrings = subStrings->GetEntries();
      if ( numSubStrings == 3 ) {
	//std::cout << ((TObjString*)subStrings->At(1))->GetString() << std::endl;
	edm::RunNumber_t runNumber = ((TObjString*)subStrings->At(1))->GetString().Atoll();
	//std::cout << ((TObjString*)subStrings->At(2))->GetString() << std::endl;
	edm::EventNumber_t eventNumber = ((TObjString*)subStrings->At(2))->GetString().Atoll();

	std::cout << "--> adding run# = " << runNumber << ", event# " << eventNumber << std::endl;
	runEventNumbers_[runNumber].insert(eventNumber);
	
	++numEventsToBeSelected_;
      } else {
	parseError = true;
      }
      
      delete subStrings;
    } else {
      parseError = true;
    }

    if ( parseError ) {
      edm::LogError ("readRunEventNumberFile") << " Error in parsing Line " << iLine << " = '" << line << "'"
					       << " of File = " << runEventNumberFileName_ << " !!"; 
      cfgError_ = 1;
    }
  }

  if ( numEventsToBeSelected_ == 0 ) {
    edm::LogError ("readRunEventNumberFile") << " Failed to read any run + event Number Pairs from File = " << runEventNumberFileName_ 
					     << " --> no Events will be selected !!";
    cfgError_ = 1;
  }
}

bool RunEventNumberFilter::filter(edm::Event& evt, const edm::EventSetup& es)
{
//--- check that configuration parameters contain no errors
  if ( cfgError_ ) {
    edm::LogError ("filter") << " Error in Configuration ParameterSet --> skipping !!";
    return false;
  }

//--- retrieve run and event numbers from the event
  edm::RunNumber_t runNumber = evt.id().run();
  edm::EventNumber_t eventNumber = evt.id().event();

//--- check if run number matches any of the runs containing events to be selected
  bool isSelected = false;
  if ( runEventNumbers_.find(runNumber) != runEventNumbers_.end() ) {
    const eventNumberSet& eventNumbers = runEventNumbers_[runNumber];

    if ( eventNumbers.find(eventNumber) != eventNumbers.end() ) isSelected = true;
  }

  ++numEventsProcessed_;
  if ( isSelected ) {
    std::cout << " selected Run# " << runNumber << ", Event# " << eventNumber << "." << std::endl;
    ++numEventsSelected_;
    return true;
  } else {
    return false;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(RunEventNumberFilter);

