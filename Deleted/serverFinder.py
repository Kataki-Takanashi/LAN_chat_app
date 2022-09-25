import logging
import socket
import threading
import random
import time

logger = logging.getLogger(__name__)
stream = logging.StreamHandler()
file = logging.FileHandler('../server.log')
stream.setLevel(logging.WARNING)
file.setLevel(logging.ERROR)
formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
stream.setFormatter(formater)
file.setFormatter(formater)
logger.addHandler(stream)
logger.addHandler(file)

class test:
    def __init__(self):
        self.port = 8000

        self.make_server = True

    def test(self, device):
        """
        Deprecated
        :param device:
        :return:
        """
        try:
            #self.my_socket.connect((device, self.port))
            self.make_servermake_server = False
            #print(f"Connected to {device}")
            return device
        except socket.error as error:
            return False
            #print(error)

    def threadTeast(self, devices):
        def start_search_thread(devises):
            for i in devises:
                search_thread = threading.Thread(
                    target=serch_thread,
                    args=(i,),  # the list of argument for the function
                    daemon=True
                )

                search_thread.start()

        self.connectable_device = False  # placeholder

        def serch_thread(device):
            try:
                time.sleep(random.randint(0, 5))
                self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.my_socket.connect((device, self.port))
                self.my_socket.close()
                self.make_server = False
                self.connectable_device = device
                print(f"Connected to {device}")
                return True
            except socket.error as error:
                logger.error(f'{error} on {device}')
                return False
            finally:
                self.my_socket.close()
                return

        start_search_thread(devices)

        return self.connectable_device


# if __name__ == '__main__':
#     test.threadTeast(test(), ['192.168.4.22', '192.168.4.24', '192.168.4.25'])