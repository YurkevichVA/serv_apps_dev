#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe

import api_controller
import json
import logging
import sys
sys.path.append('../../')
import dao

class ProductController ( api_controller.ApiController ) :
  
  def do_get( self ) :
    try:
      res = dao.Products().get_all()
    except:
      self.send_response( 500, "Internal Error", 
                         meta={ "service": "product", "count": 0, "status": 500 }, 
                         data={ "message" : "Server error, see logs for details" } )
    else:
      self.send_response( 200, "OK", 
                         meta={ "service" : "product", "count" : len(res), "status": 200 }, 
                         data=res )


  def do_post( self ) :
    auth_token = self.get_bearer_token_or_exit()
    # робота з ітлом запиту. По схемі CGI (і не тільки) тіло запиту передається у stdin
    request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
    try:
      body_data = json.loads( request_body )
    except:
      self.send_response(400, 'Bad request', { 'message' : "Body must be valid JSON " } )
    if not ( 'name' in body_data and 'price' in body_data ):
      self.send_response(400, 'Bad request', { 'message' : "Body must include 'name' and 'price' " } )
    db = self.get_db_or_exit()
    sql = "INSERT INTO products (name, price, img_url) VALUES(%(name)s, %(price)s, %(image)s)"
    try:
        with db.cursor() as cursor:
            cursor.execute( sql, body_data )
            db.commit()
    except:
      self.send_response( 500, "Internal Error", meta={ "service": "product", "count": 0, "status": 500 }, data={ "message" : "Server error, see logs for details" } )
    else:
      self.send_response( 201, "OK", meta={ "service" : "product", "count" : 1, "status": 201 }, data={"message" : "Created" } )
    

ProductController().serve()

'''
REST - Representation State Transfer - архітектура застосунку, як правило призначена для роботи з API до принципів якої належать:
(приклади у розумінні REST API з HTTP протоколом)
- єдиний інтерфейс
  = запити мають однакову (схожу) семантику, наприклад, GET завжди означає запит на читання, параметр 'page' - номер сторінки тощо
  = однакові (схожі) принципи передачі даних, наприклад, 'page' в URL-параметрах, дані про мову - у заголовку тощо
  = єдиний формат відповідей сервера, у т.ч. про помилки, наприклад, у всіх відповідях є поле 'status', у разі, якщо статус - помилка, то є поле 'message'
  = включення до відповідей окремих деталей запиту (як їх розібрав сервер)
- відсутність збереження стану - незалежність від попередніх запитів
  = не повинно бути кешування (або значно обмежене)
  = немає утримання авторизації - кожен запит містить у собі дані для авторизації (сесій немає, використання Cookie обмежене)
  = кожен запит як новий (не залежить від попередньої історії)


Дії для впровадження REST
- задаємо семантику HTTP-методів
  CRUD: GET(R) POST(C) PUT(U) DELETE(D)
- задаємо типову структуру відповіді

GET /auth                   
200 OK                    |    200 OK  /  401 Unathorized
{                         |    {
  meta: {                 |      meta: {
    service: "auth",      |        service: "auth",
    status: 200,          |        status: 401,
    scheme: "Basic"       |        scheme: "Basic"
  },                      |      },
  data: {                 |      data: {
    scheme: "Bearer",     |        message: "Credentials rejected"
    token: "12344321",    |        
    expires: 100500600    |        
  }                       |      }
}                         |    }

GET /product                   
200 OK                    |    200 OK  /  401 Bad Request
{                         |    {
  meta: {                 |      meta: {
    service: "product",   |        service: "product",
    status: 200,          |        status: 400,
    count: 15             |        count: 0
  },                      |      },
  data: [                 |      data: {
    {product1},           |        message: "Missing parametr 'page'"
    ....,                 |        
    {product15}           |        
  ]                       |      }
}                         |    }

GET /product/123                   
200 OK                    |    200 OK  /  401 Not Found
{                         |    {
  meta: {                 |      meta: {
    service: "product",   |        service: "product",
    status: 200,          |        status: 404,
    requestedId: 123      |        requestedId: 123
  },                      |      },
  data: {                 |      data: {
    name : product1       |        message: "Product '123' does not exist"
  }                       |      }
}                         |    }
'''