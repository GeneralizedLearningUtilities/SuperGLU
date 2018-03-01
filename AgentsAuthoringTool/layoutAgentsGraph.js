var jsonValue;
var fileConfig;
var hasCycles = false;
var nodeTempData;
var counter = 0;

//to display only the gateway/service name on the tool
var gatewayMapping = {"SocketIOGateway" : "edu.usc.ict.superglu.core.SocketIOGateway",
        "ActiveMQTopicMessagingGateway" : "edu.usc.ict.superglu.core.ActiveMQTopicMessagingGateway", "GIFTVHumanBridge" :
        "edu.usc.ict.superglu.vhuman.GIFTVHumanBridge", "Service" : "edu.usc.ict.superglu.core.Service" };

//to display service and gateway as different colored nodes
var typeMapping = {"SocketIOGateway": "gateway", "ActiveMQTopicMessagingGateway": "gateway", "GIFTVHumanBridge": "service", "Others": "service"}

var extraJsonVariable = {}; //to store other JSON variables which are not necessary for graphical representation
var tableJson; //to store the Table Connection JSON which is a subset of the Config Json
var editor; //to set the Connection Table Json

/**
s is a global variable for the sigma instance that we will draw our graph using.
**/
var s = new sigma({
   renderer: {
     container: document.getElementById('container'),
     type: 'canvas',
   },
   settings: {
     maxNodeSize: 10,
     minArrowSize: 8,
     defaultLabelSize: 20,
     defaultEdgeColor: "#000",
   }
 });

/**
  Initializing default Json, default Connection table, default type Mapping
**/
$(document).ready(function() {

   var mydata = JSON.parse(data);
   fileConfig = JSON.stringify(mydata[0]);
   var jsonValue = JSON.parse(fileConfig);
   modifyForTable(jsonValue);
   drawConnectionsTable();


   //Code to show full gateway/service type when hovered in dropdown
   //Position tooltip function
   var positionTooltip = function(event) {
      var tPosX = event.pageX - 5;
      var tPosY = event.pageY + 20;
      $('div.selectTooltip').css({top: tPosY, left: tPosX});
   };

   //Show tooltip function
   var showTooltip = function(event) {
      $('div.selectTooltip').remove();
      var $thisTitle = $(this).text();
      //alert($thisTitle)
      //alert(gatewayMapping[$thisTitle]);
      $('<div class="selectTooltip">' + gatewayMapping[$thisTitle] + '</div>').appendTo('body');
      positionTooltip(event);
   };

   //Hide tooltip function
   var hideTooltip = function() {
      $('div.selectTooltip').remove();
   };

   $('.multiSelect option').each(function() {
      $(this).hover(showTooltip, hideTooltip).mousemove(positionTooltip);
   });

   //Need to add a mouseout event to the select as tooltips do not hide if the user moves off of the select horizontally
   $('.multiSelect').mouseout(hideTooltip);

});

/**
  greying out Other Type text input if dropwdown gateway/service is selected
**/
$('#gatewayType').change(function() {
    if ($(this).val() != "") {
      document.getElementById("otherType").disabled = true;
    }
    else{
      document.getElementById("otherType").disabled = false;
    }
});

//Adds all node IDs and corresponding Child Nodes to display it on Connection table
function modifyForTable(jsonObj){
  tableJson = {};
  for (var key in jsonObj) {
    if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
    for ( var childKey in jsonObj[key] ) {
      tableJson[childKey] = jsonObj[key][childKey].nodes
      }
    }
  }
}

function drawConnectionsTable(){
  var container = document.getElementById('jsoneditor');

  var options = {
    mode: 'tree',
    onError: function (err) {
      alert(err.toString());
    },
    onModeChange: function (newMode, oldMode) {
      console.log('Mode switched from', oldMode, 'to', newMode);
    },
  };

  editor = new JSONEditor(container, options, tableJson);
}

