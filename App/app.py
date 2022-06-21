from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import Algoritme.algoritme as calculate
import asyncio
import aiohttp
import requests


app = Flask(__name__)
CORS(app)

@app.route("/get-products", methods=['GET'])
def begin():

    return jsonify(calculate.Knapsack().main())


if __name__ == "__main__":
    app.run()
