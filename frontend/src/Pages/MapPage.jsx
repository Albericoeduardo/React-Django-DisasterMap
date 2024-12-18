"use client";

import React, { useState, useEffect} from 'react';

import ApiService from '../Services/ApiService';
import FetchClient from '../ServiceClients/FetchClient';
import {
    MapContainer,
    TileLayer,
    Marker,
    Popup
  } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import FireEvent from '../Components/FireEvent';
import WaterEvent from '../Components/WaterEvent';
import VolcanoEvent from '../Components/VolcanoEvent';
import SevereStorms from '../Components/SevereStorms';

const MapPage = () => {
  const [categoryList, setCategoryList] = useState([]);
  const [eventsList, setEventList] = useState([]);
  const [filters, setFilters] = useState({
    country: '',
    category: '',
    start_date: '',
    end_date: '',
  });

  useEffect(() => {
    const apiService = new ApiService(FetchClient);
    
    const fetchCategories = async () => {
      try {
        const categoryList = await apiService.getCategories();
        setCategoryList(categoryList);
      } catch (error) {
        console.log(error);
      }
    }

    fetchCategories()
  }, [])

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
    <>
      <input
        type="text"
        name='country'
        onChange={handleFilterChange}
        placeholder='Filter by country' 
      />
      <select
        name='category'
        onChange={handleFilterChange}
      >
        {categoryList.map((category) => (
          <option key={category.id} value={category.id}>{category.name}</option>
        ))}
      </select>
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
      <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true} style={{ height: '100vh', width: '100vw' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
          {eventsList.map((event, index) => {
            const [longitude, latitude] = event.geometry[0].coordinates;
            const sourceUrl = event.sources[0].url;
            const categoryId = event.category.id;

            const handleEventIcon = (categoryId) => {
              if (categoryId === "wildfires") {
                return FireEvent;
              } else if (categoryId === "volcanoes"){
                return VolcanoEvent;
              } else if (categoryId === "severeStorms"){
                return SevereStorms;
              } else {
                return WaterEvent;
              }
            }

            return (
              <Marker icon={handleEventIcon(categoryId)} key={index} position={[latitude, longitude]}>
                <Popup>
                  {event.title}.
                  <br />
                  {event.country} - {event.date }
                  <br />
                  {event.category.id}
                  <br />
                  {event.description ? <p>{event.description}</p> : <p><a href={sourceUrl}>About</a></p>}
                </Popup>
              </Marker>
            )
          })}
      </MapContainer>
    </>
  )
}

export default MapPage