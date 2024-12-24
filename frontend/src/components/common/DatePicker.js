import InlineError from './InlineError';
import { useField } from 'formik';

const DatePicker = ({label, minDate, maxDate=null, error, ...props}) => {
    const [field, meta] = useField(props);
    const minDateString = minDate ? minDate.toISOString().split('T')[0]: '';
    const maxDateString = maxDate? maxDate.toISOString().split('T')[0]: '';
    
    return (
        <div className='form-field'>
            <label htmlFor={field.name}>{label}</label>
            <input id={field.name}
                type='date' {...field} 
                min={minDateString || undefined}
                max={maxDateString || undefined}/>
            <InlineError error={meta.touched && meta.error}/>
        </div>);
};

export default DatePicker;
