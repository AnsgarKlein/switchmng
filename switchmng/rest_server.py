from routes import restbp

from flask import Flask

app = Flask('switchmng')
app.url_map.strict_slashes = False
app.register_blueprint(restbp)

if __name__ == '__main__':
    app.run(debug= True, host = '127.0.0.1', port = 8000)

