var s = new sigma('container');
var lastNode;
    

//Default gateway graph
s.graph.addNode({
 
   id: 'ActiveMQ',
   label: 'ActiveMQ',
   x: 0,
   y: 0,
   size: 1,
   color: '#004c8e'
 }).addNode({

   id: 'Default GIFT ActiveMQ Gateway',
   label: 'Default GIFT ActiveMQ Gateway',
   x: 1,
   y: 1,
   size: 1,
   color: '#004c8e'
 }).addEdge({
   id: 'e0',
   source: 'ActiveMQ',
   target: 'Default GIFT ActiveMQ Gateway',
   color: '#83C8C6'    
});

    s.refresh();

   s.settings('zoomingRatio', 1);

function addNodes() {
       var newNodeName = grabAddNodeVal();
         s.graph.addNode({id: newNodeName, label:newNodeName,x: 2, y:2,size: 1, color:'#CD4A42'}).addEdge({id:'e1',source:'Default GIFT ActiveMQ Gateway', target:newNodeName, size: '1', color:'#83C8C6'});
         s.refresh();
       
       //So we can add to the next node
       lastNode = y;
       
      }


function grabAddNodeVal() {
   var newNodeName = $('#nodeAddName').val();

   return String(newNodeName);
}

function grabTextVal() {
   var newNodeName = $('#nodeToRemove').val();

   return String(newNodeName);
}


    
function removeNodes() {
          var lostNodeName = grabTextVal();
         s.graph.dropNode(lostNodeName);
         s.refresh();
         alert("done");
         }
    
