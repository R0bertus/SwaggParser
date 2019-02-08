
function parsev1() {
    var d = {};
    a = document.getElementsByTagName("a");
    for (var k of a) {
        if ( k.getAttribute("class") == "toggleOperation") {
            if(k.firstElementChild != null &&
               k.firstElementChild.getAttribute("class") == "markdown") {

            } else {
                if(-1 < k.parentElement.nextElementSibling.innerText.indexOf("/")) {
                    if( !(k.parentElement.nextElementSibling.innerText in d) ) {
                        d[k.parentElement.nextElementSibling.innerText] = {};
                    }
                    d[k.parentElement.nextElementSibling.innerText][k.innerText] = {};
                    divs = k.parentNode.parentNode.parentNode.nextElementSibling.getElementsByTagName("div")
                    for (var div of divs) {
                        if(div.getAttribute("class") == "response-class") {
                            code = div.getElementsByTagName("code")
                            if(0 < code.length) {
                                d[k.parentElement.nextElementSibling.innerText][k.innerText]["response"] = {"type": "json", "value": code[0].innerText};
                            } else {
                                d[k.parentElement.nextElementSibling.innerText][k.innerText]["response"] = {"type": div.getElementsByTagName("p")[0].innerText, "value": null};
                            }
                        }
                    }
                    tbody = k.parentNode.parentNode.parentNode.nextElementSibling.getElementsByTagName("tbody")[0]
                    d[k.parentElement.nextElementSibling.innerText][k.innerText]["request"] = {
                        "params": []
                    }
                    if(tbody != null) {
                        trs = tbody.getElementsByTagName("tr");
                        for (var tr of trs) {
                            d[k.parentElement.nextElementSibling.innerText][k.innerText]["request"]["params"].push({
                                "param": 0 < tr.getElementsByTagName("code").length ? tr.getElementsByTagName("code")[0].innerText : tr.getElementsByTagName("td")[4].innerText,
                                "name": tr.getElementsByTagName("td")[0].innerText,
                                "type": tr.getElementsByTagName("td")[3].innerText
                            });
                        }
                    }
                }
            }
        }
    }
    console.log(JSON.stringify(d))
}


function parsev2() {
    var d = {};
    a = document.getElementsByTagName("a");
    for (var k of a) {
        if ( k.getAttribute("class") == "toggleOperation") {
            if(k.firstElementChild != null &&
               k.firstElementChild.getAttribute("class") == "markdown") {

            } else {
                if(-1 < k.parentElement.nextElementSibling.innerText.indexOf("/")) {
                    if( !(k.parentElement.nextElementSibling.innerText in d) ) {
                        d[k.parentElement.nextElementSibling.innerText] = {};
                    }
                    d[k.parentElement.nextElementSibling.innerText][k.innerText] = {};
                    divs = k.parentNode.parentNode.parentNode.nextElementSibling.getElementsByTagName("div")
                    for (var div of divs) {
                        if(div.getAttribute("class") == "response-class") {
                            code = div.getElementsByTagName("code")
                            if(0 < code.length) {
                                d[k.parentElement.nextElementSibling.innerText][k.innerText]["response"] = {"type": "json", "value": code[0].innerText};
                            } else {
                                d[k.parentElement.nextElementSibling.innerText][k.innerText]["response"] = {"type": div.getElementsByTagName("p")[0].innerText, "value": null};
                            }
                        }
                    }
                    tbody = k.parentNode.parentNode.parentNode.nextElementSibling.getElementsByTagName("tbody")[0]
                    d[k.parentElement.nextElementSibling.innerText][k.innerText]["request"] = {
                        "params": []
                    }
                    if(tbody != null) {
                        trs = tbody.getElementsByTagName("tr");
                        for (var tr of trs) {
                            d[k.parentElement.nextElementSibling.innerText][k.innerText]["request"]["params"].push({
                                "param": 0 < tr.getElementsByTagName("code").length ? tr.getElementsByTagName("code")[0].innerText : tr.getElementsByTagName("td")[4].innerText,
                                "name": tr.getElementsByTagName("td")[0].innerText,
                                "type": tr.getElementsByTagName("td")[3].innerText
                            });
                        }
                    }
                }
            }
        }
    }
    console.log(JSON.stringify(d))
}



function toggle() {
    var fireEvent = function(element,event){
        if (document.createEventObject){
            var evt = document.createEventObject();
            return element.fireEvent('on'+event,evt)
        }
        else {
            var evt = document.createEvent("HTMLEvents");
            evt.initEvent(event, true, true );
            return !element.dispatchEvent(evt);
        }
    }

    var swaggerv2 = false;
    a = document.getElementsByTagName("a");
    for (var k of a) {
        if (k.getAttribute("class") == "nostyle") {
            k.click();
            swaggerv2 = true;
        }
        else if(k.getAttribute("class") == "expandResource") {
            k.click();
        }
    }
    if(swaggerv2) {
        a = document.getElementsByTagName("a");
        for (var k of a) {
            if (k.getAttribute("class") == "nostyle") {
                k.click();
            }
        }

        setTimeout(function() {
            selects = document.getElementsByTagName("select");
            for (var select of selects) {
                try {
                    select.addEventListener('click', function (e) {
                        select.value = "application/json";
                        fireEvent(select, 'change')
                    });
                    select.click()
                } catch(e) {}
            }
        }, 10000)
    }
}
toggle();




function toggle() {
    var fireEvent = function(element,event){
        if (document.createEventObject){
            var evt = document.createEventObject();
            return element.fireEvent('on'+event,evt)
        }
        else {
            var evt = document.createEvent("HTMLEvents");
            evt.initEvent(event, true, true );
            return !element.dispatchEvent(evt);
        }
    }

    var swaggerv2 = false;
    a = document.getElementsByTagName("a");
    for (var k of a) {
        if (k.getAttribute("class") == "nostyle") {
            k.click();
            swaggerv2 = true;
        }
        else if(k.getAttribute("class") == "expandResource") {
            k.click();
        }
    }
    if(swaggerv2) {

        a = document.getElementsByTagName("a");
        for (var k of a) {
            if (k.getAttribute("class") == "nostyle") {
                k.click();
            }
        }

        setTimeout(function() {
            selects = document.getElementsByTagName("select");
            for (var select of selects) {
                try {
                    select.addEventListener('click', function (e) {
                        select.value = "application/json";
                        fireEvent(select, 'change')
                    });
                    select.click()
                } catch(e) {}
            }
            divs = document.getElementsByTagName("div");
            for (var k of divs) {
                if (k.getAttribute("class") == "opblock opblock-deprecated") {
                    k.remove()
                }
            }
        }, 3200)
	}
}
toggle();



