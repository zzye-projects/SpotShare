import InlineError from './InlineError';
import { useField } from 'formik';

const PriceField = ({label, error, ...props}) => {
    const [field, meta] = useField(props);
    return (
    <div className='form-field'>
        <label htmlFor={field.name}>{label}</label>
        <input id={field.name} type='number' {...field}/>
        <InlineError error={meta.touched && meta.error}/>
    </div>
)};

export default PriceField;