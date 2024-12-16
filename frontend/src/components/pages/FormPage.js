const FormPage = ({title, children}) => {
    return (
        <section className='form-page'>
            <h1>{title}</h1>
            {children}
        </section>);
}

export default FormPage;