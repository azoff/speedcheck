import flask
import plots

app = flask.Flask(__name__)
app.register_blueprint(plots.profile, url_prefix='/plots')

if __name__ == '__main__':
    app.run()