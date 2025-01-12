import './Main.css';
import { SearchParkingPage, Page } from '../pages';
import { PLACEHOLDER_TEXT } from '../../globals';
import { Routes, Route } from 'react-router-dom';
import { LoginForm, ForgotPasswordForm } from '../forms';

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
            <Route 
                path="/login" 
                element={<Page title='Login'><LoginForm/></Page>}/>
            <Route 
                path="/forgot-password" 
                element={<Page title='Reset Password'><ForgotPasswordForm/></Page>}/>
        </Routes>
    </section>
);

export default Main;