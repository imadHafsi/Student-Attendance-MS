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
        var student_id = this.getAttribute('data-student_id');
        var firstname = this.getAttribute('data-firstname');
        var lastname = this.getAttribute('data-lastname');
        var dob = this.getAttribute('data-dob');
        var sex = this.getAttribute('data-sex');


        // Populate the modal fields with data
        document.getElementById('id-field').value = id;
        document.getElementById('student_id-field').value = student_id;
        document.getElementById('firstname-field').value = firstname;
        document.getElementById('lastname-field').value = lastname;
        document.getElementById('dob-field').value = dob;
        document.getElementById('sex-field').value = sex;
    });
});

document.getElementById("showModal").addEventListener("hidden.bs.modal", function () {
    document.getElementById('id-field').value = "";
    document.getElementById('student_id-field').value = "";
    document.getElementById('firstname-field').value = "";
    document.getElementById('lastname-field').value = "";
    document.getElementById('dob-field').value = "";
    document.getElementById('dob-field').setAttribute('placeholder', 'Select date');
    document.getElementById('sex-field').value = "";
});

document.getElementById("showModal").addEventListener("show.bs.modal", function(e) {
let modalTitle = document.getElementById("exampleModalLabel");
let addBtn = document.getElementById("save-btn");
let form = document.getElementById("studentForm");


if (e.relatedTarget.classList.contains("edit-item-btn")) {
    // Update scenario
    modalTitle.innerHTML = "Edit Student";
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
    modalTitle.innerHTML = "Add Student";
    addBtn.innerHTML = "Add Student";
    
    console.log(modalTitle)
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

document.getElementById("changeClassroom").addEventListener("show.bs.modal", function(e) {
    
    let modalClassroomTitle = document.getElementById("exampleModalLabelClassroom");
    let changeBtn = document.getElementById("changeclassroom-btn");
    let classform = document.getElementById("classForm");
        
    modalClassroomTitle.innerHTML = "Select Class";
    changeBtn.innerHTML = "Select Class";

    document.querySelector("input[name='studentid']").value = e.relatedTarget.getAttribute("data-id");

    var sectionField = document.getElementById('section-field');
    var groupField = document.getElementById('group-field');
    var levelField = document.getElementById('level-field')

    levelField.value = ""
    sectionField.innerHTML = ""
    groupField.innerHTML = ""

    let level = e.relatedTarget.getAttribute("data-level");
    let section = e.relatedTarget.getAttribute("data-section");
    let group = e.relatedTarget.getAttribute("data-group");

    if (level) {
        levelField.value=level
        fetch('/admin/classes/get_sections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level: level })
        })
        .then(response => response.json())
        .then(data => {
            
            sectionField.innerHTML = '<option value="">Choose Section</option>';
            data.sections.forEach(function (section) {
                var option = document.createElement('option');
                option.value = section;
                option.textContent = section;
                sectionField.appendChild(option);
            });
            sectionField.value = section
        })
        .catch(error => console.error('Error fetching sections:', error));
    }

    if (level && section) {
        fetch('/admin/classes/get_groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level: level, section: section })
        })
        .then(response => response.json())
        .then(data => {
            
            groupField.innerHTML = '<option value="">Choose Group</option>';
            data.groups.forEach(function (group) {
                var option = document.createElement('option');
                option.value = group;
                option.textContent = group;
                groupField.appendChild(option);
            });
            groupField.value = group
        })
        .catch(error => console.error('Error fetching groups:', error));
    }

    });

document.querySelectorAll('.remove-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        const userId = this.getAttribute('data-id');
        document.getElementById('delete-class-id').value = userId;
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
                console.log(data.first_name+" "+data.last_name+" "+data.email);
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

document.getElementById('level-field').addEventListener('change', function () {
    var level = this.value;
    if (level) {
        fetch('/admin/classes/get_sections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level: level })
        })
        .then(response => response.json())
        .then(data => {
            var sectionField = document.getElementById('section-field');
            sectionField.innerHTML = '<option value="">Choose Section</option>';
            data.sections.forEach(function (section) {
                var option = document.createElement('option');
                option.value = section;
                option.textContent = section;
                sectionField.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching sections:', error));
    }
});

document.getElementById('section-field').addEventListener('change', function () {
    var level = document.getElementById('level-field').value;
    var section = this.value;
    if (level && section) {
        fetch('/admin/classes/get_groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level: level, section: section })
        })
        .then(response => response.json())
        .then(data => {
            var groupField = document.getElementById('group-field');
            groupField.innerHTML = '<option value="">Choose Group</option>';
            data.groups.forEach(function (group) {
                var option = document.createElement('option');
                option.value = group;
                option.textContent = group;
                groupField.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching groups:', error));
    }
});

});
