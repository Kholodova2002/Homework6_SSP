
import socket
import threading

def handle_client(conn, addr):
    """Функция для обработки клиента в отдельном потоке."""
    print(f"[Тред] Начало обработки клиента {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                # Клиент отключился
                print(f"[Тред] Клиент {addr} отключился.")
                break
            message = data.decode('utf-8')
            print(f"[{addr}] Получено: {message}")
            conn.sendall(data)  # Отправляем обратно (эхо)
    except ConnectionResetError:
        print(f"[Тред] Соединение с клиентом {addr} было разорвано.")
    finally:
        conn.close()
        print(f"[Тред] Завершена обработка клиента {addr}")

def start_multithreaded_server(host='0.0.0.0', port=9090, max_connections=5):
    """Запускает многопоточный эхо-сервер."""
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Опция SO_REUSEADDR позволяет быстро переиспользовать тот же порт
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((host, port))
        print(f"[СЕРВЕР] Запущен на {host}:{port}")
    except socket.error as e:
        print(f"[СЕРВЕР] Не удалось привязать сокет к {host}:{port}: {e}")
        return

    # Начинаем прослушивание входящих соединений
    server_socket.listen(max_connections)
    print("[СЕРВЕР] Ожидание подключений...")

    try:
        while True:
            # Принимаем подключение от клиента
            conn, addr = server_socket.accept()
            print(f"[СЕРВЕР] Клиент подключился: {addr}")
            
            # Создаем и запускаем новый поток для клиента
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[СЕРВЕР] Остановка сервера по запросу пользователя (Ctrl+C)...")
    finally:
        server_socket.close()
        print("[СЕРВЕР] Сокет сервера закрыт. Сервер остановлен.")

if __name__ == "__main__":
    # Запрос хоста и порта у пользователя с использованием значений по умолчанию
    host_input = input("Введите хост сервера (по умолчанию 0.0.0.0): ").strip()
    if not host_input:
        host_input = '0.0.0.0'
    port_input = input("Введите порт сервера (по умолчанию 9090): ").strip()
    if port_input.isdigit():
        port_input = int(port_input)
    else:
        port_input = 9090
    max_conn_input = input("Введите максимальное количество подключений (по умолчанию 5): ").strip()
    if max_conn_input.isdigit():
        max_connections = int(max_conn_input)
    else:
        max_connections = 5

    start_multithreaded_server(host_input, port_input, max_connections)