/**
FUNCTION handleFileSelect, triggers when a file is selected
  It fetches a HTML element to display the contents of the JSON file
*/
document.getElementById('files').addEventListener('change', handleFileSelect, false);
function handleFileSelect(evt){
  var files = evt.target.files; // FileList object

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, f; f = files[i]; i++)
  {

      document.getElementById("configInputFileName").value = files[i].name;
      //reader object to fetch and display the contents
      var reader = new FileReader();
      reader.onload = (function(reader)
      {
          return function()
          {
              fileConfig = reader.result; //setting the config json
              var lines = fileConfig.split('\n');
              document.getElementById('myPopup').innerHTML= "<pre>"+ fileConfig +"</pre>";
              uponClick(fileConfig);  //draw graph once JSON is set
          }
      })(reader);
      reader.readAsText(f);
  }
}

/**
 FUNCTION uponClick
  -> merges JSON from table and config file loaded
  -> sets Json in the Connection table
  -> calls the drawgraph function.
**/
function uponClick(fileConfig) {
    var jsonValue = JSON.parse(fileConfig);
    jsonValue = mergeTableAndConfig(jsonValue);
    jsonValue = modifyJson(jsonValue); //removes elements not required for the graphical representation
    modifyForTable(jsonValue); //requires only ID and Nodes
    editor.set(tableJson);
    drawgraph(s, jsonValue);
}

/*
  Iterates over json in Connections table and adds diff nodes to the config JSON
*/
function mergeTableAndConfig(jsonObj){
  for (var key in jsonObj) {
    if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
      for ( var childKey in tableJson ) {
      if(! jsonObj[key].hasOwnProperty(childKey)){
      jsonObj[key][childKey] = {}
      jsonObj[key][childKey].id  = childKey;
      jsonObj[key][childKey].nodes = tableJson[childKey];
       }
     }
   }
 }
 return jsonObj;
}

//To store extra attributes in a variable which are not required for graphical representation
function modifyJson(jsonObj){
  for (var key in jsonObj) {
    if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
    for ( var childKey in jsonObj[key] ) {
        if ( jsonObj[key][childKey].id ){
          continue
        }
        else{
          extraJsonVariable[childKey] = jsonObj[key][childKey]
          delete jsonObj[key][childKey]
        }
      }
    }
  }
  fileConfig = JSON.stringify(jsonObj);
  return jsonObj;
}

/**
  This function is to merge and add a dummy node to the graph
  **/
  /**
   FUNCTION addNode, adds Nodes to the provided json by calling the merge function
    based on the given values.
  **/
function addDummyNode(){
      jsonValue = addDummyElement(JSON.parse(fileConfig));
      modifyForTable(jsonValue);
      editor.set(tableJson)
      fileConfig = JSON.stringify(jsonValue);
      drawgraph(s, jsonValue);
}

/**
FUNCTION merge, triggers when a new Node is added
  It fetches the provided JSON object and iterates to specific location
    to add the new Nodes and updates the JSON raw display area
 */
/**
  This merge function is to merge and create a dummy entry in the JSON
  **/
function addDummyElement(jsonObj){
  for ( var key in jsonObj){
    if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
      var tempName = "dummy" + counter;
      counter ++;
      jsonObj[key][tempName] = { "classId": "ServiceConfiguration", "id": tempName, "nodes": []};
    }
  }
   //document.getElementById('fileContainer').innerHTML= "<pre>"+JSON.stringify(jsonObj, null, 2)+"</pre>";
   return jsonObj;
}

