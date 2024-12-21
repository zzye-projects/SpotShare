import './ListItem.css';
import StatusIndicator from './StatusIndicator';

const ListItem = ({
    address, 
    parkingUnit, 
    availableStart, 
    availableEnd, 
    paymentAmount, 
    paymentpaymentFrequency, 
    status=''}) => {
    return (
        <section className='list-item'>
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
        </section>
    )
};

export default ListItem;