import './Overlay.css';

const Overlay = ({isVisible}) => {
    return (<div 
        className={`overlay ${isVisible? 'visible':''}`}></div>)
};

export default Overlay;