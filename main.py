import socket
import json
import os

def receive_message(port):
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 允许地址重用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('0.0.0.0', port))

    # 开始监听连接，最大连接数为5
    server_socket.listen(5)
    print(f"Server is listening on port {port}...")

    import utils

    # 接受连接
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # 接收数据
        data = client_socket.recv(1024)
        text = data.decode('utf-8')
        print(f"Received data: {text}")

        utils.copy_verification_code(text)

        # 关闭客户端连接
        client_socket.close()



def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    port = config['port']
    receive_message(port)
    # 其他代码...

if __name__ == "__main__":
    main()