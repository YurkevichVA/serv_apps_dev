#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe

import api_controller
import json
import logging
import sys
sys.path.append('../../')
import dao

class CartController ( api_controller.ApiController ) :
  
  def do_post( self ) :
    user_id = dao.Auth().get_user_id( self.get_bearer_token_or_exit() )
    request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
    try:
      body_data = json.loads( request_body )
      dao.Carts().add_cart(user_id, body_data["productId"])
    except Exception as err:
      self.send_response(500, 'Failed', meta={ "service" : "cart", "status": 500, "scheme": "Bearer" }, data={ 'message' : str(err) } )
    self.send_response( 200, "OK", meta={ "service": "cart", "count": 1, "status": 200 }, data={ "token": user_id, "body_data" : body_data } )
    

CartController().serve()