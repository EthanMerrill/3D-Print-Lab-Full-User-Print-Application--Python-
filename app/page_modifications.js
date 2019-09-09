//First wipe the page
element = document.getElementsByClassName("theme-name-dremel")[0];
element.parentNode.removeChild(element);
//<input type="button" class = "btn" value = "test" onclick="window.location.href="https://google.com'"></input>
newDiv.innerHTML = '<input type="button" value = "test" onclick="window.location.href=\'https://google.com\'></input>';
//find the parent element
//var parentDiv = document.getElementsByTagName("script")[0];
//create the new node to insert
var newDiv = document.createElement('div');
//set the id and content
newDiv.id = "button";
//<input onclick="$('.apps-block').data('file-id',1810790)" type="button" class="btn  blue slicer-blue slicer share-1810790 tooltipstered" value="SLICE" data-model_id="1810790"></input>
newDiv.innerHTML = '<input type="button" class="btn"> Log Out </input>';

//newDiv.appendChild(newContent)

var sp2 = document.getElementById("main-block");
document.getElementsByTagName("script")[0].insertBefore(newDiv, document.getElementsByTagName("script")[0]);


///Ripped straight from the MDN Docs

document.body.onload = addElement;

function addElement() {
    // create a new div element 
    var newDiv = document.createElement("div");
    // and give it some content 
    var newContent = document.createTextNode("Hi there and greetings!");
    // add the text node to the newly created div
    newDiv.appendChild(newContent);

    // add the newly created element and its content into the DOM 
    var currentDiv = document.getElementById("div1");
    document.body.insertBefore(newDiv, currentDiv);
}