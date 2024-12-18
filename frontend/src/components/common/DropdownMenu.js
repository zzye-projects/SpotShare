import './DropdownMenu.css';
import Navigation from './Navigation';

const DropdownMenu = ({items, className}) => {
    return (
        <div 
            className={`dropdown-menu ${className}`}>
            <Navigation items={items}/>
        </div>  );
};

export default DropdownMenu;