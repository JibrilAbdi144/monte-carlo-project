
def validateParameters(option_parameters: dict) -> None:

    required_keys = ["stock", "strike", "time", "rate", "sigma", "option_type"]

    for required_key in required_keys:

        if required_key not in option_parameters:
            raise ValueError(f"Missing parameter: '{required_key}'.")
        
        if (required_key != "option_type") and (not isinstance(option_parameters[required_key], (int, float))):
            raise ValueError(f"Parameter '{required_key}' must be a number.")
        
        if required_key in ["stock", "strike", "time", "volatility"] and option_parameters[required_key] <= 0:
            raise ValueError(f"Parameter '{required_key}' must be positive.")
        
    if option_parameters["option_type"] not in ["call", "put"]:
        raise ValueError("Option type must either be 'call' or 'put'.")
    