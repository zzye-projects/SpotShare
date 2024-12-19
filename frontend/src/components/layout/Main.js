import './Main.css';
import { SearchParkingPage, Page } from '../pages';
import { PLACEHOLDER_TEXT } from '../../globals';
import { Routes, Route } from 'react-router-dom';

const Main = () => (
    <section className='main'>
        <Routes>
            <Route 
                path="/" 
                element={<SearchParkingPage/>}/>
            <Route 
                path="/about" 
                element={<Page title='About Us'>{PLACEHOLDER_TEXT}</Page>}/>
            <Route 
                path="/terms" 
                element={<Page title='Terms of Use'>{PLACEHOLDER_TEXT}</Page>}/>
            <Route 
                path="/careers" 
                element={<Page title='Careers'>{PLACEHOLDER_TEXT}</Page>}/>
            <Route 
                path="/contact" 
                element={<Page title='Contact Us'>{PLACEHOLDER_TEXT}</Page>}/>
        </Routes>
    </section>
);

export default Main;