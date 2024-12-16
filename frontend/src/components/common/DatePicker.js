import InlineError from './InlineError';
import { useField } from 'formik';

const DatePicker = ({label, minDate, error, ...props}) => {
    const [field, meta] = useField(props);
    const minDateString = minDate.toISOString().split('T')[0];
    
    return (
        <div className='form-field'>
            <label htmlFor={field.name}>{label}</label>
            <input id={field.name}
                type='date' {...field} 
                min={minDateString}/>
            <InlineError error={meta.touched && meta.error}/>
        </div>);
};

export default DatePicker;
