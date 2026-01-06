import os.path
import yaml


class ReadYaml:
    """
    YAML文件读取类
    核心功能：读取指定路径的YAML文件，解析测试用例数据并格式化返回
    """

    def get_yaml_file(self, yaml_path):
        """
        读取并解析YAML文件，提取测试用例数据
        :param yaml_path: YAML文件的完整路径
        :return: 格式化后的测试用例列表，格式为[[base_info, testcase1], [base_info, testcase2]...]；文件不存在返回None
        """
        # 检查传入的路径是否是一个有效的文件，若不是则返回None
        if not os.path.isfile(yaml_path):
            return None
        # 初始化空列表，用于存储最终的测试用例数据
        case_list = []
        try:
            # 以只读模式打开YAML文件，指定编码为utf-8避免中文乱码
            with open(yaml_path, 'r', encoding="utf-8") as f:
                # 安全加载YAML文件内容（safe_load避免执行恶意代码）
                yaml_data = yaml.safe_load(f)
                # 取YAML数据的第一个元素（适配特定的YAML结构）
                temp_data = yaml_data[0]
                # 提取基础信息（如url、method、header等）
                base_info = temp_data.get('BaseInfo')
                # 遍历所有测试用例，将基础信息和单个用例组合后存入列表
                for testcase in temp_data.get('TestCase'):
                    parameter = [base_info, testcase]
                    case_list.append(parameter)
                # 返回格式化后的测试用例列表
                return case_list
        # 捕获并打印解析过程中出现的异常（如YAML格式错误、键不存在等）
        except Exception as e:
            print(e)


class YamlUtil:
    """
    YAML工具类
    封装YAML文件读取和测试用例数据提取的常用方法
    """

    def __init__(self, yaml_path):
        """
        初始化方法，创建实例时自动读取YAML文件并加载测试用例数据
        :param yaml_path: YAML文件的完整路径
        """
        # 保存YAML文件路径到实例属性
        self.yaml_path = yaml_path
        # 创建ReadYaml类的实例，用于读取YAML文件
        self.read_yaml = ReadYaml()
        # 调用读取方法，将解析后的测试用例数据保存到实例属性
        self.case_data = self.read_yaml.get_yaml_file(self.yaml_path)

    def get_case_url(self):
        """
        获取测试用例的基础URL
        :return: BaseInfo中的url值
        """
        # 从第一个用例的基础信息中提取url（默认取第一个用例的基础信息）
        case_url = self.case_data[0][0].get('url')
        return case_url

    def get_case_method(self):
        """
        获取测试用例的请求方法（如GET、POST）
        :return: BaseInfo中的method值
        """
        # 从第一个用例的基础信息中提取请求方法
        case_method = self.case_data[0][0].get('method')
        return case_method

    def get_case_header(self):
        """
        获取测试用例的请求头
        :return: BaseInfo中的header值
        """
        # 从第一个用例的基础信息中提取请求头
        case_header = self.case_data[0][0].get('header')
        return case_header

    def get_case_name(self, index):
        """
        根据索引获取指定测试用例的名称
        :param index: 测试用例在列表中的索引（从0开始）
        :return: 指定索引用例的CaseName值
        """
        # 根据索引提取对应测试用例的名称
        case_name = self.case_data[index][1].get('CaseName')
        return case_name

    def get_case_body(self, index):
        """
        根据索引获取指定测试用例的请求体数据
        支持提取data/json/params三种类型的请求体
        :param index: 测试用例在列表中的索引（从0开始）
        :return: 包含请求体类型和数据的字典，格式为{'body_type': 'data/json/params', 'body_data': 对应数据}；无请求体返回None
        """
        # 初始化空字典，用于存储请求体类型和数据
        body_info = {}
        # 根据索引提取对应测试用例的详细数据
        case_body = self.case_data[index][1]
        # 定义支持的请求体类型列表
        body_types = ['data', 'json', 'params']
        # 遍历请求体类型，匹配到第一个存在的类型后返回对应数据
        for body_type in body_types:
            if body_type in case_body:
                body_info['body_type'] = body_type
                body_info['body_data'] = case_body.get(body_type)
                return body_info
        # 若没有匹配到任何请求体类型，返回None
        return None
