# from app import create_app
from app import view
from app.view import app


if __name__ == '__main__':
    view.initialize_logging()
    view.init_db()
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
