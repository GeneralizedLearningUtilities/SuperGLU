/**Keeps track of the number of nodes.
*/
var nodenum = 0;
   
/**
   FUNCTION updateJSONText, appends the next node to the JSONtext div element.
*/
function updateJSONText() {
     
   /**This line is really long, but it results
   */
   document.getElementById('jsonText').innerHTML =    getDropDownVal(document.getElementById('jsonText').innerHTML, document.getElementById('lastNodeFlag').checked );
      
   }
     
/**
FUNCTION getDropDownVal, creates new node's string representation
   PARAM prevString, string that we are appending (all gateways so far)
   PARAM lastNodeFlag, boolean representing if this will be the last node (closing the string            representation altogether
   
   RETURN string representing new node
   
   Format of each node is {"id": "NAME", "type": "TYPEOFSERVICE", "nodes": []}
*/
function getDropDownVal(prevString, lastNodeFlag) {
   
      var nodeString = '{"id": ';
      
      var dropDownVal = document.getElementById("dropdown");
   
      if(dropDownVal.selectedIndex == 0) {
           alert('You didnt select a type of gateway or service');
      }
      else {
          var selectedText = dropDownVal.options[dropDownVal.selectedIndex].text;
         nodeNames = document.getElementById("nodeNames").value;
         
         if(nodeNames.length > 0) { 
            var splitNodeNames = nodeNames.split(",");
       
            for (var node in splitNodeNames) {
            //Surrounding node names with quotation marks
            splitNodeNames[node] = '"' + splitNodeNames[node] + '"';
            }
            
            nodeString = nodeString + ' "' + String(selectedText) + nodenum.toString() + '", "type" : "' + String(selectedText) + '", "nodes": ['  + splitNodeNames.toString() +  ']}' ;
      
         }
         else {
            nodeString = nodeString + ' "' + String(selectedText) + nodenum.toString() + '", "type" : "' + String(selectedText) + '", "nodes": []}' ;
            
            
         }
         if (lastNodeFlag) {
            nodeString = nodeString + ']}' ;
         } else {
            nodeString = nodeString + ', ';
         }
         nodenum++;
         return prevString + nodeString;
      }
      
   }