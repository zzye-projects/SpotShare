import {useField} from 'formik';
import './ViewOnlyField.css';

const ViewOnlyField = ({ label, value, ...props }) => {
    const [field, meta] = useField(props);

    return (
        <div className='form-field view-only'>
            <label htmlFor={field.name}>{label}</label>
            <textarea id={field.name} value={value} readOnly={true}/>
        </div>
    )
};

export default ViewOnlyField;