import { EmailField, PasswordField, Button } from '../common';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import './LoginForm.css';
import './forms.css';
import { Link } from 'react-router-dom';

const LoginForm = () => {
    const validationSchema = Yup.object({
        email: Yup.string().required('Email is required'),
        password: Yup.string().required('Password is required')});

    return (
      <Formik
        initialValues={{ email: '', password: ''}}
        validationSchema={validationSchema}
        onSubmit={(values) => {
            console.log(values)}}>
        {({ isSubmitting, values, isValid, dirty }) => (
          <Form className='login-form'>
            <div className='form-row'>
                <Field
                    name='email'
                    as={EmailField}
                    label='Email *'/>
            </div>
            <div className='form-row'>
                <Field
                        name='password'
                        as={PasswordField}
                        label='Password *'/>
                <Link to={'/forgot-password'}>Forgot Password?</Link>
            </div>
            <div className='form-row form-buttons'>
                <Button
                    label="Login"
                    isDisabled={!isValid || !dirty}
                    className='primary-button'/>
            </div>
        </Form>)}
    </Formik>)}

export default LoginForm;