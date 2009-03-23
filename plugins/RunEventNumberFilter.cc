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
 
//--- check for events specified by run + event number in ASCII file
//    and not found in EDM input .root file
  int numRunEventNumbersUnmatched = 0;
  for ( std::map<edm::RunNumber_t, matchedEventLumiSectionNumberMap>::const_iterator run = matchedRunEventLumiSectionNumbers_.begin();
	run != matchedRunEventLumiSectionNumbers_.end(); ++run ) {
    for ( matchedEventLumiSectionNumberMap::const_iterator event = run->second.begin();
	  event != run->second.end(); ++event ) {
      for ( matchedLumiSectionNumbersMap::const_iterator lumiSection = event->second.begin();
	    lumiSection != event->second.end(); ++lumiSection ) {
	if ( lumiSection->second < 1 ) {
	  if ( numRunEventNumbersUnmatched == 0 ) std::cout << "Events not found in PoolInputSource:" << std::endl;
	  std::cout << " Run# = " << run->first << "," 
		    << " Event# " << event->first << ", Luminosity Section# " << lumiSection->first << std::endl;
	  ++numRunEventNumbersUnmatched;
	}
      }
    }
  }

  if ( numRunEventNumbersUnmatched > 0 ) 
    std::cout << "--> Number of unmatched Events = " << numRunEventNumbersUnmatched << std::endl;

//--- check for events specified by run + event number in ASCII file
//    and found more than once in EDM input .root file
  int numRunEventNumbersAmbiguousMatch = 0;
  for ( std::map<edm::RunNumber_t, matchedEventLumiSectionNumberMap>::const_iterator run = matchedRunEventLumiSectionNumbers_.begin();
	run != matchedRunEventLumiSectionNumbers_.end(); ++run ) {
    for ( matchedEventLumiSectionNumberMap::const_iterator event = run->second.begin();
	  event != run->second.end(); ++event ) {
      for ( matchedLumiSectionNumbersMap::const_iterator lumiSection = event->second.begin();
	    lumiSection != event->second.end(); ++lumiSection ) {
	if ( lumiSection->second > 1 ) {
	  if ( numRunEventNumbersAmbiguousMatch == 0 ) std::cout << "Events found in PoolInputSource more than once:" << std::endl;
	  std::cout << " Run# = " << run->first << "," 
		    << " Event# " << event->first << ", Luminosity Section# " << lumiSection->first << std::endl;
	  ++numRunEventNumbersAmbiguousMatch;
	}
      }
    }
  }
  
  if ( numRunEventNumbersAmbiguousMatch > 0 ) 
    std::cout << "--> Number of ambiguously matched Events = " << numRunEventNumbersAmbiguousMatch << std::endl;
}

void RunEventNumberFilter::readRunEventNumberFile()
{
//--- read run + event number pairs from ASCII file

  TPRegexp regexpParser_line("[[:digit:]]+[[:space:]]+[[:digit:]]+[[:space:]]+[[:digit:]]+");
  TPRegexp regexpParser_number("([[:digit:]]+)[[:space:]]+([[:digit:]]+)[[:space:]]+([[:digit:]]+)");

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

//--- match individual run, event and luminosity section numbers;
//    require four matches (first match refers to entire line)
      TObjArray* subStrings = regexpParser_number.MatchS(line_tstring);
      int numSubStrings = subStrings->GetEntries();
      if ( numSubStrings == 4 ) {
	//std::cout << ((TObjString*)subStrings->At(1))->GetString() << std::endl;
	edm::RunNumber_t runNumber = ((TObjString*)subStrings->At(1))->GetString().Atoll();
	//std::cout << ((TObjString*)subStrings->At(2))->GetString() << std::endl;
	edm::EventNumber_t eventNumber = ((TObjString*)subStrings->At(2))->GetString().Atoll();
	//std::cout << ((TObjString*)subStrings->At(3))->GetString() << std::endl;
	edm::LuminosityBlockNumber_t lumiSectionNumber = ((TObjString*)subStrings->At(3))->GetString().Atoll();

	std::cout << "--> adding Run# = " << runNumber << "," 
		  << " Event# " << eventNumber << "," 
		  << " Luminosity Section# " << lumiSectionNumber << std::endl;

	runEventLumiSectionNumbers_[runNumber][eventNumber].insert(lumiSectionNumber);
	matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][lumiSectionNumber] = 0;
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
  edm::LuminosityBlockNumber_t lumiSectionNumber = evt.luminosityBlock();

//--- check if run number matches any of the runs containing events to be selected
  bool isSelected = false;
  if ( runEventLumiSectionNumbers_.find(runNumber) != runEventLumiSectionNumbers_.end() ) {
    const eventLumiSectionNumberMap& eventLumiSectionNumbers = runEventLumiSectionNumbers_.find(runNumber)->second;

    if ( eventLumiSectionNumbers.find(eventNumber) != eventLumiSectionNumbers.end() ) {
      const lumiSectionNumberSet& lumiSectionNumbers = eventLumiSectionNumbers.find(eventNumber)->second;

      if ( lumiSectionNumbers.find(lumiSectionNumber) != lumiSectionNumbers.end() ) isSelected = true;
    }
  }

  ++numEventsProcessed_;
  if ( isSelected ) {
    edm::LogInfo ("filter") << "copying Run# " << runNumber << "," 
			    << " Event# " << eventNumber << ", Luminosity Section# " << lumiSectionNumber << ".";
    ++matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][lumiSectionNumber];
    ++numEventsSelected_;
    return true;
  } else {
    return false;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(RunEventNumberFilter);

