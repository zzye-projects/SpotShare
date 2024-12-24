import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const VehiclesContext = createContext();

export const useVehicles = () => useContext(VehiclesContext);

export const VehiclesProvider = ({children}) => {
    const [vehicles, setVehicles] = useState([]);
        useEffect(() => {
            const fetchVehicles = async () => {
                try {
                    const response = await axios.get('/api/vehicle');
                    setVehicles(response.data);
                } catch (error) {
                    console.error('Failed to fetch vehicles', error);
                }};
            fetchVehicles();
        }, []);
    
    return (
        <VehiclesContext.Provider value={{vehicles}}>
            {children}
        </VehiclesContext.Provider>
    )};