/**
FUNCTION deleteNodes, deletes from
  1) Node from the graph
  2) JSON object
  3) Raw JSON display
**/
function deleteNode(){

  try{
    if(fileConfig){
      //console.log(fileConfig);
      var jsonValue = JSON.parse(fileConfig);
      if(nodeTempData){
      var id = nodeTempData.node.id;
      s.graph.dropNode(id);
      for (var key in jsonValue) {
        if (jsonValue.hasOwnProperty(key) && key == "serviceConfigurations") {
        for ( var childKey in jsonValue[key] ) {
          if ( childKey == id){
            delete  jsonValue[key][childKey];
            }
          else{
            var index = jsonValue[key][childKey].nodes.indexOf(id);
            if (index > -1) {
                jsonValue[key][childKey].nodes.splice(index, 1);
                }
              }
            }
          }
        }
      modifyForTable(jsonValue);
      editor.set(tableJson)
      }
      else{
        window.alert("Please select a node");
      }
      fileConfig = JSON.stringify(jsonValue);
      //console.log(jsonValue);
      s.refresh();
      drawgraph(s, jsonValue);
      document.getElementById('myPopup').innerHTML= "<pre>"+JSON.stringify(jsonValue, null, 2)+"</pre>";
      clearEditables();
      }
    else{
      window.alert("Please add a JSON file and continue");
      }
    }
  catch(err){
    window.alert("Please select a node");
  }
}

/**
  Function to Update the nodes and its connections when update connections button is clicked

**/
function uponTableChange(){
  var jsonValue = JSON.parse(fileConfig);
  var modifiedTableJsonValue = modifyTableJson(editor.get());
  var modifiedJsonValue = modifyFromTableJson(jsonValue, modifiedTableJsonValue);
  drawgraph(s, modifiedJsonValue);
  editor.set(modifiedTableJsonValue);
  fileConfig = JSON.stringify(modifiedJsonValue);
  document.getElementById('myPopup').innerHTML= "<pre>"+JSON.stringify(modifiedJsonValue, null, 2)+"</pre>";  //to populate raw Json display area
}

//Pre-Processing of the Connections json to remove redundant edges from all Nodes
function modifyTableJson(jsonObj){
  var nodes = []  //keep check of existent nodes for easy edge deletion
  for ( var childKey in jsonObj){
    nodes.push(childKey);
    }
  for ( var childKey in jsonObj){
    for ( var eachChildKey in jsonObj[childKey]){
      var index = nodes.indexOf(jsonObj[childKey][eachChildKey]);
      if (index == -1) {
        for (i = 0; i < jsonObj[childKey].length; i++) {
          if (jsonObj[childKey][i] == jsonObj[childKey][eachChildKey])
              jsonObj[childKey].splice(i, 1);
        }
      }
    }
  }
  return jsonObj;
}

//Add and Delete nodes from config Json with respect to nodes added or deleted in Connections table json
function modifyFromTableJson(jsonObj, tableJsonObj){
  for (var key in jsonObj) {
    if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
    for ( var childKey in jsonObj[key] ) {
      if (tableJsonObj.hasOwnProperty(childKey)){
        jsonObj[key][childKey].nodes = tableJsonObj[childKey]
        }
      else{
        for ( var eachChildKey in jsonObj[key] ) {
          if ( eachChildKey == childKey){
            delete  jsonObj[key][eachChildKey];
            }
          else{
            var index = jsonObj[key][eachChildKey].nodes.indexOf(childKey);
            if (index > -1) {
                jsonObj[key][eachChildKey].nodes.splice(index, 1);
                }
              }
            }
        }
      }
    for ( var childKey in tableJsonObj){
      if (jsonObj[key].hasOwnProperty(childKey)) {
        continue;
      }
      else{
        jsonObj[key][childKey] = { "id": childKey }
        jsonObj[key][childKey].nodes = tableJsonObj[childKey]
      }
      }
    }
  }
  return jsonObj;
}

