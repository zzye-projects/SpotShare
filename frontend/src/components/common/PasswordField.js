import InlineError from './InlineError';
import { useField } from 'formik';

const PasswordField = ({label, error, ...props}) => {
    const [field, meta] = useField(props);
    return (
    <div className='form-field'>
        <label htmlFor={field.name}>{label}</label>
        <input id={field.name} type='password' {...field}/>
        <InlineError error={meta.touched && meta.error}/>
    </div>)}
export default PasswordField;