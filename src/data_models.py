
def validateParameters(option_parameters: dict) -> None:
    '''
    Validates the option parameters to ensure they are of the correct datatype.

    Arguments:
        option_parameters (dict): Dictionary of the option parameters
    
    Returns:
        None
    '''

    #The keys that are required to be included in option_parameters
    required_keys = ["stock", "strike", "time", "rate", "sigma", "option_type"]

    for required_key in required_keys:
        #Checks if a required key is absent from the option_parameters dictionary
        if required_key not in option_parameters:
            raise ValueError(f"Missing parameter: '{required_key}'.")
        
        #Checks that all numerical keys (stock, strike, time, rate, sigma) are of int or float types
        if (required_key != "option_type") and (not isinstance(option_parameters[required_key], (int, float))):
            raise ValueError(f"Parameter '{required_key}' must be a number.")
        
        #Checks that stock, strike, time and sigma are all positive
        #Rate is allowed to be negative to consider markets with negative risk-free rates
        if required_key in ["stock", "strike", "time", "sigma"] and option_parameters[required_key] <= 0:
            raise ValueError(f"Parameter '{required_key}' must be positive.")
        
    #Checks that option_type is either 'call' or put'
    if option_parameters["option_type"] not in ["call", "put"]:
        raise ValueError("Option type must either be 'call' or 'put'.")
    