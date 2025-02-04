function confirmAction(formId, message, confirmButtonText = 'Yes, Do It!', cancelButtonText = 'Cancel') {
    Swal.fire({
        html: '<div class="mt-3">' +
            '<lord-icon src="https://cdn.lordicon.com/gsqxdxog.json" trigger="loop" colors="primary:#f7b84b,secondary:#f06548" style="width:100px;height:100px"></lord-icon>' +
            '<div class="mt-4 pt-2 fs-15 mx-5">' +
            `<h4>Are you Sure?</h4>` +
            `<p class="text-muted mx-4 mb-0">${message}</p>` +
            '</div>' +
            '</div>',
        showCancelButton: true,
        confirmButtonClass: 'btn btn-primary w-xs me-2 mb-1',
        confirmButtonText: confirmButtonText,
        cancelButtonClass: 'btn btn-danger w-xs mb-1',
        buttonsStyling: false,
        showCloseButton: true,
        preConfirm: () => {
            // Submit the form with the given ID
            document.getElementById(formId).submit();
        }
    });
}

// Example usage:
// Assuming you have a button with id 'custom-sa-warning' that triggers the confirmation for a form with id 'delete-account-form'
document.getElementById("custom-sa-warning-delete-account").addEventListener("click", function () {
    confirmAction('delete-account-form', 'Are you sure you want to delete this account? This action cannot be undone.');
});
