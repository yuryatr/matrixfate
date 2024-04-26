from aiohttp import web
from  aiohttp_cors.cors_config import CorsConfig

from index.views import View as indexView


def init_routes(app: web.Application, cors: CorsConfig):
    app.router.add_get('/', indexView, name='main')
