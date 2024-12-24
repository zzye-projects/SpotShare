import './ListItem.css';
import StatusIndicator from './StatusIndicator';

const ListItem = ({
    id, 
    address, 
    parkingUnit, 
    availableStart, 
    availableEnd, 
    paymentAmount, 
    paymentpaymentFrequency, 
    status='',
    selectedId,
    selectFunction }) => {
    return (
        <button 
            className={`list-item ${selectedId === id? 'selected':''}`}
            onClick={()=> selectFunction(id)}>
            <div className='list-item-row'>
                <span className='list-item-address'>{`${address} ${parkingUnit}`}</span>
                <div className='list-item-status'>
                    {status? <StatusIndicator status={status}/>:null}
                </div>
            </div>
            <div className='list-item-row'>
                <span className='list-item-dates'>{`${availableStart} - ${availableEnd}`}</span>
                <span className='list-item-paymentAmount'>{`$${paymentAmount} / ${paymentpaymentFrequency}`}</span>
            </div>
        </button>
    )
};

export default ListItem;