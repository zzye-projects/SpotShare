import './ListItem.css';
import StatusIndicator from './StatusIndicator';
import {FREQUENCY_CHOICES} from '../../globals';

const ListItem = ({
    item,
    selected,
    selectFunction }) => {
    const { id, 
        parkingUnit,
        availableStart, 
        availableEnd, 
        paymentAmount, 
        paymentFrequency, 
        status} = item;
    return (
        <button 
            className={`list-item ${selected.parking && selected.parking.id === id? 'selected':''}`}
            onClick={()=> selectFunction(item)}>
            <div className='list-item-row'>
                <span className='list-item-address'>{`${selected.address.formatted} - ${parkingUnit}`}</span>
                <div className='list-item-status'>
                    {status? <StatusIndicator status={status}/>:null}
                </div>
            </div>
            <div className='list-item-row'>
                <span className='list-item-dates'>{`${availableStart} - ${availableEnd}`}</span>
                <span className='list-item-paymentAmount'>{`$${paymentAmount} / ${FREQUENCY_CHOICES[paymentFrequency].formatted}`}</span>
            </div>
        </button>
    )
};

export default ListItem;