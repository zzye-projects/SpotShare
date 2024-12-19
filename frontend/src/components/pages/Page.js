import './Page.css';

const Page = ({title, children}) => {
    return (
        <section className='page'>
            <h1>{title}</h1>
            {children}
        </section>);
}

export default Page;