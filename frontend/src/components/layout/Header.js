import './Header.css';
import './layout.css';
import { Link } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';
import { DropdownMenu } from '../common';

const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {

            if (!dropdownRef.current.contains(event.target) && isMenuOpen) {
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
        <li ref={dropdownRef}>
            <button 
                onClick={toggleMenu}
                className='profile'>Profile</button>
            <DropdownMenu 
                items={[
                    {item:'login', label:'Log In', onClick: toggleMenu}, 
                    {item:'logout', label:'Log Out', onClick: toggleMenu}]}
                isVisible={isMenuOpen}/>
        </li>
    </ul>);
};

export default Header;