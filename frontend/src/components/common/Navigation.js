import { Link } from 'react-router-dom';

const Navigation = ({items}) => {
    return(
        <ul>
            {items.map(({item, label}) => (
                <li key={item}>
                    <Link to={`/${item}`}>{label}</Link>
                </li>
            ))}
        </ul>)
};

export default Navigation;