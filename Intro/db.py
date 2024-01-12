import mysql.connector
import hashlib;

db_ini = {
    "host": "localhost",
    "port": 3307,
    "database": "py201",
    "user": "py201_user",
    "password": "py201_pass",
    "charset": "utf8mb4",
    "use_unicode": True,
    "collation": "utf8mb4_unicode_ci"
}

db_connection = None

product = {
    "name" : "Коробка НП",
    "price": 28.50,
    "img_url": "box3.png"
}

cart = {
    'user_id' : 100628717100859394,
    'product_id' : 100628717100859393
}

user = {
    "login": "user",
    "password": "123",
    "avatar": "user.png"
}

def add_product(name:str, price:float, id:int|None = None, img_url:str|None = None) :
    sql = f"INSERT INTO products (name, price, img_url) VALUES('{name}', {price}, '{img_url}')"
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
            db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Insert product OK")


def create_products() :
    sql = '''
    CREATE TABLE IF NOT EXISTS products(
        `id` BIGINT UNSIGNED DEFAULT (UUID_SHORT()),
        `name` VARCHAR(64) NOT NULL,
        `price` FLOAT NOT NULL,
        `img_url` VARCHAR(256) NULL
        ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
    '''

    try:
        db_connection.cursor().execute(sql)
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Create products OK")


def create_users() :
    sql = '''
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT UNSIGNED PRIMARY KEY DEFAULT (UUID_SHORT()),
        password CHAR(32) NOT NULL,
        login VARCHAR(32) NOT NULL,
        avatar VARCHAR(256) NULL
    ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
    '''
    try:
        db_connection.cursor().execute(sql)
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Create users OK")


def add_user(login:str, password:str, avatar:int|None = None) :
    password = hashlib.md5( password.encode() ).hexdigest()
    sql = f"INSERT INTO users (login, password, avatar) VALUES('{login}', '{password}', '{avatar}')"
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
            db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Insert user OK")


def create_carts() :
    sql = '''
    CREATE TABLE IF NOT EXISTS carts (
        id BIGINT UNSIGNED PRIMARY KEY DEFAULT (UUID_SHORT()),
        user_id BIGINT UNSIGNED NOT NULL,
        product_id BIGINT UNSIGNED NOT NULL
    ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
    '''
    try:
        db_connection.cursor().execute(sql)
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Create carts OK")


def add_cart(user_id: int, product_id: int):
    sql = f"INSERT INTO carts (user_id, product_id) VALUES({user_id}, {product_id})"
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
            db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("INSERT INTO carts ok")


def main() -> None:
    global db_connection
    try:
        db_connection = mysql.connector.connect( **db_ini )
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Connection OK")

    sql = "SELECT * FROM users"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)
    
    sql = "SELECT * FROM products"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)

    # create_products()
    # add_product( **product )
    # create_users()
    # add_user( **user )  
    # create_carts()
    # add_cart(**cart)


if __name__ == "__main__":
    main()