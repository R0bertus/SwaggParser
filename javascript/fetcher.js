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



