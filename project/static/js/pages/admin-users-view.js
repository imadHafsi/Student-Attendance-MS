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
        var username = this.getAttribute('data-username');
        var email = this.getAttribute('data-email');
        var dob = this.getAttribute('data-dob');
        var role = this.getAttribute('data-role');
        var phone = this.getAttribute('data-phone');
        var status = this.getAttribute('data-status');

        // Populate the modal fields with data
        document.getElementById('id-field').value = id;
        document.getElementById('username-field').value = username;
        document.getElementById('email-field').value = email;
        document.getElementById('dob-field').value = dob;
        document.getElementById('role-field').value = role;
        document.getElementById('phone-field').value = phone;
        document.getElementById('status-field').value = status;
    });
});

document.getElementById("showModal").addEventListener("hidden.bs.modal", function () {
    document.getElementById('id-field').value = "";
    document.getElementById('username-field').value = "";
    document.getElementById('email-field').value = "";
    document.getElementById('dob-field').value = "";
    document.getElementById('role-field').value = "";
    document.getElementById('phone-field').value = "";
    document.getElementById('status-field').value = "";
});

document.getElementById("showModal").addEventListener("show.bs.modal", function(e) {
let modalTitle = document.getElementById("exampleModalLabel");
let addBtn = document.getElementById("save-btn");
let form = document.getElementById("userForm");

if (e.relatedTarget.classList.contains("edit-item-btn")) {
    // Update scenario
    modalTitle.innerHTML = "Edit User";
    addBtn.innerHTML = "Update";

    // Populate form fields with the selected user's data
    document.querySelector("input[name='id']").value = e.relatedTarget.getAttribute("data-id");
    form.username.value = e.relatedTarget.getAttribute("data-username");
    form.email.value = e.relatedTarget.getAttribute("data-email");
    form.date_of_birth.value = e.relatedTarget.getAttribute("data-dob");
    form.role.value = e.relatedTarget.getAttribute("data-role");
    form.phone_number.value = e.relatedTarget.getAttribute("data-phone");
    form.status.value = e.relatedTarget.getAttribute("data-status");

} else if (e.relatedTarget.classList.contains("add-btn")) {
    // Add scenario
    modalTitle.innerHTML = "Add User";
    addBtn.innerHTML = "Add User";

    // Clear form fields
    form.id.value = "";
    form.username.value = "";
    form.email.value = "";
    form.date_of_birth.value = "";
    form.role.value = "";
    form.phone_number.value = "";
    form.status.value = "";

}
});

document.querySelectorAll('.remove-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        const userId = this.getAttribute('data-id');
        document.getElementById('delete-user-id').value = userId;
    });
});

// view user details in the card

document.querySelectorAll('.view-user-details').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const userId = this.getAttribute('data-id');
        
        // Send AJAX request to get user details
        fetch(`user/${userId}/details`)
            .then(response => response.json())
            .then(data => {
                // Populate the detail view with the user data
                console.log(data.first_name+" "+data.last_name);
                document.getElementById('user-view-detail-avatar').src = data.avatar;
                document.getElementById('user-view-detail-fullname').textContent = data.first_name || "N/A" +" "+data.last_name || "N/A";
                document.getElementById('user-view-detail-email').textContent = data.email;
                document.getElementById('user-view-detail-phone').textContent = data.phone;
                document.getElementById('user-view-detail-role').textContent = data.role;


                if (data.status == 'Active'){
                    document.getElementById('user-view-detail-status').innerHTML = '<span class="badge bg-success-subtle text-success text-uppercase" >'+data.status+'</span>'
                }
                else{
                    document.getElementById('user-view-detail-status').innerHTML = '<span class="badge bg-danger-subtle text-danger text-uppercase" >'+data.status+'</span>'
                }

                let permissionsHTML = '' ;  // Initialize an empty string to hold the HTML

                for (let permission of data.role_permissions) {
                    if (!data.denied_permissions.includes(permission)) {  
                        permissionsHTML += '<span class="badge bg-success-subtle text-success text-uppercase">' + permission + '</span>';
                    }
                    else{
                        permissionsHTML += '<span class="badge bg-danger-subtle text-danger text-uppercase">' + permission + '</span>';
                    }
                } 

                document.getElementById('user-view-detail-role-permissions').innerHTML = permissionsHTML;  // Set the accumulated HTML

                let suppPermissionsHTML = '' ;  // Initialize an empty string to hold the HTML

                for (let permission of data.ind_permissions) {
                        suppPermissionsHTML += '<span class="badge bg-success-subtle text-success text-uppercase">' + permission + '</span>';
                } 

                document.getElementById('user-view-detail-supp-permissions').innerHTML = suppPermissionsHTML;  // Set the accumulated HTML
                
                // Handle permissions or other fields as needed
            });
    });
});
});
