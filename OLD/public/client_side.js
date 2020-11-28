document.addEventListener('DOMContentLoaded', bindButtons);

function bindButtons(){
    document.getElementById('exercise_submit').addEventListener('click', function(event){
        var req = new XMLHttpRequest();
        var payload = 'http://flip3.engr.oregonstate.edu:11179/?type=insert';
        payload += "&name=" + document.getElementById('name_input').value;
        payload += "&reps=" + document.getElementById('reps_input').value;
        payload += "&weight=" + document.getElementById('weight_input').value;
        payload += "&date=" + document.getElementById('date_input').value;
        var units;
        // to handle lbs boolean result
        if (document.getElementById('lbs').checked){
            units = 1;
        } else {
            units = 0;
        }
        payload += "&lbs=" + units;

        req.open("GET", payload, true);
        // set up listener prior to send to make aync call 
        req.addEventListener('load',function(){
            if(req.status >= 200 && req.status < 400){
                var response = JSON.parse(req.responseText);
                
                // resets input form values
                document.getElementById('name_input').value = null;
                document.getElementById('reps_input').value = null;
                document.getElementById('weight_input').value = null;
                document.getElementById('date_input').value = null;
                
                // builds table from latest sql db updates
                document.getElementById('resultsP').textContent = response.results;
                buildTable(JSON.parse(response.rows));
                
            } else {
                console.log("Error in network request: " + req.statusText);
            }});
        req.send(null);
        event.preventDefault();
    })

}

document.getElementById('results_output').addEventListener('click', function(event){
    let target = event.target; // where was the click?
    // if delete button clicked
    if (target.name == 'delete') {
        // for cases where during mid-update delete was pressed, cancels record edit and deletes cell
        document.getElementById('name_input').value = null;
        document.getElementById('reps_input').value = null;
        document.getElementById('weight_input').value = null;
        document.getElementById('date_input').value = null; 
        document.getElementById("exercise_submit").removeAttribute("hidden")
        document.getElementById("updates_submit").setAttribute("hidden", true)

        // update database for removal of record
        var req = new XMLHttpRequest();
        var payload = 'http://flip3.engr.oregonstate.edu:11179/?type=delete';
        payload += "&id=" + target.id;
        
        req.open("GET", payload, true);
        // set up listener prior to send to make aync call 
        req.addEventListener('load',function(){
            if(req.status >= 200 && req.status < 400){
                var response = JSON.parse(req.responseText);
                // builds table from latest sql db updates  
                document.getElementById('resultsP').textContent = response.results;        
                buildTable(JSON.parse(response.rows));
            } else {
                console.log("Error in network request: " + req.statusText);
            }
        });
        req.send(null);
        event.preventDefault();
        
        deleteRow(target); // delete table row in UI
    
    // if update button clicked
    } else if (target.name == 'update') {
        // updates original submission form to be used as update form
        document.getElementById("exercise_submit").setAttribute("hidden", true)
        document.getElementById("updates_submit").removeAttribute("hidden")
        document.getElementById("updates_submit").name = target.id

        // sets current target records values into the update forms fields
        var cell = target.parentNode.parentNode.firstChild
        document.getElementById('name_input').value = cell.value
        cell = cell.nextSibling
        document.getElementById('reps_input').value = cell.value
        cell = cell.nextSibling
        document.getElementById('weight_input').value = cell.value
        cell = cell.nextSibling
        document.getElementById('date_input').value = cell.value
        cell = cell.nextSibling
        if (cell.textContent == "lbs") {
            document.getElementById('lbs').setAttribute("checked", true);
        } else {
            document.getElementById('kg').setAttribute("checked", true);
        }
        
        
        
    } else {
        return;
    }
});

// kicks-off listener for the 'submit update' button press
document.getElementById('updates_submit').addEventListener('click', function(event){
    // requests a record update given a target record id with newly updated values
    var req = new XMLHttpRequest();
    var payload = 'http://flip3.engr.oregonstate.edu:11179/?type=update';
    payload += "&id=" + document.getElementById('updates_submit').name;
    payload += "&name=" + document.getElementById('name_input').value;
    payload += "&reps=" + document.getElementById('reps_input').value;
    payload += "&weight=" + document.getElementById('weight_input').value;
    payload += "&date=" + document.getElementById('date_input').value;
    payload += "&lbs=" + document.getElementById('lbs').checked;
    
    req.open("GET", payload, true);
    // set up listener prior to send to make aync call 
    req.addEventListener('load',function(){
        if(req.status >= 200 && req.status < 400){
            var response = JSON.parse(req.responseText);
            // builds table from latest sql db updates
            document.getElementById('resultsP').textContent = response.results;          
            buildTable(JSON.parse(response.rows));
        } else {
            console.log("Error in network request: " + req.statusText);
        }
    });
    
    req.send(null);
    event.preventDefault();

    // once update is complete, swaps update form back into submission form
    document.getElementById('name_input').value = null;
    document.getElementById('reps_input').value = null;
    document.getElementById('weight_input').value = null;
    document.getElementById('date_input').value = null;            
    document.getElementById("exercise_submit").removeAttribute("hidden")
    document.getElementById("updates_submit").setAttribute("hidden", true)
})


