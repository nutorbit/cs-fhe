import sys
import socket

from concrete import fhe

class FHEClient:
    def __init__(
        self, 
        host: str = 'localhost', 
        port: int = 65432,
        buffer_size: int = 10240 * 2
    ):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None

    def connect(self):
        self.socket.connect((self.host, self.port))

    def receive_client_specs(self):
        serialized_client_specs = self.socket.recv(self.buffer_size)
        client_specs = fhe.ClientSpecs.deserialize(serialized_client_specs)
        self.client = fhe.Client(client_specs)

    def generate_and_send_keys(self):
        self.client.keys.generate()
        serialized_evaluation_keys = self.client.evaluation_keys.serialize()
        self.socket.sendall(serialized_evaluation_keys)

    def encrypt_and_send_data(self, data, function_name):
        arg = self.client.encrypt(data, function_name=function_name)
        serialized_arg = arg.serialize()
        self.socket.sendall(serialized_arg)

    def receive_and_decrypt_result(self, function_name):
        serialized_result = self.socket.recv(self.buffer_size)
        deserialized_result = fhe.Value.deserialize(serialized_result)
        return self.client.decrypt(deserialized_result, function_name=function_name)

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <input_value> <function_name>")
        sys.exit(1)
    
    input_value = int(sys.argv[1])
    function_name = sys.argv[2]
    
    client = FHEClient()
    client.connect()
    client.receive_client_specs()
    client.generate_and_send_keys()
    client.encrypt_and_send_data(input_value, function_name)
    result = client.receive_and_decrypt_result('half')
    print(f"Decrypted result: {result}")
    client.close()