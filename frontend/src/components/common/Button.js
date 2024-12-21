import './Button.css';
const Button = ({label, onClick, isDisabled=false, isDisabledLabel='', className}) => {
    return (
        <button 
            type='submit'
            onClick={onClick}
            disabled={isDisabled}
            className={className}>
            {isDisabled? isDisabledLabel: label}
        </button>
    )
}

export default Button;