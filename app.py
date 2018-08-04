import string
from flask import Flask, request, Response
from flask_restful import Resource, Api, abort, reqparse
import random
from flask_restful.representations import json

app = Flask(__name__)
api = Api(app)

COLOURS = [x for x in "RGBYCM"]


class Mastermind(object):

    def __init__(self):
        self.history = {}
        self.colours = ''.join([random.choice(COLOURS) for _ in range(4)])
        self.solved = False
        self.guess_id = 0
        print("Created new game with pattern: {}".format(self.colours))

    def make_guess(self, guess):
        print("Making a guess: {}".format(guess))

        self.history[self.guess_id] = guess
        self.guess_id += 1

        if guess == self.colours:
            self.solved = True

        return self.check_guess(guess)

    def check_guess(self, guess):
        result = self.check_guess_dict(guess)
        return "exact: {}\tnear: {}\tsolved: {}".format(result['exact'], result['near'], result['solved'])

    def make_guess_dict(self, guess):
        print("Making a guess: {}".format(guess))

        self.history[self.guess_id] = guess
        self.guess_id += 1

        if guess == self.colours:
            self.solved = True

        return self.check_guess_dict(guess)

    def check_guess_dict(self, guess):
        # this should be the number of correct colours and the correct positions.
        near = 0
        exact = 0
        for i in range(0, len(self.colours)):
            if guess[i] == self.colours[i]:
                exact += 1
            elif guess[i] in self.colours:
                near += 1

        self.solved = (guess[0:len(self.colours)] == self.colours)
        return {'exact': exact, 'near': near, 'solved': self.solved}


games = {}


def abort_if_game_doesnt_exist(game_id):
    if game_id not in games:
        abort(404, message="Mastermind game with ID: {} doesn't exist\n".format(game_id))


class JsonMastermindGame(Resource):
    def post(self):

        game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        games[game_id] = Mastermind()
        result = {'game': game_id}

        return Response(json.dumps(result), status=201,  mimetype='application/json')

    def get(self, game_id=None):
        abort_if_game_doesnt_exist(game_id)

        result = {}
        for k in games[game_id].history:
            result[k + 1] = {
                'guess':games[game_id].history[k],
                'result':  games[game_id].check_guess_dict(games[game_id].history[k]),
             }
        return Response(json.dumps(result), status=200, mimetype='application/json')

    def put(self, game_id=None):
        result = {}
        abort_if_game_doesnt_exist(game_id)

        if request.headers['Content-Type'] == 'application/json':
            data = request.get_json()

            if "guess" not in data:
                result['error'] = "I can't find your guess -- Have you set your guess?"
                return Response(json.dumps(result), status=400, mimetype='application/json')

            guess = data['guess']
            result['guess'] = guess
            result['result'] = games[game_id].make_guess_dict(guess)
            return Response(json.dumps(result), status=201, mimetype='application/json')

        result['error'] = "I don't understand the request -- is the Content-Type correct?"
        return Response(json.dumps(result), status=400, mimetype='application/json')


class MastermindGame(Resource):

    def post(self):

        game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        games[game_id] = Mastermind()

        output = "{}\n".format(game_id)

        return Response(output, mimetype='text/plain', status=201)

    def get(self, game_id=None):
        abort_if_game_doesnt_exist(game_id)

        output = ""
        for k in games[game_id].history:
            output += "{}: {}\n".format(k + 1, games[game_id].history[k])

        output += games[game_id].check_guess(games[game_id].history[k])

        return Response(output, mimetype='text/plain', status=200)

    def put(self, game_id=None):

        abort_if_game_doesnt_exist(game_id)

        if "guess" not in request.form:
            Response("Have you set your guess?", mimetype='text/plain', status=400)

        guess = request.form['guess']
        result = games[game_id].make_guess(guess)
        print("guess {} for game {} -> {}".format(guess, game_id, result))
        return Response(result, mimetype='text/plain', status=201)


class Help(Resource):
    def get(self):
        return Response("""Mastermind

This is a simple server program to play a game of mastermind. 
You can interact with it through the following resources:

    resource    method              response
    ----------- ------------------- ------------------------------------------------------------
    /game/      POST (empty)        creates a new game, you'll get the ID in the response
    /game/<ID>  PUT  (guess=ABCD)   makes a guess for that game instance, returns the number of 
                                    correct colours/positions and if it's been solved.
    /game/<ID>  GET  (empty)        shows the history of guesses

In this game, we'll have 6 colours (Red, Green, Blue, Yellow, 
Cyan, Magenta) and 4 positions. The aim of the game is to guess
the colours of the pegs in the correct order. For example, if the 
computer has chosen the sequence 'RGBY', then you might perform 
the following set of guesses:

    RRGG - 2 correct colours, 2 correct positions
    BBYY - 2 correct colours, 1 correct positions
    RBYY - 3 correct colours, 2 correct positions
    RMGY - 3 correct colours, 2 correct positions
    RGMY - 3 correct colours, 3 correct positions
    RGBY - 4 correct colours, 4 correct positions  

""", mimetype='text/plain', status=200)


class Hello(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='Your name', required=False, default=None)

        super(Hello, self).__init__()

    @staticmethod
    def get():
        if 'name' in request.args:
            return Response("Hello, {}!".format(request.args['name']), mimetype='text/plain', status=200)
        return Response("Hello, World!", mimetype='text/plain', status=200)

    @staticmethod
    def post():
        if 'name' in request.form:
            return Response("Hiya {}!".format(request.form['name']), mimetype='text/plain', status=200)
        return Response("Hello, World!", mimetype='text/plain', status=200)

    @staticmethod
    def put():
        if 'name' in request.form:
            return Response("Wassup {}!".format(request.form['name']), mimetype='text/plain', status=200)
        return Response("Hello, World!", mimetype='text/plain', status=200)

    @staticmethod
    def delete():
        if 'name' in request.form:
            return Response("Goodbye, {}!".format(request.form['name']), mimetype='text/plain', status=200)
        return Response("Goodbye, World!", mimetype='text/plain', status=200)


api.add_resource(Hello, '/')

# about
api.add_resource(Help, '/help/')

# post - make a new game instance
# put - makes a new guess
# get - retrieves the history of the game and if it's been solved
api.add_resource(MastermindGame, '/game/', '/game/<string:game_id>/', )
api.add_resource(JsonMastermindGame, '/mastermind/', '/mastermind/<string:game_id>/', )

if __name__ == '__main__':
    app.debug = True
    app.run()
