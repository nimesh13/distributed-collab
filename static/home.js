// Validate form inputs
function checkForm(form){
    var elements = form.target.elements;
    var start_hour = parseInt(elements.starthour.value, 10);
    var start_min = parseInt(elements.startmin.value, 10);
    var end_hour = parseInt(elements.endhour.value, 10);
    var end_min = parseInt(elements.endmin.value, 10);

    if((start_hour < 6 || Number(start_hour) == 12) && elements.starttime.value === "AM"){
        alert("Start time is set too early");
        return false;
    }
    if(start_hour > 6 && Number(start_hour) != 12 && elements.starttime.value === "PM"){
        alert("Start time is set too late");
        return false;
    }

    if((end_hour < 6 || Number(end_hour) == 12) && elements.endtime.value === "AM"){
        alert("End time is set too early");
        return false;
    }

    if(end_hour > 6 && Number(end_hour) != 12 && elements.endtime.value === "PM"){
        alert("End time is set too late");
        return false;
    }

    if((elements.starttime.value === "PM" && elements.endtime.value === "AM")
        || Number(start_hour) == Number(end_hour) && Number(start_min) == Number(end_min) && elements.starttime.value === elements.endtime.value
        || Number(start_hour) != 12 && Number(start_hour) > Number(end_hour) && elements.starttime.value === elements.endtime.value
        || Number(end_hour) == 12 && (Number(start_hour) < 12) && elements.starttime.value === "PM"
        || Number(start_hour) == Number(end_hour) && Number(start_min) == 30){
        alert("End time must be after start time");
        return false;
    }

    return true;
}

// Load events from json file into calender ui
function addEvents(jsonString) {
     const jsonObj = JSON.parse(jsonString);
     for (var obj of jsonObj){
         var start_hour = obj.starthour;
         var end_hour = obj.endhour;
         var id = obj.day + start_hour + obj.startmin + obj.starttime;

         if(parseInt(start_hour, 10) == 12 && !(parseInt(start_hour, 10) == 12 && parseInt(end_hour, 10) == 12)){
            start_hour = "0";
         }

         if(obj.starttime === "AM" && obj.endtime === "PM" && parseInt(start_hour, 10) != 12 && parseInt(end_hour, 10) != 12){
            end_hour = parseInt(end_hour, 10) + 12;
         }

         var start = start_hour + ":" + obj.startmin + ":00";
         var end = end_hour.toString() + ":" + obj.endmin + ":00";
         var htimeStart = new Date("01/01/2007 " + start).getHours();
         var htimeEnd = new Date("01/01/2007 " + end).getHours();
         var mtimeStart = new Date("01/01/2007 " + start).getMinutes();
         var mtimeEnd = new Date("01/01/2007 " + end).getMinutes();

         var hourDiff = htimeEnd - htimeStart;
         var minDiff = mtimeEnd - mtimeStart;
         var sizemultiplier = hourDiff;
         if(minDiff < 0){
           sizemultiplier -= 0.5;
         }
         else if(minDiff > 0){
           sizemultiplier += 0.5;
         }
         var percentage = (sizemultiplier/0.5) * 100;
         var uiOffset = ((sizemultiplier/0.5) - 1) * 12.5;
         document.getElementById(id).innerHTML = '<div class="event double" style="height: ' + percentage +
         '%; top: ' + uiOffset + 'px;" ><input type="checkbox" class="checkbox" /> ' + obj.starthour +
         ':' + obj.startmin + '–' + obj.endhour + ':' + obj.endmin + ' ' + obj.title + '</div>';

     }
}