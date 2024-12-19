import ListItem from './ListItem';
import './ListItems.css';

const ListItems = ({items}) => {
    return (
        <section className='list-items'>
            {items.map(item => <ListItem key={item.id} {...item}/>)}
        </section>
    )};

export default ListItems;