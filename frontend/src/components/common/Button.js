import './Button.css';
const Button = ({label, onClick, handleSubmit, isLoading, isLoadingLabel, className}) => {
    return (
        <button 
            type='submit'
            onClick={handleSubmit? handleSubmit: onClick}
            disabled={isLoading}
            className={className}>
            {isLoading? isLoadingLabel: label}
        </button>
    )
}

export default Button;