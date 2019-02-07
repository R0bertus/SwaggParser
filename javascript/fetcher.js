
function swaggerify() {
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
    return d;
}

function expand() {
    a = document.getElementsByTagName("a");
    for (var k of a) {
        if (k.getAttribute("class") == "nostyle") {
            k.click();
        }
        else if(k.getAttribute("class") == "expandResource") {
            k.click();
        }
    }
}