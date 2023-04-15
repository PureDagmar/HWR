import json

from utils.align import write_map, write_cell_images
from utils.result_to_json import write_result_to_json


if __name__ == "__main__":
    scan_path = '/home/kirill/.clearml/cache/storage_manager/datasets/ds_abd87cae0731423fbdced8d01e6b5493/13336-processed-1.png'
    # Write map config yaml
    # write_map()

    # Write dict with images
    write_cell_images(scan_path)

    # Inference
    # ...
    result = dict()

    # Write str result to json
    write_result_to_json(dict)