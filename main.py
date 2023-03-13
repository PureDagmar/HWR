import json
import yaml

import cv2
import numpy as np

from utils.shape_correction import align_images
from utils.cut_cells import hor_lines_cut

with open('data/Form07.json', 'r') as file:
    data = file.read()
    form = json.loads(data)





if __name__ == "__main__":
    scan_path = '/home/kirill/.clearml/cache/storage_manager/datasets/ds_abd87cae0731423fbdced8d01e6b5493/13329-processed-2.png'
    image = cv2.imread(scan_path, cv2.IMREAD_COLOR)
    cv2.imshow('img', cv2.resize(image, (500, 700)))
    # WRITE MAP!!!
    # with open('config/form_map.yml', 'w') as file:
    #     file.write('Form_map:\n')
    #     file.write('  ID:\n')
    #     for i in range(1, 24):
    #         file.write('    {0}:\n'.format(i))
    #         for j in range(1, 10):
    #             file.write('      {0}: '.format(j))
    #             cells = np.array(form['objects'][(i - 1) * 32 + (j - 1)]['points']['exterior']) * 2
    #             file.write(np.array2string(cells, separator = ', '))
    #             file.write('\n')
    #     file.write('  VACCINATION:\n')
    #     for i in range(1, 24):
    #         file.write('    {0}:\n'.format(i))
    #         for j in range(10, 33):
    #             file.write('      {0}: '.format(j))
    #             cells = np.array(form['objects'][(i - 1) * 32 + (j - 1)]['points']['exterior']) * 2
    #             file.write(np.array2string(cells, separator = ', '))
    #             file.write('\n')

    image = align_images(image)

    y, x = 5, 50

    with open('config/form_map.yml') as stream:
        data = yaml.safe_load(stream)['Form_map']['ID']
        for i in range(1, 24):
            for j in range(1, 10):
                cord = data[i][j]
                area_of_interest = image[cord[0][1] - x:cord[1][1] + x, cord[0][0] - y:cord[1][0] + y]
                cv2.imshow('cell', hor_lines_cut(area_of_interest))
                cv2.waitKey()
    with open('config/form_map.yml') as stream:
        data = yaml.safe_load(stream)['Form_map']['VACCINATION']
        for i in range(1, 24):
            for j in range(10, 33):
                cord = data[i][j]
                area_of_interest = image[cord[0][1] - x:cord[1][1] + x, cord[0][0] - y:cord[1][0] + y]
                cv2.imshow('cell', hor_lines_cut(area_of_interest))
                cv2.waitKey()