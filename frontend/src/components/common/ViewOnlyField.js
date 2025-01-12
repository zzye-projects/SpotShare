import {useField} from 'formik';
import './ViewOnlyField.css';

const ViewOnlyField = ({ label, value, ...props }) => {
    return (
        <div className='form-field view-only'>
            <label htmlFor={props.name}>{label}</label>
            <textarea id={props.name} value={value} readOnly={true}/>
        </div>
    )
};

export default ViewOnlyField;