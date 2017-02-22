import configparser
import os


class CustomConfigParser(configparser.ConfigParser):
    def __init__(self, file_name="config.ini", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = os.path.dirname(__file__)
        self.file_path = os.path.abspath(os.path.join(self.base_path, "..", "..", "configs", file_name))
        try:
            self.config_file = open(self.file_path, "r+")
        except FileNotFoundError:
            raise FileNotFoundError ("Configuration file with name %s wasn't found" % file_name)
        self.read_file(self.config_file)

    def get_api_url(self, port=8000):
        api_url = self['API_URL']
        return api_url['url'] + ':' + str(port)

    def get_db_connection_string(self):
        return self['DB']['connection_string']

    def get_headers(self):
        return dict(self['HEADERS'])

    def get_fb_params(self):
        return dict(self['FB'])

    def get_payment_params(self):
        return dict(self['PAYMENT'])


class ApiEndpointsParser(configparser.ConfigParser):
    def __init__(self, file_name="api_endpoints_config.ini", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = os.path.dirname(__file__)
        self.file_path = os.path.abspath(os.path.join(self.base_path, "..", "..", "configs", file_name))
        try:
            self.config_file = open(self.file_path, "r+")
        except FileNotFoundError:
            raise FileNotFoundError ("Configuration file with name %s wasn't found" % file_name)
        self.read_file(self.config_file)

    def get_api_endpoints(self):
        return dict(self['API_ENDPOINTS'])


class ErrorCodesParser(configparser.ConfigParser):
    def __init__(self, file_name="error_codes.ini", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = os.path.dirname(__file__)
        self.file_path = os.path.abspath(os.path.join(self.base_path, "..", "..", "configs", file_name))
        try:
            self.config_file = open(self.file_path, "r+")
        except FileNotFoundError:
            raise FileNotFoundError("Configuration file with name %s wasn't found" % file_name)
        self.read_file(self.config_file)
        self.codes = self.get_error_codes()

    def get_error_codes(self):
        return dict(self['ERROR_CODES'])

    def get_code_for_message(self, search_message):
        result = []
        for code, message in self.codes.items():
            if message == search_message:
                result.append(code)
        if result:
            return result
        print("Message '{message}' is not found in error codes list.".format(message=search_message))
