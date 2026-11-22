# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

# Путь к HTML-файлу
HTML_DIR = Path(__file__).parent / "html"
# Путь к CSS-файлу
CSS_DIR = Path(__file__).parent / "css"

class MyServer(BaseHTTPRequestHandler):
    """ 
        Специальный класс, который отвечает за 
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        # Определяем запрашиваемый файл
        if self.path == "/":
            file_path = HTML_DIR / "index.html"
            content_type = "text/html; charset=utf-8"
        elif self.path == "/styles.css":
            file_path = CSS_DIR / "styles.css"
            content_type = "text/css; charset=utf-8"

        else:
            self.send_error(404, "File not found")
            return
      
        # Открываем HTML-файл
        with open(file_path, "rb") as file:
            html = file.read()

        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", content_type) # Отправка типа данных, который будет передаваться
        self.end_headers() # Завершение формирования заголовков ответа
        self.wfile.write(html) # Тело ответа

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