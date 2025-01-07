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

const LeaseProposalForm = ({lease, updateLease}) => {
    const {vehicles} = useVehicles();
    console.log(lease);

    return (
        <Formik
          initialValues={{
              address: lease.address.formatted,
              parkingUnit: lease.parking.parkingUnit,
              vehicle: '',
              startDate: '',
              endDate: '',
              price: '',
              payFrequency: ''
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
                      options={vehicles}/>
              </div>
              <div className='form-row'>
                  <Field
                      name='startDate'
                      as={DatePicker}
                      label='Start *'
                      minDate={new Date()}/>
                  <Field
                      name='endDate'
                      as={DatePicker}
                      label='End'
                      minDate={values.startDate ? new Date(values.startDate): new Date()}
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
        )}
      </Formik>)};
export default LeaseProposalForm;