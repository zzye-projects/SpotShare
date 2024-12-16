import './Footer.css';

const Footer = ({items}) => {
    return (
        <section className='footer'>
            <ul>
                {items.map(item => (
                    <li key={item}>
                        <a>{item}</a>
                    </li>
                ))}
            </ul>
        </section>
    )
}

export default Footer;