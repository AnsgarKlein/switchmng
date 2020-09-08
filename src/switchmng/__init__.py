from switchmng.routes import restbp

from flask import Flask

app = Flask('switchmng')
app.url_map.strict_slashes = False
app.register_blueprint(restbp)

