const DropdownMenu = ({items}) => {
    return (
        <div className='dropdown-menu'>
            <ul>
                {items.map(({item, link}) => (
                    <li><a href={link}>{item}</a></li>
                ))}
            </ul>
        </div>
    );
};

export default DropdownMenu;