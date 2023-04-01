import json
import yaml

with open('./config/utils_config.yml') as stream:
    config = yaml.safe_load(stream)['resultToJson']


def write_result_to_json(result):
    with open(config['pathToSave'], 'w') as file:
        file.write('ID:')
        for i in range(1, 24):
            str_res = ''
            for j range(1, 10):
                str_res += result['ID'][i][j]
            file.write('  {0}: {1}'.format(i, str_res))
        file.write('VACCINATION:')
        for i in range(1, 24):
            str_res = ''
            for j in range(1, 24):
                str_res += result['VACCINATION'][i][j]
            file.write('  {0}: {1}'.format(i, str_res))
