import sys
import aiohttp_cors
from aiohttp import web


from routes import init_routes
from templates import init_templates


# Application factory
def init_app(argv=None) -> web.Application:
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    init_templates(app)
    init_routes(app, cors)
    return app


def main(argv):
    application = init_app()
    web.run_app(application,
                host='127.0.0.1',
                port=8080)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
