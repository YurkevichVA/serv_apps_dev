#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe"

import api_controller
import base64
import hashlib
import os
import sys
import json
import re
import mysql.connector
sys.path.append('../')
import db_ini

query_params = None

class AuthController ( api_controller.ApiController ) :

    def do_get( self ) :
        # global query_params
        # 
        # if not 'login' in query_params:
        #     send_response(400, "Bad request", {"message": "Missing required 'login' parameter"})
        # if not 'password' in query_params:
        #     send_response(400, "Bad request", {"message": "Missing required 'password' parameter"})
        # login, password = query_params['login'], query_params['password']
        # Переходимо на авторизацію за схемою Basic
    
        auth_token = self.get_auth_header_or_exit()
        try:
            login, password = base64.b64decode( auth_token, validate=True ).decode().split(':', 1)
        except:
            self.send_response(401, 'Unauthorized', meta={ "service" : "auth", "status": 401, "scheme": "Basic" }, data={ 'message': 'Malformed credentials: Basic scheme required' } )


        db = self.get_db_or_exit()
        sql = "SELECT * FROM users u WHERE u.`login`=%s AND u.`password`=%s"
        try:
            with db.cursor() as cursor:
                cursor.execute(sql, (login, hashlib.md5(password.encode()).hexdigest()))
                row = cursor.fetchone()
                if row == None:
                    self.send_response( 401, "Unauthorized", meta={ "service" : "auth", "status": 401, "scheme": "Basic" }, data={ "message": "Credentials rejected" } )
                user_data = dict( zip( cursor.column_names, row ) )
                self.send_response( 200, "OK", meta={ "service" : "auth", "status": 200, "scheme": "Basic" }, data={ "auth": "success", "token": str(user_data['id']) } )
        except mysql.connector.Error as err:
            self.send_response(503, "Service Unavailable (do_get)", meta={ "service" : "auth", "status": 503, "scheme": "Basic" }, data=repr(err) )


    def do_post( self ) :
        # send_response(body=dict(os.environ))
        self.send_response( meta={ "service" : "auth", "status": 200, "scheme": "Basic" }, data=str( self.get_bearer_token_or_exit() ) )


    def do_put( self ) :
        auth_token = self.get_bearer_token_or_exit()
        # робота з ітлом запиту. По схемі CGI (і не тільки) тіло запиту передається у stdin
        request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
        try:
            body_data = json.loads( request_body )
        except:
            self.send_response(400, 'Bad request', meta={ "service" : "auth", "status": 400, "scheme": "Basic" }, data={ 'message' : "Body must be valid JSON " } )
        if not ( 'name' in body_data and 'price' in body_data ):
            self.send_response(400, 'Bad request', meta={ "service" : "auth", "status": 400, "scheme": "Basic" }, data={ 'message' : "Body must include 'name' and 'price' " } )
        self.send_response( meta={ "service" : "auth", "status": 401, "scheme": "Basic" }, data={ "token": auth_token,  "body": request_body } )



AuthController().serve()


# Особливість роботи серверів полягає у тому, що стандартні заголовки авторизації вони можуть не передавати в оточення
# Це пояснюється безпекою. Для того щоб передати його до CGI необхідно це прямо зазначити у налаштуваннях хосту
# SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1