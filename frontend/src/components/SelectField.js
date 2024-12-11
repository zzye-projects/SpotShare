import {useEffect} from 'react';

const SelectField = ({label, required, selectedOption, onChange, isLoading, options}) => {
    return (
        <label>
            {label} {required? <sup>*</sup>: ''}
            <select
                value={selectedOption}
                onChange={e => onChange(e.target.value)}
                disabled={isLoading}>
                {options.map(({id, value}) => (
                    <option 
                        key={id}
                        value={id}>
                            {value}
                        </option>
                ))}
            </select>
        </label>
    );
};

export default SelectField;
