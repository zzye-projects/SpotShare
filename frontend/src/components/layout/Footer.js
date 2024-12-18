import './Footer.css';
import './layout.css'
import { Navigation } from '../common';

const Footer = () => {
    const items = [
        {item:'about', label: 'About Us'},
        {item:'terms', label: 'Terms of Use'},
        {item:'careers', label: 'Careers'},
        {item: 'contact', label: 'Contact Us'}];
    return (
        <section className='footer'>
            <Navigation items={items}/>
        </section>
    )
}

export default Footer;