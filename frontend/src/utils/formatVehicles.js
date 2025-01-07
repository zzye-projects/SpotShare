const formatVehicles = vehicles => {
    const formattedVehicles = {};
    vehicles.forEach(vehicle => {
        const { id, make, model, colour, licensePlate } = vehicle;
        formattedVehicles[id] = {
            ...vehicle,
            formatted: `${make}/${model}/${colour}/${licensePlate}`
        }});
    return formattedVehicles}; 

export default formatVehicles;