/**
 FUNCTION uponClick, collects the string inside the text area and parses into a parameter for                      the drawgraph function.
**/
function uponClick() {
      var jsonValue = JSON.parse(document.getElementById("jsonText").value);
      drawgraph(s, jsonValue);
}   

/**
s is a global variable for the sigma instance that we will draw our graph using.
**/
var s = new sigma('container');
s.settings('zoomingRatio', 1);
   
/**
 FUNCTION drawgraph, creates the graph by first pushing the nodes, drawing them in priority                        order, and then drawing their edges. Also checks for cycles
 
 PARAM s, sigma instance we're using
 PARAM jsonObj, a string that we collect from the #jsonText div element
**/
function drawgraph(s, jsonObj) {
   
      s.graph.clear();
      var seenArray = {};
      var seenStrings = new StringSet();
   
      //The priority mapping.
      var weights = {activemq: 1, main:2, html:3, postmsg:4, service:5};
      
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
      for (i = 0; i < jsonObj.gateways.length; i++) {
         var tempNode = jsonObj.gateways[i];
         tempNode.label = tempNode.id;
         tempNode.size = 3;
         tempNode.weight = weights[String(tempNode.type)];
         heap.push(tempNode);

         }
      
         
   
   /**Draw the heap by popping off the next minimal weight node (next most important).
      The topNodeFlag is so we can record the name of the topNode to start the seen       
      StringSet.
      */
      var topNodeFlag = true;
      var topNode = "";
      for (i = 0; i < jsonObj.gateways.length; i++) {
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
         s.graph.addNode(tempNode);
         seenArray[tempNode.id] = tempNode;
   }
   
   /**
   Iteratively draw the edges, labeling them by their edge index.
   s.graph.addEdge( {id: LABEL, target: TARGET, source: SOURCE} )
   */
   var edge = 0;
   for (i = 0; i < jsonObj.gateways.length; i++) {
      var tempNode = jsonObj.gateways[i];
      if (tempNode.nodes != {}) {
         for (j = 0; j < tempNode.nodes.length; j++) {
         s.graph.addEdge({id:edge.toString(), target: tempNode.nodes[j], source: tempNode.id});
         edge++;
         }
      } 
   }

   alert(checkCycles(topNode, seenArray, seenStrings));
   
   s.refresh();
   }
   
   /**
   FUNCTION checkCycles, checks for cycles.
   PARAM node, the node we begin searching for cycles for.
   PARAM seenArray, a mapping of seen node names to their node objects.
   PARAM seenStrings, set of node names.  
   
   RETURN string for alert purposes
   **/
   
   function checkCycles(node, seenArray, seenStrings) {
  
      for (var index in node.nodes) {
            var childNodeName = node.nodes[index];      
            if (seenStrings.contains(childNodeName)) {
               return "Looks like you have a cycle! It includes " + childNodeName + "." ;
            } 
            seenStrings.add(childNodeName);
            checkCycles(seenArray[childNodeName], seenArray, seenStrings);  
         }
         
      return "No cycles in your graph, and you're good to go.";
      
   }
       