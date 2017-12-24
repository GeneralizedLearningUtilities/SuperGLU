// Zet.declare('ZetTestClass' , {
//     superclass : null,
//     defineBody : function(self){
//         // Constructor Function
//         self.construct = function construct(id){
//             self.id = id;
//         };
//     }
// });
// Zet.declare('ZetTestClass2' , {
//     //superclass : null,
//     CLASS_ID : "ZetTestClass2_OVERRIDE",
//     defineBody : function(self){
//         // Constructor Function
//         self.construct = function construct(id){
//             self.myId = id;
//         };
//     }
// });
// Zet.declare('ZetTestClass3' , {
//     superclass : ZetTestClass2,
//     defineBody : function(self){
//     }
// });
//
// buster.testCase("ZetTests", {
//     setUp: function (){
//     },
//     "testisInstance": function () {
//         x = ZetTestClass(1);
//         y = ZetTestClass2(2);
//         z = ZetTestClass3(3);
//         buster.assert(ZetTestClass.isInstance(x));
//         buster.refute(ZetTestClass.isInstance(y));
//         buster.refute(ZetTestClass.isInstance(z));
//         buster.refute(ZetTestClass.isInstance(1));
//         buster.assert(x.isInstance(x));
//         buster.refute(x.isInstance(y));
//         buster.refute(x.isInstance(1));
//
//         // Check Y (Class 2)
//         buster.refute(ZetTestClass2.isInstance(x));
//         buster.assert(ZetTestClass2.isInstance(y));
//         buster.assert(ZetTestClass2.isInstance(z));
//         buster.refute(ZetTestClass2.isInstance(1));
//         buster.refute(y.isInstance(x));
//         buster.assert(y.isInstance(y));
//         buster.assert(y.isInstance(z));
//         buster.refute(y.isInstance(1));
//
//         // Check Z (Class 3)
//         buster.refute(ZetTestClass3.isInstance(x));
//         buster.refute(ZetTestClass3.isInstance(y));
//         buster.assert(ZetTestClass3.isInstance(z));
//         buster.refute(ZetTestClass3.isInstance(1));
//         buster.refute(z.isInstance(x));
//         buster.refute(z.isInstance(y));
//         buster.refute(z.isInstance(1));
//     },
//     "testinstanceOf": function () {
//         x = ZetTestClass(1);
//         y = ZetTestClass2(2);
//         z = ZetTestClass3(3);
//         buster.assert(x.instanceOf(ZetTestClass));
//         buster.refute(x.instanceOf(ZetTestClass2));
//         buster.refute(x.instanceOf(ZetTestClass3));
//
//         buster.refute(y.instanceOf(ZetTestClass));
//         buster.assert(y.instanceOf(ZetTestClass2));
//         buster.refute(y.instanceOf(ZetTestClass3));
//
//         buster.refute(z.instanceOf(ZetTestClass));
//         buster.assert(z.instanceOf(ZetTestClass2));
//         buster.assert(z.instanceOf(ZetTestClass3));
//     },
//     "testCLASS_ID": function () {
//         x = ZetTestClass(1);
//         y = ZetTestClass2(2);
//         z = ZetTestClass3(3);
//         buster.assert(ZetTestClass.CLASS_ID === 'ZetTestClass');
//         buster.assert(ZetTestClass2.CLASS_ID === 'ZetTestClass2_OVERRIDE');
//         buster.assert(ZetTestClass3.CLASS_ID === 'ZetTestClass3');
//
//         buster.assert(x.CLASS_ID === 'ZetTestClass');
//         buster.assert(y.CLASS_ID === 'ZetTestClass2_OVERRIDE');
//         buster.assert(z.CLASS_ID === 'ZetTestClass3');
//     },
// });