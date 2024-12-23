import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def scan_port(host, port):
    """Проверяет, открыт ли порт на хосте."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Таймаут 0.5 секунды
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return port, True
        else:
            return port, False
    except socket.error:
        return port, False

def threaded_port_scanner(host, start_port=1, end_port=1024, max_threads=100):
    """Многопоточный сканер портов с progress bar."""
    open_ports = []
    total_ports = end_port - start_port + 1

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Создаём задачи для сканирования портов
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        # Используем tqdm для отображения progress bar
        for future in tqdm(as_completed(futures), total=total_ports, desc="Сканирование портов"):
            port = futures[future]
            try:
                port, is_open = future.result()
                if is_open:
                    print(f"\nПорт {port} открыт")
                    open_ports.append(port)
            except Exception as e:
                print(f"\nОшибка при сканировании порта {port}: {e}")

    return sorted(open_ports)

def get_valid_port(prompt, default):
    """Получает и валидирует ввод порта от пользователя."""
    while True:
        port_input = input(prompt).strip()
        if not port_input:
            return default
        if port_input.isdigit():
            port = int(port_input)
            if 1 <= port <= 65535:
                return port
        print("Пожалуйста, введите корректный номер порта (1-65535).")

if __name__ == "__main__":
    target_host = input("Введите имя хоста или IP-адрес: ").strip()
    if not target_host:
        print("Хост не может быть пустым.")
        exit()

    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"Разрешенный IP-адрес: {target_ip}")
    except socket.gaierror:
        print("Не удалось разрешить хост. Проверьте правильность ввода.")
        exit()

    start_port = get_valid_port("Введите начальный порт (по умолчанию 1): ", 1)
    end_port = get_valid_port("Введите конечный порт (по умолчанию 1024): ", 1024)
    max_threads = get_valid_port("Введите максимальное количество потоков (по умолчанию 100): ", 100)

    if start_port > end_port:
        print("Начальный порт не может быть больше конечного порта.")
        exit()

    print(f"\nСканирование хоста {target_host} ({target_ip}) с портов {start_port} до {end_port} с использованием {max_threads} потоков...\n")
    open_ports = threaded_port_scanner(target_ip, start_port, end_port, max_threads)
    print(f"\nСканирование завершено. Открытые порты: {open_ports}")