const formatAddresses = (addresses) => {
    return addresses.map(({ id, street, streetNo, city, state, postalCode, country }) => ({
        id, 
        value: `${street} ${streetNo}, ${city}, ${state} ${postalCode}, ${country}`}))};

export default formatAddresses;