import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { formatAddresses } from '../utils';

const AddressesContext = createContext();

export const useAddresses = () => useContext(AddressesContext);

export const AddressesProvider = ({children}) => {
    const [addresses, setAddresses] = useState([]);
    const [formattedAddresses, setFormattedAddresses] = useState([]);
    const [isLoadingAddresses, setIsLoadingAddresses] = useState(true);

    useEffect(() => {
        const fetchAddresses = async () => {
            try {
                const response = await axios.get('/api/address');
                setAddresses(response.data);
                setFormattedAddresses(formatAddresses(response.data));
            } catch (error) {
                console.error('Failed to fetch addresses', error);
            } finally {
                setIsLoadingAddresses(false);
            }
        }
        fetchAddresses()}, [])

    return (
        <AddressesContext.Provider value={{addresses, formattedAddresses, isLoadingAddresses}}>
            {children}
        </AddressesContext.Provider>
    )
}