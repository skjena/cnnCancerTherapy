function httpGet(theURL) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;

function runRequest() {
    var theURL = "http://512e08c6.ngrok.io";
    var result = httpGet(theURL);
    console.log(result);


