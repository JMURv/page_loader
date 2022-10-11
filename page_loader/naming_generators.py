

def url2name(url):
    name = ''
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    for char in url:
        if char.isalnum():
            name += char
        else:
            name += '-'
    if name[-1] == '-':
        name = name[:-1]
    return name


def generate_assets_name(link, site_name):
    list_of_path = link.split('/')
    filename = list_of_path[-1]
    return f"{site_name}_files/{site_name}-{filename}"
