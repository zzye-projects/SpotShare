import './ListItem.css';
import StatusIndicator from './StatusIndicator';

const ListItem = ({address, unit, startDate, endDate, price, frequency, status=''}) => {
    return (
        <section className='list-item'>
            <div className='list-item-row'>
                <span className='list-item-address'>{`${address} ${unit}`}</span>
                <div className='list-item-status'><StatusIndicator status={status}/></div>
            </div>
            <div className='list-item-row'>
                <span className='list-item-dates'>{`${startDate} - ${endDate}`}</span>
                <span className='list-item-price'>{`$${price} / ${frequency}`}</span>
            </div>
        </section>
    )
};

export default ListItem;