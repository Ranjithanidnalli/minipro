// notifications.js

// Displaying a notification if a task reminder is sent
function showNotification(message) {
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.textContent = message;

    // Append the notification to the body or a specific container
    document.body.appendChild(notification);

    // Automatically remove the notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Example function to handle sending reminders (placeholder)
document.querySelectorAll('.send-sms').forEach(button => {
    button.addEventListener('click', (event) => {
        const taskId = event.target.getAttribute('data-task-id');
        sendReminder(taskId);
    });
});

function sendReminder(taskId) {
    // You could make an AJAX call to send the reminder SMS here
    fetch(`/send_sms/${taskId}`)
        .then(response => response.json())
        .then(data => {
            showNotification(`Reminder sent for task ${taskId}!`);
        })
        .catch(error => {
            showNotification(`Error sending reminder: ${error}`);
        });
}
