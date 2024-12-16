import InlineError from './InlineError';
import { useField } from 'formik';

const SelectField = ({label, isLoading, options, ...props}) => {
    const [field, meta] = useField(props);
    return (
        <div className='form-field'>
            <label htmlFor={field.name}>{label}</label>
            <select 
                id={field.name}
                {...field} 
                disabled={isLoading}>
                <option value="" disabled>Select an option</option>
                {options.map(({id, value}) => (
                    <option key={id} value={id}>
                        {value}
                    </option>
                ))}
            </select>
            <InlineError error={meta.touched && meta.error}/>
        </div>
    );
};

export default SelectField;
