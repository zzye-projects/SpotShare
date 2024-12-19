import './DropdownMenu.css';
import './common.css';
import Navigation from './Navigation';

const DropdownMenu = ({items, isVisible}) => {
    return (
        <div 
            className={`dropdown-menu ${isVisible? 'visible':''}`}>
            <Navigation items={items}/>
        </div>  );
};

export default DropdownMenu;