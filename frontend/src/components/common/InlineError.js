import './InlineError.css';

const InlineError = ({error}) => {
    return (error && <div className='inline-error'>{error}</div>)
}

export default InlineError;