/**
FUNCTION drawgraph, draws the graphs by creating Nodes and Edges
**/
function drawgraph(s, jsonObj) {

      s.graph.clear();
      var seenArray = {};
      var seenStrings = new StringSet();

      //The priority mapping.
      var weights = { 'edu.usc.ict.superglu.core.ActiveMQTopicMessagingGateway' : 1,
      'edu.usc.ict.superglu.core.SocketIOGateway': 2, Main:3, HTML:4, PostMsg:5,
       Service:6, 'edu.usc.ict.superglu.vhuman.GIFTVHumanBridge':7, 'Others':8};

      //Creating a heap with a custom comparator based on the priority weights above.
      var heap = new Heap(function cmp(a, b) {
      if (a.weight < b.weight) {
         return -1;
      }
      if (a.weight > b.weight) {
         return 1;
      }
      return 0;
      });

      //x, y for node positions. (0,0) will be where the first node is always.
      var x = 0;
      var y = 0;

      /**Iterating through the gateways, we add default properties to convert the string
         representation of the node into a node object that we push to the heap.
      */

      var ObjCounter = 0
      for (var key in jsonObj) {
        if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
        for ( var childKey in jsonObj[key] ) {
          if(jsonObj[key].hasOwnProperty(childKey)){
            ObjCounter ++;
            var tempNode = jsonObj[key][childKey];
            tempNode.label = tempNode.id;
            tempNode.size = 3;
             var weightValue = weights[String(tempNode.type)] ? weights[String(tempNode.type)] : weights['Others'];
            tempNode.weight = weightValue
            heap.push(tempNode);
          }
        }
        }
      }

      var topNodeFlag = true;
      var topNode = "";
      var colors = {gateway:"#000000", service:"#FF0000", other:"#000000"}
      for (i = 0; i < ObjCounter; i++) {
         var tempNode = heap.pop();
         if (topNodeFlag) {
            topNode = tempNode;
            topNodeFlag = false;
            seenStrings.add(topNode.id);
         }
         tempNode.x = Math.random(0, 0.2);
         tempNode.y = y + 0.2;
         x = x + 0.2;
         y = y + 0.2;
         var typeVariable;
         if( tempNode.type){
           typeVariable = tempNode.type.split('.');
         }
         else{
           typeVariable = 'Others'
         }
         var nodeType = typeMapping[typeVariable[typeVariable.length-1]] ? typeMapping[typeVariable[typeVariable.length-1]] : typeMapping['Others'];
         tempNode.color = colors[nodeType];
         s.graph.addNode(tempNode);
         seenArray[tempNode.id] = tempNode;
   }//);

   var edge = 0;

   for (var key in jsonObj) {
     if (jsonObj.hasOwnProperty(key) && key == "serviceConfigurations") {
     for ( var childKey in jsonObj[key] ) {
       if(jsonObj[key].hasOwnProperty(childKey)){
         var tempNode = jsonObj[key][childKey];
         if (tempNode.nodes != {}) {
            for (j = 0; j < tempNode.nodes.length; j++) {
            s.graph.addEdge({id:edge.toString(), target: tempNode.nodes[j], source: tempNode.id});
            s.refresh();
            edge++;
           }
          }
        }
      }
    }
  }

   if(checkCycles(topNode, seenArray, seenStrings)){
      hasCycles = true;
      alert("Has cycle please update");
    }
   s.refresh();
   }

   function checkCycles(node, seenArray, seenStrings) {
      for (var index in node.nodes) {
            var childNodeName = node.nodes[index];
            if (seenStrings.contains(childNodeName)) {
              return true
            }
            seenStrings.add(childNodeName);
            hasCycles = checkCycles(seenArray[childNodeName], seenArray, seenStrings);
            if (hasCycles)
              break
         }
      return false

   }

/**
FUNCTION writeJsonToFile, creates a NEW Json file with
  al the new added Nodes and edges. Provides a link to download the file
  Doesn't allow if cycle found in the graph.
*/
function writeJsonToFile(){
     if(hasCycles == true)
        window.alert("Graph contains cycles");
     makeJSONReady()
     var fileName = document.getElementById("configFileName").value;
     var text = JSON.stringify(JSON.parse(fileConfig), null, "\t");
     var blob = new Blob([text], {type:'application/json'});
     var x = document.getElementById("Downloadable");
     var link = document.createElement("a");
     link.download = fileName;
     link.innerHTML = "Download File";
     link.href = window.URL.createObjectURL(blob);
     x.appendChild(link);
}

