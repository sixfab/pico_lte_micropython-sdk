
def read_file(file_path):
    """
    Function for reading file
    """
    with open(file_path, "r") as file:
        data = file.read()
    return data or {}  


class Auth:
    """
    Class for getting certificates of cloud services
    """
    def __init__(self, config: dict):
        self.config = config
        self.config["auth"] = {}

    def load_certificas(self):
        """
        Function for loading certificates from file
        """
        cacert = read_file("../cert/AmazonRootCA1.pem")
        client_cert = read_file("../cert/pico3.pem")
        client_key = read_file("../cert/pico3.key")
        
        self.config["auth"]["cacert"] = cacert
        self.config["auth"]["client_cert"] = client_cert
        self.config["auth"]["client_key"] = client_key



