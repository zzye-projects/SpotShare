import { SearchForm } from '../forms';
import { Modal, ListItems, Overlay } from '../common';
import Page from './Page';
import { useState } from 'react';

const mockListItems = [
    {id: '1', address: 'address1', unit: 'unit1', startDate: 'startDate1', endDate: 'endDate1', price: 'price1', frequency: 'monthly', status: 'leased'},
    {id: '2', address: 'address2', unit: 'unit2', startDate: 'startDate2', endDate: 'endDate2', price: 'price2', frequency: 'annually', status: 'available'},
    {id: '3', address: 'address3', unit: 'unit3', startDate: 'startDate3', endDate: 'endDate3', price: 'price3', frequency: 'weekly', status: 'pending'},
];
const SearchParkingPage = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const toggleModal = () => {
        setIsModalOpen(!isModalOpen)
        console.log('modal is getting toggled ', isModalOpen)
    }; 

    return (
        <Page title="Find Parking">
            <SearchForm onSubmit={toggleModal}/>
            <Modal 
                title='Select Your Spot'
                isVisible={isModalOpen}
                onClose={toggleModal}>
                <ListItems items={mockListItems}/>
            </Modal>
            <Overlay isVisible={isModalOpen}/>
        </Page>)};

export default SearchParkingPage;
