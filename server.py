from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer

from common.Config import BASE_CONFIG
from tornado.ioloop import IOLoop

from app import create_app

if __name__ == '__main__':
    app = create_app()
    environment = BASE_CONFIG.get('environment')
    host = BASE_CONFIG.get('host')
    port = BASE_CONFIG.get('port')

    if environment == 'dev':
        app.run(debug=True, host=host, port=port)
    else:
        s = HTTPServer(WSGIContainer(app))
        s.listen(port)
        IOLoop.current().start()



