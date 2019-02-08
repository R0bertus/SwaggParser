function toggle() {
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


function fireEvent(element,event){
    if (document.createEventObject){
        var evt = document.createEventObject();
        return element.fireEvent('on'+event,evt);
    }
    else {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent(event, true, true );
        return !element.dispatchEvent(evt);
    }
}

function change_branch(text) {
    document.getElementById("select").addEventListener('click', function (e) {
        document.getElementById("select").value = text;
        fireEvent(select, 'change');
    });
    document.getElementById("select").click();
}