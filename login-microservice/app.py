from flask import Flask, jsonify, request
import requests


app = Flask(__name__)

languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})

if __name__ == '__main__':
    app.run()
