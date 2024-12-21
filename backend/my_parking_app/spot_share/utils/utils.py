import re 
from rest_framework.renderers import JSONRenderer

def camelize(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            data = {camelize(key): value for key, value in data.items()}
        elif isinstance(data, list):
            data = [{camelize(key): value for key, value in item.items()} for item in data]
        return super().render(data, accepted_media_type, renderer_context)