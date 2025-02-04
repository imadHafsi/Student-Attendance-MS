document.addEventListener('DOMContentLoaded', function () {

    // Handle flash messages
    const messages = JSON.parse(document.getElementById('flash-messages-data').textContent);
    if (messages.length > 0) {
        messages.forEach(({ category, message }) => {
            const messageData = getMessageData(category, message);
            if (messageData) {

                showMessage(messageData);
            }
        });
    }

    // Function to get message data based on category
    function getMessageData(category, message) {
        let title, lordicon, messageContent;

        switch (category) {
            case 'success':
                title = '<h4>Well done!</h4>';
                lordicon = '<lord-icon src="https://cdn.lordicon.com/lupuorrc.json" trigger="loop" colors="primary:#0ab39c,secondary:#405189" style="width:120px;height:120px"></lord-icon>';
                messageContent = `Aww yeah, ${message}`;
                break;
            case 'danger':
                title = '<h4>Oops...! Something went wrong!</h4>';
                lordicon = '<lord-icon src="https://cdn.lordicon.com/tdrtiskw.json" trigger="loop" colors="primary:#f06548,secondary:#f7b84b" style="width:120px;height:120px"></lord-icon>';
                messageContent = message;
                break;
            default:
                return null;
        }

        return { title, lordicon, messageContent, category };
    }

    // Function to display the message using SweetAlert2
    function showMessage({ title, lordicon, messageContent, category }) {
        Swal.fire({
            html: `
                <div class="mt-3">
                    ${lordicon}
                    <div class="mt-4 pt-2 fs-15">
                        ${title}
                        <p class="text-muted mx-4 mb-0">${messageContent}</p>
                    </div>
                </div>
            `,
            showCancelButton: true,
            showConfirmButton: false,
             customClass: {
        cancelButton: 'btn btn-' + category + ' w-xs mb-1',
    },
            cancelButtonText: 'Back',
            buttonsStyling: false,
            showCloseButton: true
        });
    }
});
