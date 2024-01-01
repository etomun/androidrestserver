document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/event');
        if (response.ok) {
            const events = await response.json();
            displayEvents(events);
        } else {
            console.error('Failed to fetch events:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

function displayEvents(events) {
    const appElement = document.getElementById('app');
    const eventsList = events.map(event => `
    <div class="event-item">
      <h2>${event.name}</h2>
      <p><strong>Location:</strong> ${event.location}</p>
      <!-- Add more details or format as needed -->
    </div>
  `).join('');

    // Append events list to the app element
    appElement.innerHTML = `<div class="events">${eventsList}</div>`;
}