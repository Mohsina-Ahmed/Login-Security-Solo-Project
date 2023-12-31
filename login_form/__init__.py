import os
from flask import Flask, make_response
#from decouple import config
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()


#Load environment variables from the .env file
#config()
load_dotenv()

#Retrieve the SECRET_KEY from the environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    csrf.init_app(app)

    #to set the cookie with SameSite 'lax' attribute  
    app.config["SESSION_COOKIE_SAMESITE"] = 'lax'
    
    app.config.from_mapping(
        #Configure the app with the retirieved SECRET_KEY
        SECRET_KEY=SECRET_KEY, #Should not use the hard coded secret key
        DATABASE=os.path.join(app.instance_path, 'login_form.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.after_request
    def add_security_headers(resp):
        csp = "default-src 'self'; frame-ancestors 'self'; form-action 'self'"
        resp.headers['Content-Security-Policy']=csp
        resp.headers['X-Content-Type-Options'] = 'nosniff'

        #Set the header with SameSite Lax attribute
        resp.headers['Set-Cookie'] = 'username=flask; Secure; HttpOnly; SameSite=Lax; Path=/'
        
        return resp

    return app