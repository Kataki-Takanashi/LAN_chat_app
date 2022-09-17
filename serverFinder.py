import socket
import threading


class test:
    def __init__(self):
        self.port = 8000
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.make_server = True

    def test(self, device):
            try:
                self.my_socket.connect((device, self.port))
                self.make_servermake_server = False
                #print(f"Connected to {device}")
                return device
            except socket.error as error:
                return False
                #print(error)
    def threadTeast(self, devices):
        def start_search_thread(devices):
            for i in devices:
                search_thread = threading.Thread(
                    target=serch_thread,
                    args=(i,),  # the list of argument for the function
                    daemon=True
                )

                search_thread.start()

        self.connectable_device = False  # placeholder

        def serch_thread(device):
            try:
                self.my_socket.connect((device, self.port))
                self.make_server = False
                self.connectable_device = device
                print(f"Connected to {device}")
                return True
            except socket.error as error:
                # logger.error(f'{error} on {device}')
                return False
            finally:
                self.my_socket.close()
                return

        start_search_thread(devices)

        return self.connectable_device


