#include "TauAnalysis/Skimming/plugins/RunEventNumberFilter.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <TPRegexp.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TString.h>

#include <iostream>
#include <fstream>

const int noMatchRequired = -1;

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
	  std::cout << " Run# = " << run->first << ", Event# " << event->first << "," 
		    << " Luminosity Section# " << lumiSection->first << std::endl;
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
	  std::cout << " Run# = " << run->first << ", Event# " << event->first << ","
		    << " Luminosity Section# " << lumiSection->first << std::endl;
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

  TPRegexp regexpParser_twoColumnLine("[[:digit:]]+[[:space:]]+[[:digit:]]+");	   
  TPRegexp regexpParser_twoColumnNumber("([[:digit:]]+)[[:space:]]+([[:digit:]]+)");

  TPRegexp regexpParser_threeColumnLine("[[:digit:]]+[[:space:]]+[[:digit:]]+[[:space:]]+[[:digit:]]+");
  TPRegexp regexpParser_threeColumnNumber("([[:digit:]]+)[[:space:]]+([[:digit:]]+)[[:space:]]+([[:digit:]]+)");

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
//--- check if line matches three column format;
//    in which case require three matches (first match refers to entire line)
//    and match individually run, event and luminosity section numbers
    if ( regexpParser_threeColumnLine.Match(line_tstring) == 1 ) {
      TObjArray* subStrings = regexpParser_threeColumnNumber.MatchS(line_tstring);
      int numSubStrings = subStrings->GetEntries();
      if ( numSubStrings == 4 ) {
	edm::RunNumber_t runNumber = ((TObjString*)subStrings->At(1))->GetString().Atoll();
	edm::EventNumber_t eventNumber = ((TObjString*)subStrings->At(2))->GetString().Atoll();
	edm::LuminosityBlockNumber_t lumiSectionNumber = ((TObjString*)subStrings->At(3))->GetString().Atoll();

	std::cout << "--> adding Run# = " << runNumber << ", Event# " << eventNumber << "," 
		  << " Luminosity Section# " << lumiSectionNumber << std::endl;

	runEventLumiSectionNumbers_[runNumber][eventNumber].insert(lumiSectionNumber);
	matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][lumiSectionNumber] = 0;
	++numEventsToBeSelected_;
      } else {
	parseError = true;
      }
      
      delete subStrings;
    } else if ( regexpParser_twoColumnLine.Match(line_tstring) == 1 ) {
//--- check if line matches two column format;
//    in which case require three matches (first match refers to entire line)
//    and match individually run and event numbers 
//    (set lumiSectionNumber to -1 to indicate that to match for luminosity section numbers is required)
      TObjArray* subStrings = regexpParser_twoColumnNumber.MatchS(line_tstring);
      int numSubStrings = subStrings->GetEntries();
      if ( numSubStrings == 3 ) {
	edm::RunNumber_t runNumber = ((TObjString*)subStrings->At(1))->GetString().Atoll();
	edm::EventNumber_t eventNumber = ((TObjString*)subStrings->At(2))->GetString().Atoll();

	std::cout << "--> adding Run# = " << runNumber << "," 
		  << " Event# " << eventNumber << std::endl;

	runEventLumiSectionNumbers_[runNumber][eventNumber].insert(noMatchRequired);
	matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][noMatchRequired] = 0;
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
  bool lumiSection_noMatchRequired = true;
  if ( runEventLumiSectionNumbers_.find(runNumber) != runEventLumiSectionNumbers_.end() ) {
    const eventLumiSectionNumberMap& eventLumiSectionNumbers = runEventLumiSectionNumbers_.find(runNumber)->second;

    if ( eventLumiSectionNumbers.find(eventNumber) != eventLumiSectionNumbers.end() ) {
      const lumiSectionNumberSet& lumiSectionNumbers = eventLumiSectionNumbers.find(eventNumber)->second;

      if ( lumiSectionNumbers.find(noMatchRequired) != lumiSectionNumbers.end() ) {
	isSelected = true;
      } else {
	edm::LuminosityBlockNumber_t lumiSectionNumber = evt.luminosityBlock();
	if ( lumiSectionNumbers.find(lumiSectionNumber) != lumiSectionNumbers.end() ) {
	  isSelected = true;
	  lumiSection_noMatchRequired = false;
	}
      } 
    }
  }

  ++numEventsProcessed_;
  if ( isSelected ) {
    if ( lumiSection_noMatchRequired ) {
      edm::LogInfo ("filter") << "copying Run# " << runNumber << ", Event# " << eventNumber << ".";
      ++matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][noMatchRequired];
    } else {
      edm::LuminosityBlockNumber_t lumiSectionNumber = evt.luminosityBlock();
      edm::LogInfo ("filter") << "copying Run# " << runNumber << ", Event# " << eventNumber << ","
			      << " Luminosity Section# " << lumiSectionNumber << ".";
      ++matchedRunEventLumiSectionNumbers_[runNumber][eventNumber][lumiSectionNumber];
    }
    ++numEventsSelected_;
    return true;
  } else {
    return false;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(RunEventNumberFilter);

