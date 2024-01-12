from starter import MainHandler
import inspect
import appconfig
import os

class HomeController:
    def __init__(self, handler:MainHandler) -> None:
        self.handler = handler

    def index(self):
        self.handler.session['data'] = 'HomeController'
        self.view_data = {
            '@session-timestamp': self.handler.session['timestamp']
        }
        self.handler.send_view()

    def about( self ) :
        self.handler.send_view()

    def privacy(self):
        self.handler.send_view()