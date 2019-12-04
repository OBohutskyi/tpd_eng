import json
import os


class Project:

    @staticmethod
    def extract_values(source, key):
        arr = []

        def extract(json_object, temp, key):
            if isinstance(json_object, dict):
                for k, v in json_object.items():
                    if isinstance(v, (dict, list)):
                        extract(v, temp, key)
                    elif k in key:
                        temp.append(v)
            elif isinstance(json_object, list):
                for item in json_object:
                    extract(item, temp, key)
            return temp

        return extract(source, arr, key)

    @staticmethod
    def process_file(file_name, result):
        print('started processing', file_name, 'file')
        with open(file_name, "r") as readFile:
            data = json.load(readFile)
            source_data = Project.extract_values(data, 'name,location')
            segment = source_data[1]
            element_path = source_data[1]
            for x in range(len(source_data)):
                b = source_data[x]
                if b.startswith('Segment-'):
                    segment = b[8:]
                    element_path = source_data[x]
                elif b.startswith(segment):
                    if x+2 >= len(source_data):
                        break
                    if not (source_data[x + 1].startswith(segment) or (source_data[x + 2].startswith('Segment-'))):
                        if source_data[x + 2].find('/') != -1:
                            if element_path + '/' + b + ':' + source_data[x + 2] in result:
                                result.update({element_path + '/' + b + ':' + source_data[x + 2]: result[
                                                                                                      element_path + '/' + b + ':' +
                                                                                                      source_data[
                                                                                                          x + 2]] + 1})
                            else:
                                result[element_path + '/' + b + ':' + source_data[x + 2]] = 1
        print('ended processing', file_name, 'file')
        return result

    @staticmethod
    def main_t():
        path = 'input'
        versions = {}

        for r, d, f in os.walk(path):
            for file in f:
                file_path = os.path.join(r, file)
                print('reading file:', file_path)
                start_src_index = file_path.find('_RSX')
                start_dest_index = file_path.find('_to_')
                end_index = file_path.find('_Transaction')
                source = file_path[start_src_index + 1:start_dest_index]
                destination = file_path[start_dest_index + 4:end_index + 16]
                if source + ':' + destination in versions:
                    versions[source + ':' + destination] = Project.process_file(os.path.join(r, file), versions[source + ':' + destination])
                else:
                    versions[source + ':' + destination] = Project.process_file(os.path.join(r, file), {})

        print('started to write output file')
        output = open('output/output.csv', 'w')
        output.write('Source,Destination,ElementPath,SourcePath,Occurrences\n')
        for item in versions:
            for i in versions[item]:
                result = item + ',' + i + ',' + json.dumps(versions[item][i]) + '\n'
                result = result.replace(':', ',')
                output.write(result)

        output.close()
        print('finished to write output file')


Project.main_t()
