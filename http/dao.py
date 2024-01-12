import logging
import mysql.connector
import sys
sys.path.append('cgi/')
import db_ini

def get_db():
    return mysql.connector.connect(**db_ini.connection_params)


class Products:
    def get_all(self) :
        sql = "SELECT * FROM products"
        res = []
        try:
            db = get_db()
            with db.cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    res.append( dict( zip(cursor.column_names, map( str, row ) ) ) )
        except mysql.connector.Error as err:
            logging.error( 'DAO Product', { 'sql': sql, 'err' : str( err ) } )
            raise RuntimeError()
        except Exception as err:
            logging.error( 'DAO Product', { 'exc': err } )
            raise RuntimeError()
        else:
            return res
        

class Auth :
    def get_user_id(self, token:str ) -> str | None :
        sql = "SELECT COUNT(id) FROM users WHERE id=%s"
        try:
            db = get_db()
            with db.cursor() as cursor:
                cursor.execute(sql, ( token, ) )
                cnt = cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logging.error( 'DAO Auth', { 'sql': sql, 'err' : str( err ) } )
            raise RuntimeError()
        except Exception as err:
            logging.error( 'DAO Auth', { 'exc': err } )
            raise RuntimeError()
        else:
            return token if cnt == 1 else None
        

class Carts:
    def add_cart(self, user_id, product_id):
        sql = f"INSERT INTO carts (user_id, product_id) VALUES({user_id}, {product_id})"
        try:
            db = get_db()
            with db.cursor() as cursor:
                cursor.execute(sql)
                db.commit()
        except mysql.connector.Error as err:
            logging.error( 'DAO Cart', { 'sql': sql, 'err' : str( err ) } )
            raise RuntimeError()
        except Exception as err:
            logging.error( 'DAO Cart', { 'exc': err } )
            raise RuntimeError()
        else:
            return "OK"