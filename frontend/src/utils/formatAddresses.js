const formatAddresses = addresses => {
    const formattedAddresses = {};
    addresses.forEach(address => {
        const {id, street, streetNo, city, state, postalCode, country } = address;
        formattedAddresses[id] = {
            ...address,
            formatted: `${street} ${streetNo}, ${city}, ${state} ${postalCode}, ${country}`}});
    return formattedAddresses;
    };

export default formatAddresses;