import { EmailField, Button } from '../common';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import './forms.css';
import { Link } from 'react-router-dom';

const ForgotPasswordForm = () => {
    const validationSchema = Yup.object({
        email: Yup.string().required('Email is required')});

    return (
      <Formik
        initialValues={{ email: '', password: ''}}
        validationSchema={validationSchema}
        onSubmit={(values) => {
            console.log(values)}}>
        {({ isSubmitting, values, isValid, dirty }) => (
            <Form className='forgot-password-form'>
                <div className='form-row'>
                    <Field
                        name='email'
                        as={EmailField}
                        label='Email *'/>
                    <Link to={'/login'}>Back to Login</Link>
                </div>
                <div className='form-row form-buttons'>
                <Button
                    label="Login"
                    isDisabled={!isValid || !dirty}
                    className='primary-button'/>
                </div>
            </Form>)}
        </Formik>)};

export default ForgotPasswordForm;