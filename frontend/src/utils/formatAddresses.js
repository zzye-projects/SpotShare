const formatAddresses = (addresses) => {
    return addresses.map(({ id, street, street_no, city, state, postal_code, country }) => ({
        id,
        value: `${street} ${street_no}, ${city}, ${state} ${postal_code}, ${country}`
    }));
};

export default formatAddresses;