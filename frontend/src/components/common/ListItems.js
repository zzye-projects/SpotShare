import ListItem from './ListItem';
import './ListItems.css';

const ListItems = ({items, selectedId, selectFunction}) => {
    return (
        <section className='list-items'>
            {items.map(item => <ListItem 
                key={item.id}
                {...item}
                selectedId={selectedId}
                selectFunction={selectFunction}/>)}
        </section>
    )};

export default ListItems;