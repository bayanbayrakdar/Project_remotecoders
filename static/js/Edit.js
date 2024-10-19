//delet item 


document.addEventListener('DOMContentLoaded', () => {
    

    const delete_reservation = (event) => {

        event.preventDefault();
        localStorage.removeItem("name_patient");
        localStorage.removeItem("age_patient");
        localStorage.removeItem("day");
        localStorage.removeItem("year");
        localStorage.removeItem("month");
        localStorage.removeItem("Hour");
        localStorage.removeItem("minute")
        
        
        
        
    };

    if (delete_button) {
        delete_button.addEventListener("click", delete_reservation);
    }
    else{
        console.error("erro");
        
    }

})
function removeRow(button) {
    // Get the row containing the button
    const row = button.parentElement.parentElement;
    // Remove the row from the table
    row.remove();
}


function addRow() {
    const table = document.getElementById('outputTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow(); 

    
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    const cell3 = newRow.insertCell(2);
    const cell4 = newRow.insertCell(3);
    const cell5 = newRow.insertCell(4);
    const cell6 = newRow.insertCell(5);

    
    cell1.innerHTML = "0"; 
    cell2.innerHTML = "New Name"; 
    cell3.innerHTML = "New Age"; 
    cell4.innerHTML = "New Time"; 
    cell5.innerHTML = "New Date"; 
    cell6.innerHTML = `
        <button class="save">Save</button>
        <button class="btn btn-success" data-toggle="modal" data-target="#myModal">Edit</button>
        <button class="delete" onclick="removeRow(this)">Delete</button>
    `;
}


// document.getElementById('button').addEventListener('click', () =>{

//     const popup =document.getElementById('popup')
//     const overlay =document.getElementById('overlay')
//     popup.style.display="block"
//     overlay.style.display="block"
//     // if(popup.style.display=="none" || popup.style.display=== ""){

//     // }
//     }

// )