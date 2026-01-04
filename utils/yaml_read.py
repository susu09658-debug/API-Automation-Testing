import os.path
import yaml


class ReadYaml:
    def get_yaml_file(self, yaml_path):
        if not os.path.isfile(yaml_path):
            return None
        case_list = []
        try:
            with open(yaml_path, 'r', encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)
                temp_data = yaml_data[0]
                base_info = temp_data.get('BaseInfo')
                for testcase in temp_data.get('TestCase'):
                    parameter = [base_info, testcase]
                    case_list.append(parameter)
                return case_list
        except Exception as e:
            print(e)


class YamlUtil:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.read_yaml = ReadYaml()

    def get_case_url(self):
        case_data = self.read_yaml.get_yaml_file(self.yaml_path)
        case_url = case_data[0][0].get('url')
        return case_url

    def get_case_method(self):
        case_data = self.read_yaml.get_yaml_file(self.yaml_path)
        case_method = case_data[0][0].get('method')
        return case_method

    def get_case_header(self):
        case_data = self.read_yaml.get_yaml_file(self.yaml_path)
        case_header = case_data[0][0].get('header')
        return case_header

    def get_case_name(self, index):
        case_data = self.read_yaml.get_yaml_file(self.yaml_path)
        case_name = case_data[index][1].get('CaseName')
        return case_name

    def get_case_body(self, index):
        body_info = {}
        case_data = self.read_yaml.get_yaml_file(self.yaml_path)
        case_body = case_data[index][1]
        body_types = ['data', 'json', 'params']
        for body_type in body_types:
            if body_type in case_body:
                body_info['body_type'] = body_type
                body_info['body_data'] = case_body.get(body_type)
                return body_info
        return None
