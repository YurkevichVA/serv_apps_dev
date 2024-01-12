from starter import MainHandler
import dao

class ShopController:
    def __init__(self, handler: MainHandler) -> None:
        self.handler = handler

    def index(self):
        products_list = dao.Products().get_all()
        print(products_list)
        self.handler.session['data'] = 'ShopController'
        self.view_data = {"@products" : ''}
        for product in products_list:
            self.view_data['@products'] += f'<h3>{product['name']}</h3>'
            self.view_data['@products'] += f'<p>{product['price']}</p>'
            self.view_data['@products'] += f'<img src="/img/{product['img_url']}" width="150">'
        self.handler.send_view()

    def cart( self ) :
        self.handler.send_view()