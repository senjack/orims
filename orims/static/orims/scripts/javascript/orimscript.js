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
	var b = document.getElementById(a);
	var c = b.style.display;
    if(c == 'block' || c == 'inline-block'){
        orimsHideOne(b);
    }
    else{
        orimsShowOne(b);
    }

}

function orimsShowOneOfAll(e,es){
	orimsShowOne(e);
}

function toggle_content(a,b){
	var c,d;
	 c = document.getElementById(a);
	 d = document.getElementById(b);
    if(d.style.display == 'block'){
        orimsHideOne(d);
        orimsShowOne(c);
    }
    else{
        orimsHideOne(c);
        orimsShowOne(d);
    }
    return
}