/**
FUNCTION makeJSONReady, updates the JSON objects by removing the
  unnecessary elements like priority weights, graph coordinates etc
*/
function makeJSONReady(){
  var jsonValue = JSON.parse(fileConfig);
  for (var key in jsonValue) {
    if (jsonValue.hasOwnProperty(key) && key == "serviceConfigurations") {
      for (eachExtra in extraJsonVariable){
        jsonValue[key][eachExtra] = extraJsonVariable[eachExtra]
      }
      for ( var childKey in jsonValue[key] ) {
          delete  jsonValue[key][childKey]['label'];
          delete  jsonValue[key][childKey]['size'];
          delete  jsonValue[key][childKey]['weight'];
          delete  jsonValue[key][childKey]['x'];
          delete  jsonValue[key][childKey]['y'];
          delete jsonValue[key][childKey]['color'];
        }
    }
  }
  fileConfig = JSON.stringify(jsonValue);
}

/**
  bind functiton to bind all Nodes to edit and delete from JSON
    by clicking the Node
**/
s.bind('clickNode',onClick);

/**
function onclickyo(event){
  console.log(event.data);
}

function testing(event){
  console.log(event.data);
}
**/
/**
FUNCTION onClick, triggers when the Node binding function has an event:
  It displays the editable fields of a Node and provides
    option to Edit or Delete a Node
**/
function onClick(event){
  clearEditables();
  nodeTempData = event.data;
  nodeTempData.node["tempID"] = event.data.node.id;
  document.getElementById("idName").value = event.data.node.id;

  var otherTypeGrey = false
  if ( event.data.node.type){
  var typeVariable = event.data.node.type.split('.');
  for (i = 0; i < document.getElementById("gatewayType").length; ++i){
    if (document.getElementById("gatewayType").options[i].value == typeVariable[typeVariable.length-1]){
      document.getElementById("gatewayType").value == typeVariable[typeVariable.length-1];
      document.getElementById("gatewayType").options.selectedIndex = i;
      otherTypeGrey = true
    }
  }
  document.getElementById("otherType").value = event.data.node.type//.split('.').slice(-1).pop();
  document.getElementById("otherType").disabled = otherTypeGrey;
  }

  var nodeEdges = event.data.node.nodes;
  var nodeTable = document.getElementById("nodeTable");
  for ( i = 0; i < nodeEdges.length ; i++){
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.value = nodeEdges[i];
    td.appendChild(input)
    tr.appendChild(td)
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "button");
    input.onclick = deleteNodeRow;
    input.value = "-";
    td.appendChild(input)
    tr.appendChild(td)
    nodeTable.appendChild(tr)
    }

  //Params
  if ( event.data.node.params){
  var nodeParams = event.data.node.params;
  var nodeTable = document.getElementById("paramTable");
  for (var key in nodeParams) {
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.style = "width:130px"
    input.value = key;
    td.appendChild(input)
    tr.appendChild(td)
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.style = "width:130px"
    input.value = JSON.stringify(nodeParams[key]);
    td.appendChild(input)
    tr.appendChild(td)
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "button");
    input.onclick = deleteParamRow;
    input.value = "-";
    td.appendChild(input)
    tr.appendChild(td)
    nodeTable.appendChild(tr)
    }
  }
}

//Clear all the Node Editor entries to display new selected node data
function clearEditables(){
  document.getElementById("gatewayType").value = "";
  document.getElementById("idName").value = '';
  document.getElementById("nodeTable").innerHTML = '';
  document.getElementById("paramTable").innerHTML = '';
  document.getElementById("otherType").value = '';
  document.getElementById("otherType").disabled = false;
}

