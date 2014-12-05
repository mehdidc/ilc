import sys
import os
import numpy as np
from root_numpy import root2array, list_branches
from vars import get_vars, get_raw_values, get_other_values
from collections import defaultdict

def raw_images_event_to_array(result, values, event_id=None):
    assert event_id is not None
    energy, posx, posy, posz = values["energy"], values["posx"], values["posy"], values["posz"]
    for e, x, y, z in zip(energy, posx, posy, posz):
        result[0][event_id , z, y, x]  = e
    return result

def raw_images_post_processing(result):
    return result[0]

def raw_images_predict_angle_event_to_array(result, values, event_id=None):
    result = raw_images_event_to_array(result, values, event_id)
    result[1][event_id][0] = np.mean(values["z_angles"])
    return result

def raw_images_predict_angle_post_processing(result):
    return result

raw_images = {"variables": ["energy", "posx", "posy", "posz"], 
              "event_to_array_func": raw_images_event_to_array,
              "shapes": ((30, 18, 18),),
              "post_processing_func": raw_images_post_processing}

raw_images_predict_angle = {"variables": raw_images["variables"] + ["z_angles"], 
                            "event_to_array_func": raw_images_predict_angle_event_to_array,
                            "shapes": ((30, 18, 18), (1,) ),
                            "post_processing_func": raw_images_predict_angle_post_processing}



structures = {
        "raw_images": raw_images,
        "raw_images_predict_angle": raw_images_predict_angle
}

if __name__ == "__main__":
    rootfiles_path = '../rootfiles'

    filenames = ('Secondaries.root',
                'EcalReconstruction.root')
    treename = 'Content'

    if len(sys.argv) <= 1:
        print "structures available : "
        print structures.keys()
        sys.exit(0)
        
    structure = structures[sys.argv[1]]
    
    raw_variables, other_variables = get_vars(structure["variables"])
    
    arrays = []
    branches = []
    file_raw_variables = []
    for filename in filenames:
        filename = os.path.join(rootfiles_path, filename)
        branches_cur = list_branches(filename, treename)
        file_raw_variables.append([b for b in branches_cur if b in raw_variables])
        array = root2array( filename,
                            treename, branches=file_raw_variables[-1])
        arrays.append(array)
        branches.append(branches_cur)

    result = []
    array_len = len(arrays[0])
    for shape in structure["shapes"]:
        result.append( np.zeros(  tuple([array_len] + list(shape))  ) )

    result = structure.get("pre_processing_func", lambda x:x)(result)
    
    for event_id in xrange(array_len):
        values = defaultdict(list)
        for array, file_raw_variables_cur in zip(arrays, file_raw_variables):
            new_values = (get_raw_values(array[event_id:event_id+1], file_raw_variables_cur))

            for k, v in new_values.items():
                if k not in values:
                    values[k] = v

        for k in values.keys():values[k]=np.array(values[k])
        values = get_other_values(values, other_variables)
        result = structure["event_to_array_func"](result, values, event_id)
    result = structure.get("post_processing_func", lambda x:x)(result)
    np.savez(sys.argv[2], *result)
