var d = {};
a = document.getElementsByTagName("a");
for (var k of a) {
    if (k.getAttribute("class") == "nostyle") {
        if(-1 < k.firstElementChild.innerHTML.indexOf("/")) {
			if( !(k.firstElementChild.innerText in d) ) {
				d[k.firstElementChild.innerText] = {};
            }
			d[k.firstElementChild.innerText][k.parentElement.parentElement.firstElementChild.innerText] = {};
		}
    }
}


console.log(d)