from collections import defaultdict
import numpy as np


def get_z_angles(values):
    vx, vy, vz = (values["endX"] - values["startX"],
                  values["endY"] - values["startY"],
                  values["endZ"] - values["startZ"])
    norms = np.sqrt(vx**2+vy**2+vz**2)
    cos_theta_z = np.arccos(vz/norms) / np.pi
    return cos_theta_z

additional_variables = {
        "z_angles": {"getter": get_z_angles, 
                      "dependencies": ["startX", "startY", "startZ", "endX", "endY", "endZ"]}
}



def get_vars(all_variables):
    raw_variables = [variable for variable in all_variables 
                     if variable not in additional_variables.keys()]
    other_variables = [variable for variable in all_variables 
                       if variable in additional_variables.keys()]
    # add dependencies
    for variable in other_variables:
        new_variables = additional_variables[variable]["dependencies"]
        for new_variable in new_variables:
            if new_variable not in raw_variables:
                raw_variables.append(new_variable)
    return raw_variables, other_variables

def get_raw_values(array, raw_variables):
    values = defaultdict(list)
    for i, event in enumerate(array):
        event_values = {}
        # raw variables
        for value, var in zip(event, raw_variables):
            event_values[var] = value
            if hasattr(value, "__iter__"):
                values[var].extend(value)
            else:
                values[var].append(value)
    for i, k in values.items():
        values[i]=np.array(values[i])
    return values

def get_other_values(event_values, other_variables):
    # other variables (=additional)
    for var in other_variables:
        value = additional_variables[var]["getter"](event_values)
        event_values[var].extend(value)
    return event_values


