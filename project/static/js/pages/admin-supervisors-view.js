new DataTable("#ajax-datatables2",{
    //ajax: "{{ url_for('admin.view_users') }}",
    dom: "Bfrtip",
    buttons: ["copy", "csv", "excel", "print", "pdf"]
});


document.addEventListener('DOMContentLoaded', function() {
// Add click event listener to all edit buttons
document.querySelectorAll('.edit-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        // Get data attributes from the clicked button

        

        var id = this.getAttribute('data-id');
        var supervisor_id = this.getAttribute('data-supervisor_id');
        var firstname = this.getAttribute('data-firstname');
        var lastname = this.getAttribute('data-lastname');
        var dob = this.getAttribute('data-dob');
        var sex = this.getAttribute('data-sex');

        
        // Populate the modal fields with data
        document.getElementById('id-field').value = id;
        document.getElementById('supervisor_id-field').value = supervisor_id;
        document.getElementById('firstname-field').value = firstname;
        document.getElementById('lastname-field').value = lastname;
        document.getElementById('sex-field').value = sex;

        let dobField = document.getElementById('dob-field');
        let flatpickrInstance = flatpickr(dobField, {
            dateFormat: "Y-m-d",  // Ensure format matches Flask-WTF's expected format
            altInput: true,
            altFormat: "d M, Y",  // Human-readable format
            allowInput: true
        });

        // Convert the date format before populating the modal
          // Set Flatpickr date if DOB exists
        if (dob) {
            let parsedDate = new Date(dob);
            flatpickrInstance.setDate(parsedDate, true); // Update Flatpickr with the correct date
        } else {
            flatpickrInstance.clear(); // Clear the field if no date is available
        }

    });
});

document.getElementById("showModal").addEventListener("hidden.bs.modal", function () {
    document.getElementById('id-field').value = "";
        document.getElementById('supervisor_id-field').value = "";
        document.getElementById('firstname-field').value = "";
        document.getElementById('lastname-field').value = "";
        document.getElementById('sex-field').value = "";

        let dobField = document.getElementById('dob-field');
        let flatpickrInstance = flatpickr(dobField, {
            dateFormat: "Y-m-d",  // Ensure format matches Flask-WTF's expected format
            altInput: true,
            altFormat: "d M, Y",  // Human-readable format
            allowInput: true
        });

        flatpickrInstance.clear();

});

document.getElementById("showModal").addEventListener("show.bs.modal", function(e) {
let modalTitle = document.getElementById("exampleModalLabel");
let addBtn = document.getElementById("save-btn");
let form = document.getElementById("supervisorForm");

if (e.relatedTarget.classList.contains("edit-item-btn")) {
    // Update scenario
    modalTitle.innerHTML = "Edit Supervisor";
    addBtn.innerHTML = "Update";

    // Populate form fields with the selected user's data
    document.querySelector("input[name='id']").value = e.relatedTarget.getAttribute("data-id");
    form.supervisor_id.value = e.relatedTarget.getAttribute("data-supervisor_id");
    form.firstname.value = e.relatedTarget.getAttribute("data-firstname");
    form.lastname.value = e.relatedTarget.getAttribute("data-lastname");
    form.dob.value = e.relatedTarget.getAttribute("data-dob");
    form.sex.value = e.relatedTarget.getAttribute("data-sex");

} else if (e.relatedTarget.classList.contains("add-btn")) {
    // Add scenario
    modalTitle.innerHTML = "Add Supervisor";
    addBtn.innerHTML = "Add Supervisor";

    // Clear form fields
    form.supervisor_id.value = "";
    form.firstname.value = "";
    form.lastname.value = "";
    form.dob.value = "";
    form.sex.value = "";

}
});

document.querySelectorAll('.remove-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        const userId = this.getAttribute('data-id');
        document.getElementById('delete-class-id').value = userId;
    });
});

// view user details in the card

// document.querySelectorAll('.view-user-details').forEach(button => {
//     button.addEventListener('click', function(event) {
//         event.preventDefault();
//         const userId = this.getAttribute('data-id');
        
//         // Send AJAX request to get user details
//         fetch(`user/${userId}/details`)
//             .then(response => response.json())
//             .then(data => {
//                 // Populate the detail view with the user data
//                 console.log(data.first_name+" "+data.last_name);
//                 document.getElementById('user-view-detail-avatar').src = data.avatar;
//                 document.getElementById('user-view-detail-fullname').textContent = data.first_name || "N/A" +" "+data.last_name || "N/A";
//                 document.getElementById('user-view-detail-email').textContent = data.email;
//                 document.getElementById('user-view-detail-phone').textContent = data.phone;
//                 document.getElementById('user-view-detail-role').textContent = data.role;


//                 if (data.status == 'Active'){
//                     document.getElementById('user-view-detail-status').innerHTML = '<span class="badge bg-success-subtle text-success text-uppercase" >'+data.status+'</span>'
//                 }
//                 else{
//                     document.getElementById('user-view-detail-status').innerHTML = '<span class="badge bg-danger-subtle text-danger text-uppercase" >'+data.status+'</span>'
//                 }

//                 let permissionsHTML = '' ;  // Initialize an empty string to hold the HTML

//                 for (let permission of data.role_permissions) {
//                     if (!data.denied_permissions.includes(permission)) {  
//                         permissionsHTML += '<span class="badge bg-success-subtle text-success text-uppercase">' + permission + '</span>';
//                     }
//                     else{
//                         permissionsHTML += '<span class="badge bg-danger-subtle text-danger text-uppercase">' + permission + '</span>';
//                     }
//                 } 

//                 document.getElementById('user-view-detail-role-permissions').innerHTML = permissionsHTML;  // Set the accumulated HTML

//                 let suppPermissionsHTML = '' ;  // Initialize an empty string to hold the HTML

//                 for (let permission of data.ind_permissions) {
//                         suppPermissionsHTML += '<span class="badge bg-success-subtle text-success text-uppercase">' + permission + '</span>';
//                 } 

//                 document.getElementById('user-view-detail-supp-permissions').innerHTML = suppPermissionsHTML;  // Set the accumulated HTML
                
//                 // Handle permissions or other fields as needed
//             });
//     });
// });
 });
