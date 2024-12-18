import './Page.css';

const Page = ({title, text}) => {
    return (
        <section className='page'>
            <h1>{title}</h1>
            <span>{text}</span>
        </section>);
}

export default Page;