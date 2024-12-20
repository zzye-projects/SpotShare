import { ReactComponent as CloseIcon } from '../../assets/icons/close_icon.svg';
import './Modal.css';
import './common.css';
import ProgressBar from './ProgressBar';

const Modal = ({title, children, isVisible, onClose, primaryBtnClick = null, secondaryBtnClick = null}) => {
    return (
        <div className={`modal ${isVisible? 'visible':''}`}>
            <div className='modal-row'>
                <ProgressBar steps={5} currentStep={3}/>
                <button 
                    onClick={onClose}
                    className='invisible-button'>
                    <CloseIcon/>
                </button>
            </div>
            <div className='modal-row'><h1>{title}</h1></div>
            <div className='modal-row'>{children}</div>
            <div className='modal-row modal-actions'>
            </div>
        </div>)};

export default Modal;