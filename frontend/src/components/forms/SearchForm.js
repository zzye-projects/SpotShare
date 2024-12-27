import { SelectField, DatePicker, PriceField, Button } from '../common';
import { useAddresses } from '../../context';
import formatAddresses from '../../utils/formatAddresses' ;
import {FREQUENCY_CHOICES} from '../../globals';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import './SearchForm.css';

const validationSchema = Yup.object({
    address: Yup.string().required('Address is required'),
    maxPrice: Yup.number().min(0, 'Price must be at least 0'),
  });
  
  const SearchForm = ({onSubmit}) => {
    const {formattedAddresses, isLoadingAddresses} = useAddresses();

    return (
      <Formik
        initialValues={{
            address: '',
            startDate: '',
            endDate: '',
            maxPrice: '',
            payFrequency: 'MONTHLY'
            }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting }) => {
            onSubmit(values);
            setSubmitting(false);}}
      >
        {({ isSubmitting, values, isValid, dirty }) => (
          <Form className='search-form'>
            <div className='form-row'>
                <Field
                    name='address'
                    as={SelectField}
                    label='Address *'
                    options={formattedAddresses}
                    isLoading={isLoadingAddresses}/>
            </div>
            <div className='form-row'>
                <Field
                    name='startDate'
                    as={DatePicker}
                    label='Start'
                    minDate={new Date()}/>
                <Field
                    name='endDate'
                    as={DatePicker}
                    label='End'
                    minDate={values.startDate ? new Date(values.startDate): new Date()}/>
            </div>
            <div className='form-row'>
                <Field
                    name='maxPrice'
                    as={PriceField}
                    label='Max Price'/>
                <Field
                    name='payFrequency'
                    as={SelectField}
                    label='Per'
                    options={FREQUENCY_CHOICES}/>
                </div>
            <div className='form-row'>
                <Button
                    label="Search"
                    isDisabled={isSubmitting || !isValid || !dirty}
                    className='primary-button'/>
            </div>
            </Form>

      )}
    </Formik>)}

export default SearchForm;