#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe

import os

print("Content-Type: text/html;")
print("") # заголовки від тіла відокремлюються порожнім рядком
with open( './static/home.html', mode='r' ) as f:
    print( f.read() )