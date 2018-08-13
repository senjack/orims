/*
This is a  custom Javascript code for orims app.
Developed by Afrodjango initiative.
All rights reserved @AfroDjango initiative
*/

var test_connectivity = function(){
	alert("Am alive");
}

function orimsShowOne(a){
   	a.style.display = 'block';
}
function orimsHideOne(a){
    a.style.display = 'none';
}

function orimsCollapseOne(a){
	var b;
	b = document.getElementById(a);
    if(b.style.display == 'block'){
        orimsHideOne(b);
    }
    else{
        orimsShowOne(b);
    }
}

function orimsShowOneOfAll(e,es){
    var c;
    var d=0;
    c = document.getElementByClass(es);
    for(d;d<c.length;d++){
        c[d].style.display = 'none';
    }
	orimsShowOne(e);
}