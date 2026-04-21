import socket
import threading

is_connected = True


def receive_messages(client_socket):
    global is_connected
    while is_connected:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('\n[Соединение с сервером разорвано]')
                is_connected = False
                break
            print(f'\r{data.decode("utf-8")}\nЯ: ', end='')
        except:
            is_connected = False
            break


def send_messages(client_socket):
    global is_connected
    while is_connected:
        try:
            message = input('Я: ')

            if not is_connected:
                break

            if message.lower() == '/exit':
                is_connected = False
                break

            client_socket.send(message.encode('utf-8'))
        except:
            break

    client_socket.close()



nickname = input('Введите ваш ник: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5001))
client_socket.send(nickname.encode('utf-8'))


receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
receive_thread.start()

send_messages(client_socket)
print('Вы вышли из чата.')
