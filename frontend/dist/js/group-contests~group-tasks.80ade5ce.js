(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["group-contests~group-tasks"],{"0944":function(t,e,a){"use strict";var n=a("fa64"),s=a.n(n);s.a},"0b40":function(t,e,a){},"0e72":function(t,e,a){},"14c3":function(t,e,a){var n=a("c6b6"),s=a("9263");t.exports=function(t,e){var a=t.exec;if("function"===typeof a){var r=a.call(t,e);if("object"!==typeof r)throw TypeError("RegExp exec method returned something other than an Object or null");return r}if("RegExp"!==n(t))throw TypeError("RegExp#exec called on incompatible receiver");return s.call(t,e)}},1778:function(t,e,a){},1799:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return!t.$types.isNull(t.count)&&!t.$types.isNull(t.page)&&t.pageCount>1?a("div",{staticClass:"pl-2 pr-2 mt-1"},[a("paginate",{attrs:{clickHandler:t.changePage,"page-count":t.pageCount,"page-range":5,"container-class":"pagination","page-class":"page","prev-class":"prev-page","next-class":"next-page","page-link-class":"page-link","prev-link-class":"page-link","next-link-class":"page-link","active-class":"active"},model:{value:t.page,callback:function(e){t.page=e},expression:"page"}})],1):t._e()},s=[],r=(a("a9e3"),{data:function(){return{page:null}},props:{count:Number,pagesize:Number},methods:{changePage:function(t){var e=Object.assign({},this.$route.query,{page:t});this.$router.push({query:e}).catch((function(){}))}},created:function(){var t=this.$route.query.page,e=void 0===t?"1":t;e=parseInt(e),this.page=e},computed:{pageCount:function(){return Math.max(1,Math.floor((this.count+this.pagesize-1)/this.pagesize))}}}),i=r,c=a("2877"),l=Object(c["a"])(i,n,s,!1,null,null,null);e["a"]=l.exports},"2c00":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return t.$types.isNull(t.task)?t._e():a("div",[!t.$types.isNull(t.task)&&t.task.can_edit_task?a("div",{staticClass:"p-r"},[a("div",{staticClass:"a-tr"},[a("router-link",{staticClass:"btn nlnk",attrs:{to:{name:"task_edit",params:{id:t.task.id}}}},[t._v(" Edit task ")])],1)]):t._e(),a("h1",{staticClass:"header"},[t._v(" "+t._s(t.task.name)+" ")]),a("div",{staticClass:"author mt-1"},[t._v(" By "),a("user",{attrs:{rating:t.task.author_rating,username:t.task.author_username}}),t._v(" , "),t.solved.link?a("router-link",{staticClass:"link nlnk",attrs:{to:t.solved.link}},[t._v(t._s(t.solved.number)+" solves ")]):a("span",[t._v(t._s(t.solved.number)+" solves")])],1),t.task.hints.length>0?a("div",{staticClass:"hints mt-1"},t._l(t.task.hints,(function(t,e){return a("hint",{key:e,attrs:{id:t,num:e+1}})})),1):t._e(),a("div",{staticClass:"tags mt-1 mb-1"},[a("span",{staticClass:"tags-h"},[t._v("Tags:")]),t._l(t.task.tags_details,(function(t){return a("tag",{key:t.id,attrs:{name:t.name}})}))],2),a("div",{staticClass:"hr"}),a("div",{staticClass:"content mt-1"},[a("div",{staticClass:"markdown"},[a("markdown",{attrs:{content:t.task.description}})],1)]),a("div",{staticClass:"hr mt-1"}),t.task.files_details.length>0?a("div",{staticClass:"files mt-1"},[a("div",[t._v("Files:")]),t._l(t.task.files_details,(function(e){return a("div",{key:e.id,staticClass:"mt-1"},[a("a",{staticClass:"nlnk link",attrs:{href:e.file_field,target:"_blank"}},[t._v(" "+t._s(e.name)+" ")])])}))],2):t._e(),t.task.files_details.length>0?a("div",{staticClass:"hr mt-1"}):t._e(),a("form",{staticClass:"mt-2",on:{submit:function(e){return e.preventDefault(),t.submitFlag(t.flag)}}},[a("f-input",{attrs:{customClasses:[t.task.is_solved_by_user?"solved":"",t.task.is_solved_on_upsolving&&!t.task.is_solved_by_user?"upsolved":""],errors:t.errors["flag"],name:"flag",placeholder:"Flag",type:"text"},model:{value:t.flag,callback:function(e){t.flag=e},expression:"flag"}}),a("div",{staticClass:"ff"},[a("f-detail",{attrs:{errors:t.errors["detail"]}})],1),t._m(0)],1)])},s=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"ff"},[a("input",{staticClass:"btn",attrs:{type:"submit",value:"Submit"}})])}],r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[t.show?a("div",[a("hr"),a("span",{staticClass:"hint",on:{click:t.change}},[t._v("Hint "+t._s(t.num)+": "+t._s(t.text))]),a("hr")]):a("span",{staticClass:"link",on:{click:t.change}},[t._v("Hint "+t._s(t.num))]),a("f-detail",{attrs:{errors:t.errors["detail"]}})],1)},i=[],c=(a("a9e3"),a("96cf"),a("1da1")),l={props:{id:Number,num:Number},data:function(){return{show:!1,text:"",errors:{}}},methods:{change:function(){var t=Object(c["a"])(regeneratorRuntime.mark((function t(){var e,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(this.show){t.next=12;break}return t.prev=1,t.next=4,this.$http.get("/task_hints/".concat(this.id,"/"));case 4:e=t.sent,a=e.data,this.text=a.body,t.next=12;break;case 9:t.prev=9,t.t0=t["catch"](1),this.errors=this.$parse(t.t0.response.data);case 12:this.show=!this.show;case 13:case"end":return t.stop()}}),t,this,[[1,9]])})));function e(){return t.apply(this,arguments)}return e}()}},o=l,u=(a("0944"),a("2877")),p=Object(u["a"])(o,r,i,!1,null,"2cc286ed",null),f=p.exports,d=a("c009"),v=a("e6e0"),h=a("b05e"),g={props:{task:Object,errors:Object,submitFlag:Function,solved:Object},components:{Tag:d["a"],Markdown:v["a"],FInput:h["a"],Hint:f},data:function(){return{flag:null}}},_=g,m=(a("dfb0"),Object(u["a"])(_,n,s,!1,null,"19115da6",null));e["a"]=m.exports},"32d8":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"group"},[a("input",t._b({staticClass:"input",attrs:{type:"checkbox",invalid:t.invalid},domProps:{checked:t.value},on:{input:function(e){return t.$emit("input",e.target.checked)}}},"input",t.$attrs,!1)),a("label",{staticClass:"label"},[t._v(t._s(t.label))]),t.invalid?a("div",t._l(t.errors,(function(e){return a("div",{key:e,staticClass:"error"},[t._v(" "+t._s(e)+" ")])})),0):t._e()])},s=[],r={props:{label:String,value:Boolean,errors:Array},computed:{invalid:function(){return this.$types.isArray(this.errors)&&this.errors.length>0}}},i=r,c=(a("7530"),a("2877")),l=Object(c["a"])(i,n,s,!1,null,"7007b029",null);e["a"]=l.exports},"590c":function(t,e,a){"use strict";var n=a("0b40"),s=a.n(n);s.a},7530:function(t,e,a){"use strict";var n=a("0e72"),s=a.n(n);s.a},a089:function(t,e,a){"use strict";var n=a("1778"),s=a.n(n);s.a},a434:function(t,e,a){"use strict";var n=a("23e7"),s=a("23cb"),r=a("a691"),i=a("50c4"),c=a("7b0b"),l=a("65f0"),o=a("8418"),u=a("1dde"),p=a("ae40"),f=u("splice"),d=p("splice",{ACCESSORS:!0,0:0,1:2}),v=Math.max,h=Math.min,g=9007199254740991,_="Maximum allowed length exceeded";n({target:"Array",proto:!0,forced:!f||!d},{splice:function(t,e){var a,n,u,p,f,d,m=c(this),k=i(m.length),b=s(t,k),C=arguments.length;if(0===C?a=n=0:1===C?(a=0,n=k-b):(a=C-2,n=h(v(r(e),0),k-b)),k+a-n>g)throw TypeError(_);for(u=l(m,n),p=0;p<n;p++)f=b+p,f in m&&o(u,p,m[f]);if(u.length=n,a<n){for(p=b;p<k-n;p++)f=p+n,d=p+a,f in m?m[d]=m[f]:delete m[d];for(p=k;p>k-n+a;p--)delete m[p-1]}else if(a>n)for(p=k-n;p>b;p--)f=p+n-1,d=p+a-1,f in m?m[d]=m[f]:delete m[d];for(p=0;p<a;p++)m[p+b]=arguments[p+2];return m.length=k-n+a,u}})},c009:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("router-link",{staticClass:"nlnk tag wb-a ta-c",attrs:{to:{name:"task_list",query:{tag:t.name}}}},[t._v(" "+t._s(t.name)+" ")])},s=[],r={props:{name:String}},i=r,c=(a("590c"),a("2877")),l=Object(c["a"])(i,n,s,!1,null,"7e93b490",null);e["a"]=l.exports},ceb0:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"group"},[a("vue-simplemde",{staticClass:"editor",attrs:{value:t.value,configs:t.configs,"preview-class":"markdown-body"},on:{input:function(e){return t.$emit("input",e)}}}),t.invalid?a("div",t._l(t.errors,(function(e){return a("div",{key:e,staticClass:"error"},[t._v(" "+t._s(e)+" ")])})),0):t._e()],1)},s=[],r=a("8e36"),i={props:{value:String,errors:Array},data:function(){return{configs:{autoDownloadFontAwesome:void 0,spellChecker:!1,previewRender:function(t){return r["a"].render(t)}}}},computed:{invalid:function(){return this.$types.isArray(this.errors)&&this.errors.length>0}}},c=i,l=(a("a089"),a("2877")),o=Object(l["a"])(c,n,s,!1,null,"5950a9d7",null);e["a"]=o.exports},d29f:function(t,e,a){},d784:function(t,e,a){"use strict";a("ac1f");var n=a("6eeb"),s=a("d039"),r=a("b622"),i=a("9263"),c=a("9112"),l=r("species"),o=!s((function(){var t=/./;return t.exec=function(){var t=[];return t.groups={a:"7"},t},"7"!=="".replace(t,"$<a>")})),u=function(){return"$0"==="a".replace(/./,"$0")}(),p=r("replace"),f=function(){return!!/./[p]&&""===/./[p]("a","$0")}(),d=!s((function(){var t=/(?:)/,e=t.exec;t.exec=function(){return e.apply(this,arguments)};var a="ab".split(t);return 2!==a.length||"a"!==a[0]||"b"!==a[1]}));t.exports=function(t,e,a,p){var v=r(t),h=!s((function(){var e={};return e[v]=function(){return 7},7!=""[t](e)})),g=h&&!s((function(){var e=!1,a=/a/;return"split"===t&&(a={},a.constructor={},a.constructor[l]=function(){return a},a.flags="",a[v]=/./[v]),a.exec=function(){return e=!0,null},a[v](""),!e}));if(!h||!g||"replace"===t&&(!o||!u||f)||"split"===t&&!d){var _=/./[v],m=a(v,""[t],(function(t,e,a,n,s){return e.exec===i?h&&!s?{done:!0,value:_.call(e,a,n)}:{done:!0,value:t.call(a,e,n)}:{done:!1}}),{REPLACE_KEEPS_$0:u,REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE:f}),k=m[0],b=m[1];n(String.prototype,t,k),n(RegExp.prototype,v,2==e?function(t,e){return b.call(t,this,e)}:function(t){return b.call(t,this)})}p&&c(RegExp.prototype[v],"sham",!0)}},dfb0:function(t,e,a){"use strict";var n=a("d29f"),s=a.n(n);s.a},fa64:function(t,e,a){}}]);
//# sourceMappingURL=group-contests~group-tasks.80ade5ce.js.map