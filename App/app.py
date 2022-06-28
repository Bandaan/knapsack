# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 28/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

from flask import Flask, jsonify
from flask_cors import CORS
import algoritme as calculate

# API aanmaken om frontend en algoritme te linken
app = Flask(__name__)
CORS(app)


# Route maken voor algoritme met massa, categorie en dieet
@app.route("/get-products/<massa>/<categorie>/<dieet>", methods=['GET'])
def begin(massa, categorie, dieet):

    # Beste producten aanvragen en teruggeven aan client
    return jsonify(calculate.Knapsack().main(massa, categorie, dieet))


if __name__ == "__main__":
    # API starten
    app.run()
