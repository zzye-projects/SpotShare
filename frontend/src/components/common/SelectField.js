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
                {Object.entries(options).map(([key, value]) => 
                    (<option key={key} value={key}>
                        {value.formatted}
                    </option>))}
            </select>
            <InlineError error={meta.touched && meta.error}/>
        </div>
    );
};

export default SelectField;
