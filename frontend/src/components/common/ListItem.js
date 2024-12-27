import './ListItem.css';
import StatusIndicator from './StatusIndicator';
import { formatAddresses } from '../../utils';
import { useAddresses } from '../../context';

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
    
    const {formattedAddresses} = useAddresses();
    const selectedAddress = formattedAddresses.find(item => item.id === address).value;

    return (
        <button 
            className={`list-item ${selectedId === id? 'selected':''}`}
            onClick={()=> selectFunction(id)}>
            <div className='list-item-row'>
                <span className='list-item-address'>{`${selectedAddress} - ${parkingUnit}`}</span>
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