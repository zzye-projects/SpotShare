import { SelectField, DatePicker, PriceField, ViewOnlyField } from '../common';
import formatVehicles from '../../utils/formatVehicles';
import { useVehicles } from '../../context';
import {FREQUENCY_CHOICES} from '../../globals';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import './LeaseProposalForm.css';

const validationSchema = Yup.object({
    address: Yup.string().required('This field is required'),
    parkingUnit: Yup.string().required('This field is required'),
    vehicle: Yup.string().required('This field is required'),
    startDate: Yup.string().required('This field is required'),
    maxPrice: Yup.number().min(0, 'Price must be at least 0').required('This field is required'),
    payFrequency: Yup.string().required('This field is required')
  });

const LeaseProposalForm = ({
    address, 
    parkingUnit, 
    availableStart, 
    availableEnd=null, 
    price, 
    payFrequency}) => {
    
    const {vehicles} = useVehicles();
    return (
        <Formik
          initialValues={{
              address: address,
              parkingUnit: parkingUnit,
              vehicle: '',
              startDate: availableStart,
              endDate: availableEnd,
              maxPrice: price,
              payFrequency: payFrequency
              }}
          validationSchema={validationSchema}
          onSubmit={(values) => console.log(values)}
        >
          {({ isSubmitting, values, isValid, dirty }) => (
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
                      options={formatVehicles(vehicles)}/>
              </div>
              <div className='form-row'>
                  <Field
                      name='startDate'
                      as={DatePicker}
                      label='Start *'
                      minDate={availableStart}/>
                  <Field
                      name='endDate'
                      as={DatePicker}
                      label='End'
                      minDate={values.startDate ? new Date(values.startDate): availableStart}
                      maxDate={availableEnd}/>
              </div>
              <div className='form-row'>
                  <Field
                      name='maxPrice'
                      as={PriceField}
                      label='Max Price *'/>
                  <Field
                      name='payFrequency'
                      as={SelectField}
                      label='Per *'
                      options={FREQUENCY_CHOICES}/>
                  </div>
              </Form>
        )}
      </Formik>)};
export default LeaseProposalForm;