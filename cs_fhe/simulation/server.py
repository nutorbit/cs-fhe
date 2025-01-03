import socket
from concrete import fhe

class FHEServer:
    def __init__(
        self, 
        host: str = 'localhost', 
        port: int = 65432, 
        buffer_size: int = 10240 * 2,
        server_zip: str = 'server.zip'
    ):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server = fhe.Server.load(server_zip)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)  # Listen for two clients
        print(f"Server listening on {self.host}:{self.port}")
        for _ in range(2):
            conn, addr = self.socket.accept()
            print(f"Connected by {addr}")
            self.connections.append(conn)

    def send_client_specs(self):
        serialized_client_specs = self.server.client_specs.serialize()
        for conn in self.connections:
            conn.sendall(serialized_client_specs)

    def receive_data(self):
        serialized_evaluation_keys = []
        serialized_args = []
        for conn in self.connections:
            serialized_evaluation_keys.append(conn.recv(self.buffer_size))
            serialized_args.append(conn.recv(self.buffer_size))
        return serialized_evaluation_keys, serialized_args

    def compute_and_send_result(self, serialized_evaluation_keys: list, serialized_args: list):
        deserialized_evaluation_keys = [fhe.EvaluationKeys.deserialize(ek) for ek in serialized_evaluation_keys]
        deserialized_args = [fhe.Value.deserialize(arg) for arg in serialized_args]

        processed_inputs = []
        for i, arg in enumerate(deserialized_args):
            function_name = 'bank' if i == 0 else 'telco'
            processed_input = self.server.run(
                arg,
                evaluation_keys=deserialized_evaluation_keys[i],
                function_name=function_name
            )
            processed_inputs.append(processed_input)

        added_result = self.server.run(
            *processed_inputs,
            evaluation_keys=deserialized_evaluation_keys[0],
            function_name='add'
        )

        final_result = self.server.run(
            added_result,
            evaluation_keys=deserialized_evaluation_keys[0],
            function_name='half'
        )

        serialized_result = final_result.serialize()
        for conn in self.connections:
            conn.sendall(serialized_result)

    def close(self):
        for conn in self.connections:
            conn.close()
        self.socket.close()


if __name__ == "__main__":
    server = FHEServer()
    server.start()
    server.send_client_specs()
    serialized_evaluation_keys, serialized_args = server.receive_data()
    server.compute_and_send_result(serialized_evaluation_keys, serialized_args)
    server.close()
