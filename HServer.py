import socket
import threading


clients = {}
clients_lock = threading.Lock()


def broadcast(message, sender_socket=None):
    with clients_lock:
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    pass


def handle_client(client_socket, client_address):
    try:
        nickname = client_socket.recv(1024).decode('utf-8')

        with clients_lock:
            clients[client_socket] = nickname

        print(f'Клиент {client_address} зарегистрирован как: {nickname}')
        broadcast(f'>>> {nickname} ворвался в чат!\n')
        client_socket.send(f'Server: Привет, {nickname}! Ты в чате.'.encode('utf-8'))

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            broadcast(f'{nickname}: {message}', client_socket)
            print(f'[{nickname}]: {message}')

    except Exception as e:
        print(f'Server: Ошибка с клиентом {client_address}: {e}')
    finally:
        with clients_lock:
            if client_socket in clients:
                name = clients[client_socket]
                del clients[client_socket]
                broadcast(f'<<< {name} покинул чат.')

        client_socket.close()
        print(f'Server: Связь с {client_address} разорвана')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5001))
server_socket.listen()

print('Сервер запущен и ждет подключений...')

while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
    thread.start()