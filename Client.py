import socket

def start_echo_client(server_host='localhost', server_port=9090):
    """
    Запускает простой TCP-клиент для эхо-сервера.
    :param server_host: Адрес сервера (по умолчанию 'localhost')
    :param server_port: Порт сервера (по умолчанию 9090)
    """
    # Создаем TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        client_socket.connect((server_host, server_port))
        print(f"Подключено к серверу {server_host}:{server_port}")
    except ConnectionRefusedError:
        print(f"Не удалось подключиться к серверу {server_host}:{server_port}. Убедитесь, что сервер запущен.")
        return

    try:
        while True:
            # Считываем сообщение от пользователя
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                print("Завершение работы клиента.")
                break

            # Отправляем сообщение на сервер
            client_socket.sendall(message.encode('utf-8'))

            # Принимаем ответ от сервера
            data = client_socket.recv(1024)
            if not data:
                print("Сервер закрыл соединение.")
                break
            print(f"Ответ от сервера: {data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("\nКлиент прерван пользователем.")
    finally:
        client_socket.close()
        print("Соединение закрыто.")

if __name__ == "__main__":
    # Опционально: можно запросить хост и порт у пользователя
    server_host = input("Введите хост сервера (по умолчанию localhost): ").strip()
    if not server_host:
        server_host = 'localhost'
    port_input = input("Введите порт сервера (по умолчанию 9090): ").strip()
    if port_input.isdigit():
        server_port = int(port_input)
    else:
        server_port = 9090

    start_echo_client(server_host, server_port)