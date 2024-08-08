from flask import Flask
from routes.register import register_blueprint
from routes.login import login_blueprint
from routes.user import user_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gSKMJh.2+Dc2pK_[ELlT"90&8MIs{Dd{COq%vB={do^=Rh+@r>n~yX2Is74<!e>'

app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(port=5000)