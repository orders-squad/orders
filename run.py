from app import app



@app.route('/')
def api_orders():
    return 'Welcome to api orders!'


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
