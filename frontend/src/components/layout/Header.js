import './Header.css';
import './layout.css';
import { Link } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';
import { DropdownMenu } from '../common';

const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const profileRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {

            if (!profileRef.current.contains(event.target) && isMenuOpen) {
                setIsMenuOpen(false); 
            }};

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isMenuOpen]);

    const toggleMenu = () => { setIsMenuOpen(!isMenuOpen)};
    return (
    <ul className='header'>
        <li><Link to='/' className='company-logo'>Logo</Link></li>
        <li><Link to='/'>SpotShare</Link></li>
        <li>
            <button 
                ref={profileRef}
                onClick={toggleMenu}
                className='profile'>Profile</button>
            <DropdownMenu 
                items={[
                    {item:'login', label:'Log In'}, 
                    {item:'logout', label:'Log Out'}]}
                isVisible={isMenuOpen}/>
        </li>
    </ul>);
};

export default Header;