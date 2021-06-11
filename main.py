from constants import MONGODB_URL, SECRET_KEY, DEBUG
from login import signup, login
from sanic import Sanic
from sanic_motor import BaseModel
from views import FooBar


app = Sanic(__name__)
BaseModel.init_app(app)

# creating settings
settings = dict(
    MOTOR_URI=MONGODB_URL,
    SECRET_KEY=SECRET_KEY
)

# apply settings variables to app config
app.config.update(settings)

# apply routing to app
app.add_route(FooBar.as_view(), "/movies")
app.add_route(login, '/login', methods=["POST"])
app.add_route(signup, '/signup', methods=["POST"])


if __name__ == "__main__":
    # initialize the app by run command and defining params.
    app.run(host="127.0.0.1", port=8000, debug=DEBUG)


# FOR CRUD API

""" 
from sanic import Sanic
from routers import router

def create_app(**kwargs):
    app = Sanic("IMDB APP")
    return app


if __name__ == "__main__":
    sanic_app: Sanic = create_app()

    router(sanic_app)
    sanic_app.run(host ="0.0.0.0", port = 8000, debug = True, workers=2) 
"""

# FOR EC2 CHECK

""" 
from sanic import Sanic, response

app = Sanic("IMDB APP")


@app.route('/')
def hello_world(request):
	return response.text('Hello World!')

if __name__ == "__main__":
    app.run(host ="0.0.0.0", port = 8000, debug = True, workers=2)
"""
