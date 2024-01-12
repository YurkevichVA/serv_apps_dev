#!C:/Users/bekke/AppData/Local/Programs/Python/Python312/python.exe

import os

query_params = {k: v for k, v in (pair.split('=') for pair in os.environ['QUERY_STRING'].split('&'))}
lang = query_params['lang']
id = query_params['id']
resource = {
    'uk': 'Товар',
    'en': 'Product',
}
lang = lang if lang in resource else 'uk'

print("Content-Type: text/html")
print("")
print(f"""<!DOCTYPE html>
<html lang={lang}>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{resource[lang]}</title>
  </head>
  <body>
    <h1>{resource[lang]} {id}</h1>
  </body>
</html>
""")