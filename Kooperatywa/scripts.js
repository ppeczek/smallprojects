// Return array consisting only unique values
function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

// Check if string is in Name + Surname format
function checkForName(string) {
  if (string.indexOf(" ") != -1 &&
      string.charCodeAt(0) > 64 &&
      string.charCodeAt(0) < 91 &&
      string.charCodeAt(1) > 96 &&
      string.charCodeAt(1) < 123 &&
      string.charCodeAt(string.indexOf(" ") + 1) > 64 &&
      string.charCodeAt(string.indexOf(" ") + 1) < 91) {
      return string;
   }
  else {
    return "";
  }
}

// Get list of members who did duty
function whoDidDuty(data) {
  var peopleDoneDuty = [];
  for (var i = 0; i < data.length; i++) {
    for (var j = 0; j < data.length; j++) {
      if (typeof data[i][j] == "string") {
        var dataTrimmed = data[i][j].trim();
        var name = checkForName(dataTrimmed);
        if (name && name.indexOf("/") != -1) {
          peopleDoneDuty.push(name.substring(0, name.indexOf("/")));
          peopleDoneDuty.push(name.substring(name.indexOf("/") + 1));
        }
        else if (name) {
          peopleDoneDuty.push(name);
        }
      }
    }
  }
  return peopleDoneDuty = peopleDoneDuty.filter(onlyUnique).sort();  
}

// Get sheet with active members list
function getMembersSheet(url) {
  var ss = SpreadsheetApp.openByUrl(url);
  var sheets = ss.getSheets()
  for (var k = 0; k < sheets.length; k++) {
    if (sheets[k].getSheetName() === "Aktywni Raport") {
      return sheets[k];
    }
  }
}

// Get list of active members
function getActiveMembers(data) {
  var activeMembers = [];
  for (var a = 1; a < data.length; a++) {
    if (data[a][0] != ""){
      activeMembers.push((data[a][0] + " " + data[a][1]));
    }
  }
 return activeMembers.filter(onlyUnique).sort();
}

// Compare two lists, return object with unique values of each list and duplicates list
function compareLists(peopleDoneDuty, activeMembers) {
  var compared = {"peopleOkay": [], "peopleToCheck": [], "peopleDoneDuty": []}
  for (var x = 0; x < activeMembers.length; x++) {
    var index = peopleDoneDuty.indexOf(activeMembers[x]);
    if (index != -1) {
      compared.peopleOkay.push(activeMembers[x]);
      peopleDoneDuty.splice(index, 1);
    }
    else {
      compared.peopleToCheck.push(activeMembers[x]);
    }
  }
  compared.peopleDoneDuty = peopleDoneDuty;
  return compared;
}

// Main function
function myFunction() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var peopleDoneDuty = whoDidDuty(data);
  
  var membersSheet = getMembersSheet('https://docs.google.com/spreadsheets/d/1IZMhL-sN5GAtj6e_7odva1k3v_ZSneToIjaz1eWPciE/edit#gid=2018401575');
  var membersSheetData = membersSheet.getDataRange().getValues();
  var activeMembers = getActiveMembers(membersSheetData);
  
  var comparedLists = compareLists(peopleDoneDuty, activeMembers);
  
  var notFoundPeopleDoneDuty = comparedLists.peopleDoneDuty;
  var peopleOkay = comparedLists.peopleOkay;
  var peopleToCheck = comparedLists.peopleToCheck;

//  Logger.log(notFoundPeopleDoneDuty.length);
//  Logger.log(activeMembers.length);
//  Logger.log(peopleOkay.length);
//  Logger.log(peopleToCheck.length);

}

// Simple append to spreadsheet
//Logger.log(peopleDoneDuty.sort());
//  sheet.appendRow(["", 'Dyżurujący']);
//  for (var k = 0; k < peopleDoneDuty.length; k++){
//    sheet.appendRow([k + 1, peopleDoneDuty[k]]);
//  }

// Example similiarity checking script
//function similarity(s1, s2) {
//  var longer = s1;
//  var shorter = s2;
//  if (s1.length < s2.length) {
//    longer = s2;
//    shorter = s1;
//  }
//  var longerLength = longer.length;
//  if (longerLength == 0) {
//    return 1.0;
//  }
//  return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
//}
//
//
//function editDistance(s1, s2) {
//  s1 = s1.toLowerCase();
//  s2 = s2.toLowerCase();
//
//  var costs = new Array();
//  for (var i = 0; i <= s1.length; i++) {
//    var lastValue = i;
//    for (var j = 0; j <= s2.length; j++) {
//      if (i == 0)
//        costs[j] = j;
//      else {
//        if (j > 0) {
//          var newValue = costs[j - 1];
//          if (s1.charAt(i - 1) != s2.charAt(j - 1))
//            newValue = Math.min(Math.min(newValue, lastValue),
//              costs[j]) + 1;
//          costs[j - 1] = lastValue;
//          lastValue = newValue;
//        }
//      }
//    }
//    if (i > 0)
//      costs[s2.length] = lastValue;
//  }
//  return costs[s2.length];
//}
//
//console.log(similarity('Agata Amelczenko','Agata Amelczenko'));