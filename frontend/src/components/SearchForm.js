import SelectField from './SelectField';
import {useEffect, useState} from 'react';
import axios from 'axios';
import formatAddresses from '../utils/formatAddresses' ;

const SearchForm = () => {
    const [addresses, setAddresses] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedAddress, setSelectedAddress] = useState('');
    useEffect(() => {
        const fetchAddresses = async () => {
            try {
                const response = await axios.get('/api/address');
                setAddresses(formatAddresses(response.data))
            } catch (error) {
                console.error('Failed to fetch addresses', error);
            } finally {
                setIsLoading(false);
            }
        }
        fetchAddresses()}, [])

    return (
        <form>
            <h1>Find Parking...</h1>
            <SelectField
                label='Address'
                required={true}
                selectedOption={selectedAddress}
                onChange={setSelectedAddress}
                isLoading={isLoading}
                options={addresses}/>
        </form>
    );
};

export default SearchForm;