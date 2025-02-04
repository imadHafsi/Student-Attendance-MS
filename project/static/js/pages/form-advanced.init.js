
document.addEventListener('DOMContentLoaded', function() {

    var multiSelectHeader = document.getElementById("multiselect-header");

    multiSelectHeader && multi(multiSelectHeader, {
    non_selected_header: "All Permissions",
    selected_header: "Supplementary Permissions for User"
    });
    
 
})