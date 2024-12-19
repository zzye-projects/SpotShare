import { ReactComponent as CloseIcon } from '../../assets/icons/close_icon.svg';
import './Modal.css';
import './common.css';

const Modal = ({title, children, isVisible}) => {
    return (
        <div className={`modal ${isVisible? 'visible':''}`}>
            <div className='modal-row'>
                <span>Progress Bar</span>
                <button className='invisible-button'>
                    <CloseIcon/>
                </button>
            </div>
            <div className='modal-row'><h1>{title}</h1></div>
            <div className='modal-row'>{children}</div>
            <div className='modal-row modal-actions'></div>
        </div>)};

export default Modal;