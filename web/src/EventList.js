import React, {useEffect, useState} from 'react';

const EventList = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/event/');
                const data = await response.json();
                setEvents(data);
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        fetchEvents();
    }, []); // Empty dependency array means this effect runs once when the component mounts

    return (
        <div>
            <h2>List of Events</h2>
            <ul>
                {events.map((event) => (
                    <li key={event.id}>{event.name}</li>
                    // Adjust the properties based on your event model
                ))}
            </ul>
        </div>
    );
};

export default EventList;