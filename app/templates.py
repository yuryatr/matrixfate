import jinja2
import aiohttp_jinja2
from aiohttp import web


def init_templates(app: web.Application):
    env = aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader('./ui'),
        auto_reload=True,
        enable_async=True
    )
    env.globals.update(
        config=app.config if hasattr(app, 'config') else {},
        STATIC_PREFIX='/static',
        THEME_PATH=''
    )
    app['ui'] = env