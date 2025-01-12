import { Link } from 'react-router-dom';

const Navigation = ({items}) => {
    return(
        <ul>
            {items.map(({item, label, onClick}) => (
                <li key={item}>
                    <Link to={`/${item}`} onClick={onClick}>{label}</Link>
                </li>
            ))}
        </ul>)
};

export default Navigation;