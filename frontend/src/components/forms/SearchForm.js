import { SelectField, DatePicker, PriceField, Button } from '../common';
import { useEffect, useState } from 'react';
import axios from 'axios';
import formatAddresses from '../../utils/formatAddresses' ;
import {FREQUENCY_CHOICES} from '../../globals';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import './SearchForm.css';

const validationSchema = Yup.object({
    address: Yup.string().required('Address is required'),
    maxPrice: Yup.number().min(0, 'Price must be at least 0').required('Max price is required'),
  });
  
  const SearchForm = ({onSubmit}) => {
    const [addresses, setAddresses] = useState([]);
    const [isLoadingAddresses, setIsLoadingAddresses] = useState(true);

    useEffect(() => {
        const fetchAddresses = async () => {
            try {
                const response = await axios.get('/api/address');
                setAddresses(formatAddresses(response.data))
            } catch (error) {
                console.error('Failed to fetch addresses', error);
            } finally {
                setIsLoadingAddresses(false);
            }
        }
        fetchAddresses()}, [])

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
        {({ isSubmitting, values }) => (
          <Form className='search-form'>
            <div className='form-row'>
                <Field
                    name='address'
                    as={SelectField}
                    label='Address *'
                    options={addresses}
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
                    isDisabled={isSubmitting}
                    isDisabledLabel="Searching..."
                    className='primary-button'/>
            </div>
            </Form>

      )}
    </Formik>)}

export default SearchForm;