import './StatusIndicator.css';

const StatusIndicator = ({status}) => {
    const statusList = {
        available: ['Available', 'green'],
        pending: ['Pending', 'orange'],
        leased: ['Leased', 'blue']
    }

    const [label, color] = statusList[status];
    return (
        <div className='status'>
            <span className='desktop-only' style={{color}}>{label}</span>
            <div className='status-circle' style={{backgroundColor:color}}></div>
        </div>
)};

export default StatusIndicator;

