import './Main.css';
import { SearchForm } from '../forms';
import { FormPage, Page } from '../pages';
import { PLACEHOLDER_TEXT } from '../../globals';
import { Routes, Route } from 'react-router-dom';

const Main = () => (
    <section className='main'>
        <Routes>
            <Route 
                path="/" 
                element={
                <FormPage title="Find Parking">
                    <SearchForm />
                </FormPage>}/>
            <Route 
                path="/about" 
                element={<Page title='About Us' text={PLACEHOLDER_TEXT}/>} />
            <Route 
                path="/terms" 
                element={<Page title='Terms of Use' text={PLACEHOLDER_TEXT}/>} />
            <Route 
                path="/careers" 
                element={<Page title='Careers' text={PLACEHOLDER_TEXT}/>} />
            <Route 
                path="/contact" 
                element={<Page title='Contact Us' text={PLACEHOLDER_TEXT}/>} />
        </Routes>
    </section>
);

export default Main;