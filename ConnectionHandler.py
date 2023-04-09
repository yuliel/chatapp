import socket
import logging
from ConnectionServer import ConnectionServer
from connection_utils import *
from time import sleep
from ChatProtocol import *


class ConnectionHandler:

    def __init__(self):
        self.__chat_server = self.__connect_chat_server()
        self.__wconn_socket = None

    @staticmethod
    def __connect_chat_server():
        chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ConnectionServer.get_chat_server_address()
        while True:
            try:
                chat_server.connect(server_address)
                break
            except ConnectionError:
                print("Cannot connect chat server. Waiting 5 seconds")
                sleep(5)
        return chat_server

    def start_listener(self, connection_handler):
        self.__wconn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__wconn_socket.bind((WCONN_IP, 0))
        self.__wconn_socket.listen()
        connection_handler.__send_wconn(WCONN_IP, self.__wconn_socket.getsockname()[1])
        conn, address = self.__wconn_socket.accept()
        return conn

    def do_listen(self, conn):
        try:
            return conn.recv(MSG_SIZE).decode()
        except ConnectionResetError:
            print("the main server is down. closing connection")
            self.close_connection()
            exit()

    def __get_server(self):
        return self.__chat_server

    def __switch_server(self):
        self.__chat_server = self.__connect_chat_server()

    def __send_message(self, msg):
        self.__get_server().send(msg.encode())

    def __receive_message(self):
        return self.__get_server().recv(MSG_SIZE).decode()

    def __send_wconn(self, ip, port):
        self.__send_message(ChatProtocol.build_set_wconn(ip, port))

    def login(self, username, pwd):
        try:
            self.__send_message(ChatProtocol.build_login(username, pwd))
            status, msg = ChatProtocol.parse_response(self.__receive_message())
            if status == OK_STATUS:
                logging.info(f"User '{username}' logged in successfully")
                return True
            else:
                logging.warning(f"User '{username}' failed to logged in. {msg}")
                return False
        except Exception:
            logging.error("Error during login")
            return False

    def close_connection(self):
        logging.info(f"closing")
        self.__send_message(ChatProtocol.build_close_connection())

    def authorize(self, username):
        try:
            logging.info(f"authorizing {username}")
            self.__send_message(ChatProtocol.build_authorize(username))
            status, msg = ChatProtocol.parse_response(self.__receive_message())
            if status == OK_STATUS:
                logging.info(f"User '{username}' authorized")
            else:
                logging.warning(f"User '{username}' failed to authorize. {msg}")
        except Exception:
            logging.error("Error during authorize")

    def get_connected_users(self):
        try:
            self.__send_message(ChatProtocol.build_get_connected_users())
            connected, authorized = ChatProtocol.parse_response(self.__receive_message())
            return connected, authorized
        except Exception:
            logging.error("Error during get connected users")
            return None, None

    def send_message(self, target_user, msg):
        try:
            self.__send_message(ChatProtocol.build_send_message(target_user, msg))
            status, msg = ChatProtocol.parse_response(self.__receive_message())
            if status == OK_STATUS:
                logging.info(f"message send")
            else:
                logging.warning(f"couldn't send message: {msg}")
        except Exception:
            logging.error("Error during send_message")




def main():
    logging.basicConfig(level=logging.INFO)
    ConnectionServer.get_chat_server_address()
    ch = ConnectionHandler()
    ch.login("user1", "pwd1")


if __name__ == '__main__':
    main()
