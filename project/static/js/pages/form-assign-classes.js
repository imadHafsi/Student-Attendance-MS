
document.addEventListener('DOMContentLoaded', function() {

document.getElementById("assignClasses").addEventListener("hidden.bs.modal", function() {
    
    existingWrapper = document.getElementById("multi-container").querySelector('.multi-wrapper');
    if (existingWrapper) {
        existingWrapper.remove();
    }

    // Remove the existing select element if it exists
    existingSelect = document.getElementById('multiselect-optiongroup');
    if (existingSelect) {
        existingSelect.remove();
    }
});

document.getElementById("assignClasses").addEventListener("show.bs.modal", function(e) {

    let modalClassroomTitle = document.getElementById("exampleModalLabelClassroom");
    let changeBtn = document.getElementById("assignClasses-btn");
    let role  =''

    if (e.relatedTarget.classList.contains("assign-teacher-classes")){
        modalClassroomTitle.innerHTML = "Asign Classes to Teacher";
        role='teacher'
    }
    else if (e.relatedTarget.classList.contains("assign-supervisor-classes")){
        modalClassroomTitle.innerHTML = "Asign Classes to Supervisor";
        role='supervisor'
    }
    
    changeBtn.innerHTML = "Asign Classes";

    
    document.getElementById("tid").value = e.relatedTarget.getAttribute("data-id");
    
    
    id = e.relatedTarget.getAttribute("data-id");

    mydata={
        id:id,
        role:role
    }


    fetch('/admin/classes/get_classes_to_assign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mydata)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }

         // Create a new <select> element
         const newSelect = document.createElement("select");
         newSelect.id = "multiselect-optiongroup";
         newSelect.name = "classes";
         newSelect.multiple = true;
         newSelect.classList.add("form-control"); // Ensure styling remains intact

         // Append the new select to the container
         document.getElementById("multi-container").appendChild(newSelect);

        let groupedClasses = {};
        data.classes.forEach(cls => {
            if (!groupedClasses[cls.level]) {
                groupedClasses[cls.level] = [];
            }
            groupedClasses[cls.level].push(cls);
        });

        for (let level in groupedClasses) {
            let optgroup = document.createElement('optgroup');
            optgroup.label = `Level ${level}`;

            groupedClasses[level].forEach(cls => {
                let option = document.createElement('option');
                option.value = cls.id;
                option.textContent = `${cls.level} - ${cls.section} Group ${cls.group}`;
                if (cls.selected) {
                    option.selected = true;
                }
                optgroup.appendChild(option);
                
            });

            newSelect.appendChild(optgroup);
        }

        multi(newSelect, {
            enable_search: true
        });

    })
    .catch(error => {
        console.error('Error fetching classes:', error);
    });

});
});
