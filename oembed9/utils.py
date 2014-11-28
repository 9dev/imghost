import sys

def del_none(d):
    for key, value in d.items():
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def get_size(sizes, maxw, maxh):
    for size in sizes:
        for x in range(0, len(size)):
            if size[x] == 0:
                size[x] = sys.maxsize
        if maxw >= size[0]:
            if maxh >= size[1]:
                return size
    return sizes[0]

def format_data(data, format):
    data = del_none(data)
    
    if format == 'json':
        import json
        data = json.dumps(data)
    else:
        from dicttoxml import dicttoxml
        data = dicttoxml(data, attr_type=False, custom_root='oembed')
        
    return data
            
def missing(str):
    raise Exception("'%s' parameter is missing in your OEmbed class." % str)
