from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import appconfig
import inspect
import importlib
import routes
import random
import time
import json


class MainHandler(BaseHTTPRequestHandler) :
    sessions = {}

    def __init__(self, request, client_address, server) -> None:
        self.response_headers = dict()
        super().__init__(request, client_address, server)

    def do_GET(self) -> None:
        # для початку відокремлюємо query string TODO відокремити hash(#)
        parts = self.path.split('?')
        path = parts[0]
        query_string = parts[1] if len(parts) > 1 else None

        if '../' in path or '..\\' in path:
            self.send_404()
            return
        
        filename = appconfig.WWWROOT_PATH + path
        if os.path.isfile( filename ) :
            self.flush_file( filename )
            return
        
        # Робота з сесією
        cookies_header = self.headers.get('Cookie', '')
        cookies = dict( cookie.split( '=' ) for cookie in cookies_header.split( '; ' ) if '=' in cookie)
        if 'session-id' in cookies and cookies['session-id'] in MainHandler.sessions:
            self.session = MainHandler.sessions[cookies['session-id']]
        else: # Немає сесії для запиту
            # стартуємо сесію - генеруємо id, якого немає у sessions
            while True:
                session_id = str( random.randint(1000, 9999) )
                if not session_id in MainHandler.sessions :
                    break
            # встановлюємо заголовок Cookie
            self.response_headers['Set-Cookie'] = f'session-id={session_id}'
            # утворюємо сховище для даних
            MainHandler.sessions[session_id] = {
                'id' : session_id,
                'timestamp' : time.time()
            }
            self.session = MainHandler.sessions[ session_id ]
        # Кінець роботи з сесією
            
        path_info = routes.parse_path(path)

        try:
            controller_module = importlib.import_module( path_info["controller"] )
            controller_class = getattr( controller_module, path_info["controller"] )
            controller_instance = controller_class( self )
            controller_action = getattr( controller_instance, path_info["action"] )
        except:
            controller_action = None

        if controller_action:
            controller_action()
        else:
            self.send_404()
        
        return

    def send_view(self, view_name:str=None, layout_name:str=None) :
        controller_instance = inspect.currentframe().f_back.f_locals['self']

        if layout_name == None:
            layout_name = appconfig.DEFAULT_VIEW

        if view_name == None:
            controller_short_name = controller_instance.__class__.__name__.removesuffix("Controller").lower()
            action_name = inspect.currentframe().f_back.f_code.co_name
            view_name = f'{appconfig.VIEW_PATH}/{controller_short_name}/{action_name}.html'

        if not os.path.isfile(layout_name) or not os.path.isfile(view_name) :
            self.send_404()
            return

        for k, v in self.session.items() :
            MainHandler.sessions[self.session['id']][k] = v

        self.send_response(200, 'OK')
        self.send_header('Content-Type', "text/html; charset=utf-8")
        for header, value in self.response_headers.items():
            self.send_header(header, value)

        self.end_headers()
        with open(view_name) as view:
            view_content = view.read()
            view_data = getattr(controller_instance, 'view_data', None)
            if view_data:
                for k, v in view_data.items() :
                    view_content = view_content.replace( k, str( v ) )
            with open(layout_name) as layout:
                self.wfile.write( layout.read().replace( '<!-- RenderBody -->', view_content ).encode('cp1251') )

    def flush_file( self, filename ) :

        if not os.path.isfile( filename ) :
            self.send_404()
            return
        
        ext = filename.split('.')[-1]
        if ext in ('css', 'html'):
            content_type = 'text/' + ext
        elif ext == 'js':
            content_type = 'text/javascript'
        elif ext == 'ico':
            content_type = 'image/x-icon'
        elif ext in ('pnt', 'bmp'):
            content_type = 'image/' + ext
        elif ext in ('jpg', 'jpeg'):
            content_type = 'image/jpeg'
        elif ext in ('py', 'ini', 'env', 'jss', 'php'):
            self.send_404()
            return
        else:
            content_type = 'application/octet-stream'

        self.send_response(200, 'OK')
        self.send_header('Content-Type', content_type)
        self.end_headers()
        with open( filename, "rb" ) as file:
            self.wfile.write( file.read() )

    def send_404(self) -> None:
        self.send_response(404, 'Not Found')
        self.send_header('Status', '404 Not Found')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write( 'Resource for request not found'.encode() )

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        return None # відключити логування запитів у консоль


def main() -> None:
    if os.path.exists("sessions.json"):
        with open("sessions.json", 'r') as file:
            MainHandler.sessions = json.load(file)
    http_server = HTTPServer( ('127.0.0.1', 81), MainHandler )
    try:
        print(" Server starting...")
        http_server.serve_forever()
    except:
        print( "Server stopped" )
        with open("sessions.json", 'w') as file:
            json.dump( MainHandler.sessions, file )


if __name__ == "__main__":
    main()


'''
Модуль HTTP
Альтернативний підхід до створення серверних програм - використання власних модулів/пакетів/бібліотек мов програмування (http.server).
Такі програми складаються з двох блоків:
- запуск/зупинка сервера, підготовка інжекцій, конфігурацій тощо
- обслуговування (слухання) запитів
Оброблення запитів покладається на клас-нащадок BaseHTTPRequestHandler
Запуск сервера - на об'єкт HTTPServer
Особливості (відмінності від CGI)
- сервер запускається засобами мови (Python), шлях до інтерпретатора зазначати не треба, сторонніх серверів також не вимагається
- серверу потрібен вільний порт для запуску
- метод-обробник не отримує параметрів (типу Request/Response), всі дані передаються як поля/властивості класу (BaseHTTPRequestHandler)
- тіло відповіді формується записом у поле wfile у бінарному виді (рядок треба перевести в байти)
- print() виводить у консоль запуску, у відповідь ці дані не потрапляють
- методи обробника відповідають за методи запиту (do_GET, do_POST, ...) і всі запити потрапляють у них (у т.ч. запити на файл, навіть 
якщо файл існує). Задача звернення до файлів має бути вірішена самостійно

'''

'''
- Структура проєкту
Серверні проєкти, які складаються з двох частин - код та статика, прийнято розподіляти таким чином, щоб прямий доступ із браузерв було обмежено
статичними ресурсами. Іншими словами, пошук файлів (чи інших ресурсів) має бути обмежений окремою папкою (public, wwwroot, www, static, html)
'''

'''
Cookie це
а) заголовки HTTP-пакету, які за вимогами стандартів повинні включатись у всі запити клієнтом
б) елемети (частішеза все - файли), які зберігає та обслуговує клієнт (браузер) з метою включення їх до запитів та забезпечення достатнього часу
їх існування (у т.ч. після перезапуску клієнта)

Cookie встановлюються заголовком Set-Cookie: name=value;expires=[DateTime];path=/
Якщо треба декілька Cookie, вони передаються окремими заголовками Set-Cookie

Отримавши запит з таким заголовком клієнт (браузер) повинен зберігати ці дані і в усі запити (за шаблоном path) протягом терміну (expires)
включати заголовоком
Cookie: name=value; name2=value; name3=value3
у якому всі Cookie включаються черех "; ", тільки імена та значення (інше ігнорується)

Видалення Cookie - повторне її встановлення з "минулим" терміном
Встановити також можна засобами JS через document.cookie
'''