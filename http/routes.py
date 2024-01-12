predefined_urls = {
    "/about" : "/home/about",
    "/cart" : "/shop/cart"
}

def parse_path(path:str) -> dict:
    path = predefined_urls.get(path, path)
    parts = path.split('/')
    return {
        "controller" : (parts[1].capitalize() if parts[1] != '' else 'Home') + 'Controller',
        "action" : parts[2] if len(parts) > 2 and parts[2] != '' else 'index',
        "lang" : "uk",
        "path-id" : None
    }