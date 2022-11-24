var selected = null;
var jsonObjects;

// Select or deselect html element
function setSelected(item){
    var eventStr = item.getAttribute('name') + item.getAttribute('value');

    if(selected){
        selected.style.backgroundColor = "#6D56AC";
        selected.style.color = "white";
        selected.style.fontWeight = "normal";
    }

    if(selected && (selected.getAttribute('name') + selected.getAttribute('value')) === eventStr){
        selected = null;
        document.getElementById("delete_button").disabled = true;
        return false;
    }

    selected = item;
    document.getElementById("delete_button").disabled = false;
    selected.style.backgroundColor = "#FFB146";
    selected.style.color = "black";
    selected.style.fontWeight = "bold";
}

// Load events from json file into calender ui
function addEvents(jsonString) {
     const jsonObjects = JSON.parse(jsonString);
     for (var obj of jsonObjects){
         var id = 'Nov' + obj.day;
         document.getElementById(id).innerHTML += '<div class = "event double" ' +
         'style="height: 27px; padding: 2px 5px;"  name="' + obj.day +
         '" value="' + obj.title + '" onclick="setSelected(this)">' + obj.title + '</div>';
     }
}

// Remove selected event
function removeEvent() {

    data = '{"day": "' + selected.getAttribute('name') + '", "title": "' +
    selected.getAttribute('value') + '"}';
    document.getElementById("delete_button").value = data;
}