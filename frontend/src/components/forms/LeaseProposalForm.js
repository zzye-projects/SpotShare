import { SelectField, DatePicker, PriceField, ViewOnlyField } from '../common';
import { useVehicles } from '../../context';
import {FREQUENCY_CHOICES} from '../../globals';
import { Formik, Field, Form, useFormikContext } from 'formik';
import * as Yup from 'yup';
import { useEffect } from 'react';
import './LeaseProposalForm.css';
import './forms.css';

const LeaseProposalForm = ({userEntry, updateUserEntry}) => {
    const {vehicles} = useVehicles();
    const today = new Date();
    console.log(userEntry);

    // return (
    //     <form className='lease-proposal-form'>
    //         <div className='form-row'>
    //             <ViewOnlyField
    //                 props={{name:'address'}}
    //                 label='Address *'
    //                 value={userEntry.address.formatted}/>
    //             <ViewOnlyField
    //                 props={{name:'parkingUnit'}}
    //                 label='Parking Unit *'
    //                 value={userEntry.parking.parkingUnit}/>
    //         </div>
    //         <div className='form-row'>
    //              <SelectField
    //                 props={{name:'vehicle'}}
    //                 label='Vehicle *'
    //                 options={vehicles}/>
    //          </div>
    //     </form>)};

    const validationSchema = Yup.object({
        address: Yup.string().required('This field is required'),
        parkingUnit: Yup.string().required('This field is required'),
        vehicle: Yup.string().required('This field is required'),
        startDate: Yup.string().required('This field is required'),
        maxPrice: Yup.number().min(0, 'Price must be at least 0').required('This field is required'),
        payFrequency: Yup.string().required('This field is required')
    });
    const changeHandler = e => {
            console.log('something is changing!')
    }
    return (
        <Formik
            initialValues={{
                address: userEntry.address.formatted,
                parkingUnit: userEntry.parking.parkingUnit,
                vehicle: '',
                startDate: '',
                endDate: '',
                price: '',
                payFrequency: ''
                }}
            validationSchema={validationSchema}>
            { ({ values, isValid, dirty }) => { 
                return (
                <Form className='lease-proposal-form'>
                <div className='form-row'>
                    <Field
                        name='address'
                        as={ViewOnlyField}
                        label='Address *'/>
                    <Field
                        name='parkingUnit'
                        as={ViewOnlyField}
                        label='Parking Unit *'/>
                </div>
                <div className='form-row'>
                    <Field
                        name='vehicle'
                        as={SelectField}
                        label='Vehicle *'
                        options={vehicles}
                        onChange={changeHandler}/>
                </div>
                <div className='form-row'>
                    <Field
                        name='startDate'
                        as={DatePicker}
                        label='Start *'
                        minDate={new Date(userEntry.parking.availableStart) > today ? new Date(userEntry.parking.availableStart): today}
                        maxDate={userEntry.parking.availableEnd? new Date(userEntry.parking.availableEnd): null}/>
                    <Field
                        name='endDate'
                        as={DatePicker}
                        label='End'
                        minDate={values.startDate ? new Date(values.startDate): today}
                        maxDate={userEntry.parking.availableEnd? new Date(userEntry.parking.availableEnd): null}
                        />
                </div>
                <div className='form-row'>
                    <Field
                        name='price'
                        as={PriceField}
                        label='Proposed Price *'/>
                    <Field
                        name='payFrequency'
                        as={SelectField}
                        label='Per *'
                        options={FREQUENCY_CHOICES}/>
                    </div>
                </Form>
            )}}
    </Formik>)};

export default LeaseProposalForm;
