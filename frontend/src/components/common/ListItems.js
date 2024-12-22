import ListItem from './ListItem';
import './ListItems.css';

const ListItems = ({items, selection}) => {
    return (
        <section className='list-items'>
            {items.map(item => <ListItem 
                key={item.id}
                {...item}
                {...selection}/>)}
        </section>
    )};

export default ListItems;