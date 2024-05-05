import hashlib
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from modules.db.bootstrap import create_schema

app = Flask(__name__)
# Setup the limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per day"],
)

# Store the codes in a dictionary
codes = {}


@limiter.exempt
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@limiter.exempt
@app.route('/submit_code', methods=['POST'])
def submit_code():
    code = request.form['code']
    hash_obj = hashlib.sha256()
    hash_obj.update(code.encode('utf-8'))
    unique_id = hash_obj.hexdigest()
    codes[unique_id] = code

    db = get_db()
    db.execute("INSERT OR IGNORE INTO snippets(snippet_id, snippet) values (?,?)", (unique_id,code))
    db.commit()
    db.close()

    return redirect(url_for('get_code', code_id=unique_id))


@app.route('/explain_code', methods=['POST'])
def explain_code():
    unique_id = request.get_json()['id']
    db = get_db()
    x=db.execute("SELECT snippet from snippets where snippet_id=(?)", (unique_id,)).fetchone()
    db.commit()
    print(x[0])
    # explained=explain_code_snippet(codes[unique_id])
    # print(explained)
    return jsonify({'content': str("""
- The code snippet simply prints the string "hello" to the console.
- The `print()` function is used to output text or data to the terminal or console. 
- In this case, the `print()` function is called with the argument "hello", causing it to display the text "hello" when the code is executed.
- This code demonstrates a basic use of the `print()` function in Python to produce output.
- The `print()` function is commonly used for debugging, logging, or providing information to the user in Python programs.
    """)})


@limiter.exempt
@app.route('/code/<code_id>', methods=['GET'])
def get_code(code_id):
    code = codes.get(code_id, "Code not found")
    return render_template('code_display.html', code=code, code_id=code_id)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("snippets.db")
    return db


if __name__ == '__main__':
    create_schema()
    app.run()
