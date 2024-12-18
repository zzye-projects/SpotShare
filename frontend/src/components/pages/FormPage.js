import './Page.css';
const FormPage = ({title, children}) => {
    return (
        <section className='form-page page'>
            <h1>{title}</h1>
            {children}
        </section>);
}

export default FormPage;