// used for deleting row from table UI
function deleteRow(button) {
    try {
        var row = button.parentNode.parentNode;
        row.parentNode.removeChild(row)
    } catch (e) {
        alert(e);
    }
    //getValues();
}

// used for building table UI
function buildTable(rows){
    // Create new Table Node on each query pull
    element = document.getElementById("results_table");
    element.parentNode.removeChild(element);
    var table = document.createElement("table");
    table.id = "results_table"
    document.getElementById("results_output").appendChild(table);

    // Create Caption Node
    var captionNode = document.createElement("caption");
    captionNode.textContent = "Tracked Exercises";
    table.appendChild(captionNode);

    // Create thead node
    var headerNode = document.createElement("thead");
    table.appendChild(headerNode);
        // Create TR
        var rowNode = document.createElement("tr");
        headerNode.appendChild(rowNode);
            // Create Header Cells
            var newCell = document.createElement("th");
            newCell.textContent = "Name";
            headerNode.appendChild(newCell);

            var newCell = document.createElement("th");
            newCell.textContent = "Reps";
            headerNode.appendChild(newCell);

            var newCell = document.createElement("th");
            newCell.textContent = "Weight";
            headerNode.appendChild(newCell);

            var newCell = document.createElement("th");
            newCell.textContent = "Date";
            headerNode.appendChild(newCell);

            var newCell = document.createElement("th");
            newCell.textContent = "Units";
            headerNode.appendChild(newCell);

    // Create tbody node
    var bodyNode = document.createElement("tbody");
    table.appendChild(bodyNode);
        // Creates each rows
        for (var row = 0; row < rows.length; row++){
            // Create TR node
            var rowNode = document.createElement("tr");
            //rowNode.id = rows[row].id;
            bodyNode.appendChild(rowNode);
                // Create Table Cells
                var newCell = document.createElement("td");
                newCell.name = "name";
                newCell.value = rows[row].name;
                newCell.textContent = rows[row].name;
                rowNode.appendChild(newCell);

                var newCell = document.createElement("td");
                newCell.name = "reps";
                newCell.value = rows[row].reps;
                newCell.textContent = rows[row].reps;
                rowNode.appendChild(newCell);

                var newCell = document.createElement("td");
                newCell.name = "weight";
                newCell.value = rows[row].weight;
                newCell.textContent = rows[row].weight;
                rowNode.appendChild(newCell);

                var newCell = document.createElement("td");
                newCell.name = "date";
                newCell.value = rows[row].date.slice(0,10);
                newCell.textContent = rows[row].date.slice(0,10);
                rowNode.appendChild(newCell);

                var newCell = document.createElement("td");
                newCell.name = "units";
                var units;
                if (rows[row].lbs) {
                    units = "lbs"
                } else {
                    units = "kg"
                }
                newCell.textContent = units;
                rowNode.appendChild(newCell);

                var newCell = document.createElement("td");
                newCell.name = "delete";
                rowNode.appendChild(newCell);

                var newButton = document.createElement("button");
                newCell.appendChild(newButton);
                newButton.textContent = "update";
                newButton.name = "update"
                newButton.id = rows[row].id;
                
                var newCell = document.createElement("td");
                newCell.name = "delete";
                rowNode.appendChild(newCell);

                var newButton = document.createElement("button");
                newCell.appendChild(newButton);
                newButton.textContent = "delete";
                newButton.name = "delete"
                newButton.id = rows[row].id;
            }
        
    generateBorder("table")
    generateBorder("tr")
}

// Style table
function generateBorder(tagName){
    var elements = document.getElementsByTagName(tagName)
    for(var i = elements.length - 1; i >= 0; i--){
        elements[i].style.borderStyle = "solid";
    }
}

// for reset table button press - sends get reqeuest to reset-table page but does not load anything
document.getElementById('reset_table').addEventListener('click', function(event){
    var req = new XMLHttpRequest();
    var payload = 'http://flip3.engr.oregonstate.edu:11179/?type=reset'
    req.open("GET", payload, true);
    // set up listener prior to send to make aync call 
    req.addEventListener('load',function(){
        if(req.status >= 200 && req.status < 400){
            var response = JSON.parse(req.responseText);
            
            // resets input form values
            document.getElementById('name_input').value = null;
            document.getElementById('reps_input').value = null;
            document.getElementById('weight_input').value = null;
            document.getElementById('date_input').value = null;
            
            // builds table from latest sql db updates
            document.getElementById('resultsP').textContent = response.results;
            buildTable(JSON.parse(response.rows));
        } else {
            console.log("Error in network request: " + req.statusText);
        }});
    req.send(null);
    event.preventDefault();

})