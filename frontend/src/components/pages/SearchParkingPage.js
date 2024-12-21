import { SearchForm } from '../forms';
import { Modal, ListItems, Overlay } from '../common';
import Page from './Page';
import { useState } from 'react';
import axios from 'axios';

const SearchParkingPage = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => { setIsModalOpen(false); setCurrentStep(0) }

    const totalSteps = 3;
    const [currentStep, setCurrentStep] = useState(1);
    const nextStep = () => setCurrentStep(currentStep + 1);
    const prevStep = () => {
        if (currentStep === 1) { closeModal(); }
        else { setCurrentStep(currentStep - 1); }
    }

    const [searchResults, setSearchResults] = useState([]);
    const handleSearchSubmit = async ({address, startDate, endDate, maxPrice, payFrequency}) => {
        const params = {'address': address, 'staff_approved': 'APPROVED'};
        if (startDate) { params['available_start_gte'] = startDate; }
        if (endDate) { params['available_end_lte'] = endDate; }
        if (maxPrice && payFrequency) { 
            params['payment_amount'] = maxPrice; 
            params['payment_frequency'] = payFrequency;}

        try {
            const response = await axios.get('/api/parking', {params:params});
            if (response.data.length > 0) { 
                nextStep();
                setSearchResults(response.data);
            }
            openModal();
        } catch (error) {
            console.error('Failed to fetch parking units', error);
        }
    };

    const nextBtn = {
        label: 'Next',
        onClick: nextStep,
        className: 'primary-button'};
    const backBtn = {
        label: 'Back',
        onClick: prevStep,
        className: 'secondary-button'};
    const cancelBtn = {
        label: 'Cancel',
        onClick: closeModal,
        className: 'secondary-button'
    }
    const stepContent = [
        {
            title: 'No units that satisfy your criteria', 
            content: <span>Please update your search criteria.</span>,
            primaryBtn: cancelBtn, secondaryBtn: null
        },
        {
            title: 'Select Your Spot', 
            content:<ListItems items={searchResults}/>,
            primaryBtn: nextBtn, secondaryBtn: cancelBtn
        },
        {
            title: 'Create a Proposal', 
            content: null,
            primaryBtn: nextBtn, secondaryBtn: backBtn
        },
        {
            title: 'Review Lease', 
            content: null,
            primaryBtn: nextBtn, secondaryBtn: backBtn
        }];

    return (
        <Page title="Find Parking">
            <SearchForm onSubmit={handleSearchSubmit}/>
            <Modal
                title={stepContent[currentStep].title}
                isVisible={isModalOpen}
                onClose={closeModal}
                progressBar={{totalSteps, currentStep}}
                primaryBtn={stepContent[currentStep].primaryBtn}
                secondaryBtn={stepContent[currentStep].secondaryBtn}
                content={stepContent[currentStep].content}/>
            <Overlay isVisible={isModalOpen}/>
        </Page>)};

export default SearchParkingPage;
