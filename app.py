from flask import Flask, make_response,  request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "dota2"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app) 


@app.route("/")
def hello_world():
    return "<p> Hello World </p>"


@app.route("/heroes", methods=["GET"])
def get_heroes():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM heroes;"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


@app.route("/heroes/<int:id>", methods=["GET"])
def get_heroes_by_id(id):
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM heroes where id = {} """.format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


@app.route("/heroes", methods=["POST"])
def add_heroes():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Heroes_name = info["name"]
    Heroes_role = info['role']
    cur.execute("""
        INSERT INTO heroes (name, role)
        VALUES (%s, %s)
        """, (Heroes_name, Heroes_role))
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "Hero added sucessfully",
                                  "rows_affected": rows_affected}), 200)


@app.route("/heroes/<int:id>", methods=["PUT"])
def update_heroes(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Heroes_name = info["name"]
    Heroes_role = info["role"]
    cur.execute(
        """ UPDATE heroes SET name = %s, role = %s
        WHERE id = %s """,
        (Heroes_name, Heroes_role, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Hero updated successfully",
             "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/heroes/<int:id>", methods=["DELETE"])
def delete_heroes(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM heroes where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Hero deleted successfully",
             "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)