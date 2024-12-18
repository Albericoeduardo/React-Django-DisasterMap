import React, { useState, useEffect} from 'react';

import ApiService from '../Services/ApiService';
import FetchClient from '../ServiceClients/FetchClient';

const EventList = () => {
  const [eventsList, setEventList] = useState([]);
  const [filters, setFilters] = useState({
    country: '',
    category: '',
    start_date: '',
    end_date: '',
  });

  useEffect(() => {
    const apiService = new ApiService(FetchClient);

    const fetchEvents = async () => {
      try {
        var url = 'http://127.0.0.1:8000/api/v1/events';
        const params = [];

        if (filters.country) params.push(`country=${filters.country}`);
        if (filters.category) params.push(`category=${filters.category}`);
        if (filters.start_date) params.push(`start_date=${filters.start_date}`);
        if (filters.end_date) params.push(`end_date=${filters.end_date}`);

        if (params.length > 0) url += `?${params.join('&')}`;

        const eventsList = await apiService.getEvents(url);
        setEventList(eventsList);     
      } catch (error) {
        console.log(error);
      }
    }

    fetchEvents();
  }, [filters])

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value
    }));
  }

  return (
    <div>
      <h1>Events:</h1>
      <input
        type="text"
        name='country'
        onChange={handleFilterChange}
        placeholder='Filter by country'
      />
      <input
        type="text"
        name='category'
        onChange={handleFilterChange}
        placeholder='Filter by category'
      />
      <input
        type="text"
        name='start_date'
        onChange={handleFilterChange}
        placeholder='Set the start date'
      />
      <input
        type="text"
        name='end_date'
        onChange={handleFilterChange}
        placeholder='Set the end date'
      />
      {eventsList.map((event, index) => (
        <div key={index}>
          <h4>{event.id}:</h4>
          <p>{event.title}</p>
          <p>{event.country}</p>
          <p>{event.category.name}</p>
          <p>{event.date}</p>
        </div>
      ))}
    </div>
  )
}

export default EventList