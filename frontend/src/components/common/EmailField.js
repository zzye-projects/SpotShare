import InlineError from './InlineError';
import { useField } from 'formik';

const EmailField = ({label, error, ...props}) => {
    const [field, meta] = useField(props);
    return (
    <div className='form-field'>
        <label htmlFor={field.name}>{label}</label>
        <input id={field.name} type='email' {...field}/>
        <InlineError error={meta.touched && meta.error}/>
    </div>)}
export default EmailField;