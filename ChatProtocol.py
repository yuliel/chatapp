DELIMITER = "|"
LOGIN_COMMAND = "login"
CLOSE_COMMAND = "close"
CONNECTED_COMMAND = "connected"
AUTHORIZE_COMMAND = "authorize"
SEND_MESSAGE_COMMAND = "sendto"
WCONN_COMMAND = "wconn"

OK_STATUS = "ok"

class ChatProtocol:
    @staticmethod
    def build_login(username, pwd):
        return f"{LOGIN_COMMAND}{DELIMITER}{username}{DELIMITER}{pwd}"

    @staticmethod
    def parse_login(data):
        return data.split(DELIMITER)

    @staticmethod
    def build_close_connection():
        return f"{CLOSE_COMMAND}{DELIMITER}"

    @staticmethod
    def build_get_connected_users():
        return f"{CONNECTED_COMMAND}{DELIMITER}"

    @staticmethod
    def parse_connected(data):
        return data.split(DELIMITER)

    @staticmethod
    def build_authorize(username):
        return f"{AUTHORIZE_COMMAND}{DELIMITER}{username}"

    @staticmethod
    def build_send_message(target_user, msg):
        return f"{SEND_MESSAGE_COMMAND}{DELIMITER}{target_user}{DELIMITER}{msg}"

    @staticmethod
    def parse_authorize(data):
        return data.split(DELIMITER)

    @staticmethod
    def parse_send_message(data):
        return data.split(DELIMITER)

    @staticmethod
    def build_set_wconn(ip, port):
        return f"{WCONN_COMMAND}{DELIMITER}{ip}{DELIMITER}{port}"

    @staticmethod
    def parse_set_wconn(data):
        return data.split(DELIMITER)

