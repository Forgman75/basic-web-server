# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

BASE_DIR = Path(__file__).resolve().parent
# Путь к HTML-файлу
HTML_DIR = BASE_DIR / "html"
# Путь к CSS-файлу
CSS_DIR = BASE_DIR / "css"

class MyServer(BaseHTTPRequestHandler):
    """ 
        Специальный класс, который отвечает за 
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        # Отбрасываем ?query и #fragment, нормализуем путь
        raw = self.path.split("?", 1)[0].split("#", 1)[0]
        rel = raw.lstrip("/")

        # "/" и "" -> главная страница
        if rel == "":
            rel = "contacts.html"

        # Определяем запрашиваемый файл
        if self.path == "/" or self.path == "/contacts.html":
            file_path = HTML_DIR / "contacts.html"
            content_type = "text/html; charset=utf-8"
        elif self.path == "/form":
            file_path = HTML_DIR / "form.html"
            content_type = "text/html; charset=utf-8"
        elif self.path == "/styles.css":
            file_path = CSS_DIR / "styles.css"
            content_type = "text/css; charset=utf-8"
        
        else:
            self.send_error(404, "File not found")
            return
      
        # Открываем HTML-файл
        try:
            with open(file_path, "rb") as file:
                html = file.read()
        except FileNotFoundError:
            self.send_error(404, f"Not found: {file_path.name}")
            return


        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", content_type) # Отправка типа данных, который будет передаваться
        self.end_headers() # Завершение формирования заголовков ответа
        self.wfile.write(html) # Тело ответа

    def do_POST(self):
        """Обработка POST-запросов."""

        # Проверяем адрес запроса
        if self.path != "/submit":
            self.send_error(404, "Page not found")
            return

        # Получаем размер переданных данных
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            content_length = 0

        # Читаем данные из запроса
        post_data = self.rfile.read(content_length) if content_length else b""

        # Декодируем данные и преобразуем в словарь
        data = parse_qs(post_data.decode("utf-8", errors="replace"))

        # Получаем значение поля message
        name    = data.get("name",    [""])[0]
        email   = data.get("email",   [""])[0]
        message = data.get("message", [""])[0]

        # Выводим полученные данные в консоль
        print(f"Имя: {name} | Почта: {email} | Сообщение: {message}")

        # Отправляем ответ клиенту
        response = "Сообщение успешно получено сервером!".encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)


if __name__ == "__main__":        
    # Инициализация веб-сервера, который будет по заданным параметрах в сети 
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")