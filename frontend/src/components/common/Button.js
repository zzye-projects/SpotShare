import './Button.css';
const Button = ({label, onClick, isDisabled=false, className}) => (
        <button 
            type='submit'
            onClick={onClick}
            disabled={isDisabled}
            className={`${className} ${isDisabled? 'disabled-button': ''}`}>
            {label}
        </button>
    );

export default Button;