/**
FUNCTION updateJsonForm, updates:
  1) Node in the graph
  2) JSON object
  3) Raw JSON display
**/
function updateJsonForm(){
   var jsonValue = JSON.parse(fileConfig);
   var x = document.getElementById("gateWayForm");
   for (var key in jsonValue) {
     if (jsonValue.hasOwnProperty(key) && key == "serviceConfigurations") {
     for ( var childKey in jsonValue[key] ) {
       if ( childKey == nodeTempData.node.tempID ){
         jsonValue[key][childKey].id = document.getElementById("idName").value;
         nodeEdges = []
         var nodeTable = document.getElementById("nodeTable");
          for (var i = 0, row; row = nodeTable.rows[i]; i++) {
              nodeEdges.push(nodeTable.rows[i].cells[0].children[0].value);
          }
          jsonValue[key][childKey].nodes = nodeEdges;
         var gatewayType = document.getElementById("gatewayType");
         var otherType = document.getElementById('otherType').value;

         if ( document.getElementById('otherType').disabled ) {
           jsonValue[key][childKey].type = gatewayMapping[gatewayType.options[gatewayType.selectedIndex].text];
         }
         else{
           jsonValue[key][childKey].type = otherType
         }

         //Params
         paramValues = {}
         var nodeTable = document.getElementById("paramTable");
          for (var i = 0, row; row = paramTable.rows[i]; i++) {
              var paramValue;
              try{
                  paramValue = JSON.parse(nodeTable.rows[i].cells[1].children[0].value);
              }
              catch(err){
                paramValue = JSON.parse(JSON.stringify(nodeTable.rows[i].cells[1].children[0].value));
              }
              paramValues[nodeTable.rows[i].cells[0].children[0].value] = paramValue;
          }
          jsonValue[key][childKey].params = paramValues

         if (nodeTempData.node.tempID !== document.getElementById("idName").value) {
            Object.defineProperty(jsonValue[key], document.getElementById("idName").value,
            Object.getOwnPropertyDescriptor(jsonValue[key], nodeTempData.node.tempID));
            delete jsonValue[key][nodeTempData.node.tempID];
          }
       }
     }
   }
 }
 modifyForTable(jsonValue);
 editor.set(tableJson)
 fileConfig = JSON.stringify(jsonValue);
 document.getElementById('myPopup').innerHTML= "<pre>"+JSON.stringify(jsonValue, null, 2)+"</pre>";
 drawgraph(s, jsonValue);
 clearEditables();
 //var x = document.getElementById("gateWayForm").remove();
}

// When the user clicks on show json, open the popup
function showRawJson() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

//Add new row with text input when Add Nodes button is clicked
function addNodeRow(){
  var table = document.getElementById('nodeTable');
  var tr = document.createElement('tr');
  var td = document.createElement('td');
  var input = document.createElement("input");
  input.setAttribute("type", "text");
  td.appendChild(input)
  tr.appendChild(td)
  var td = document.createElement('td');
  var input = document.createElement("input");
  input.setAttribute("type", "button");
  input.onclick = deleteNodeRow;
  input.value = "-";
  td.appendChild(input)
  tr.appendChild(td)
  table.appendChild(tr)
}

//Delete row with selected row ID when Delete Node button is clicked
function deleteNodeRow(r){
  var i = r.target.parentNode.parentNode.rowIndex;
  document.getElementById("nodeTable").deleteRow(i);
}

//Add new row with two text input when Add Param button is clicked
function addParamRow(){
  var table = document.getElementById('paramTable');
  var tr = document.createElement('tr');
  for (i = 0; i < 2; i++) {
    var td = document.createElement('td');
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.style = "width:130px"
    td.appendChild(input)
    tr.appendChild(td)
  }
  var td = document.createElement('td');
  var input = document.createElement("input");
  input.setAttribute("type", "button");
  input.onclick = deleteParamRow;
  input.value = "-";
  td.appendChild(input)
  tr.appendChild(td)
  table.appendChild(tr)
}

//Delete row with selected row ID when Delete Param button is clicked
function deleteParamRow(r) {
    var i = r.target.parentNode.parentNode.rowIndex;
    document.getElementById("paramTable").deleteRow(i);
}
