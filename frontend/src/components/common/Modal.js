import { ReactComponent as CloseIcon } from '../../assets/icons/close_icon.svg';
import './Modal.css';
import './common.css';
import ProgressBar from './ProgressBar';
import Button from './Button';

const Modal = ({
        title, 
        content, 
        isVisible, 
        onClose, 
        primaryBtn=null, 
        secondaryBtn=null,
        progressBar=null}) => {
            
    return (
        <div className={`modal ${isVisible? 'visible':''}`}>
            <div className='modal-row'>
                {progressBar? <ProgressBar {...progressBar}/>:null}
                <button 
                    onClick={onClose}
                    className='invisible-button'>
                    <CloseIcon/>
                </button>
            </div>
            <div className='modal-row'><h1>{title}</h1></div>
            <div className='modal-row'>{content}</div>
            <div className='modal-row modal-actions'>
                {secondaryBtn? <Button {...secondaryBtn}/>: null}
                {primaryBtn? <Button {...primaryBtn}/>: null}
            </div>
        </div>)};

export default Modal;