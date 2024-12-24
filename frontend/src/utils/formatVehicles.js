const formatVehicles = (vehicles) => {
    return vehicles.map(({id, make, model, colour, licensePlate}) => ({
        id, 
        value: `${make}/${model}/${colour}/${licensePlate}`
    }));
};

export default formatVehicles;