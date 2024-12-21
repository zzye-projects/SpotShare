import { SearchForm } from '../forms';
import { Modal, ListItems, Overlay } from '../common';
import Page from './Page';
import { useState } from 'react';
import axios from 'axios';

const SearchParkingPage = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => { setIsModalOpen(false); setCurrentStep(1) }

    const totalSteps = 3;
    const [currentStep, setCurrentStep] = useState(1);
    const nextStep = () => setCurrentStep(currentStep + 1);
    const prevStep = () => {
        if (currentStep === 1) { closeModal(); }
        else { setCurrentStep(currentStep - 1); }
    }

    const [searchResults, setSearchResults] = useState([]);
    const handleSearchSubmit = async (data) => {
        try {
            const response = await axios.get('/api/parking');
            setSearchResults(response.data);
        } catch (error) {
            console.error('Failed to fetch parking units', error);
        }
    };

    const stepContent = [
        {title: 'Select Your Spot', content:<ListItems items={searchResults}/>},
        {title: 'Create a Proposal', content:null},
        {title: 'Review Lease', content: null}];
    const primaryBtn = {
        label: 'Next',
        onClick: nextStep,
        className: 'primary-button'};
    const secondaryBtn = {
        label: 'Back',
        onClick: prevStep,
        className: 'secondary-button'};

    return (
        <Page title="Find Parking">
            <SearchForm onSubmit={handleSearchSubmit}/>
            <Modal
                title={stepContent[currentStep - 1].title}
                isVisible={isModalOpen}
                onClose={closeModal}
                progressBar={{totalSteps, currentStep}}
                primaryBtn={primaryBtn}
                secondaryBtn={secondaryBtn}
                content={stepContent[currentStep - 1].content}/>
            <Overlay isVisible={isModalOpen}/>
        </Page>)};

export default SearchParkingPage;
