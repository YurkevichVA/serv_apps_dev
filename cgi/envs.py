#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe

import os
# os.environ -- dict із змінними оточення (ім'я-значення)

keys = ['REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI', 'REMOTE_ADDR']

envs = "<ul>" + "".join("<li>%s = %s</li>" %(k,v) for k,v in os.environ.items()) + "</ul>"

query_params = { k: v for k,v in ( pair.split('=') for pair in os.environ['QUERY_STRING'].split('&') ) }

lang = query_params['lang']

resource = {
  'uk': 'Вітання',
  'en': 'Greetings',
  'de': 'Hertzlich willkommen'
}

if not lang in resource:
  lang = 'uk'

print("Content-Type: text/html;")
print("") # заголовки від тіла відокремлюються порожнім рядком
print(f"""<!doctype html>
<html>
    <head>
      <title>Py-201</title>
    </head>
    <body>
      <h1>{resource[lang]}</h1>
      {envs}
    </body>
</html>""")

'''
REQUEST_METHOD = GET
QUERY_STRING = 
REQUEST_URI = /
'''