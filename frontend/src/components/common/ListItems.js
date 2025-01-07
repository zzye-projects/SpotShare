import ListItem from './ListItem';
import './ListItems.css';

const ListItems = ({items, selected, selectFunction}) => {
    return (
        <section className='list-items'>
            {items.map(item => <ListItem 
                key={item.id}
                item={item}
                selected={selected}
                selectFunction={selectFunction}/>)}
        </section>
    )};

export default ListItems;