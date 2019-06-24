import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy import text

app = Flask(__name__)
cors = CORS(app)

DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_NAME = os.environ['DATABASE_NAME']
DB_USER = os.environ['DATABASE_USER']
DB_HOST = os.environ['DATABASE_HOST']

engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))


@app.route('/jobs', methods=['GET'])
def get_jobs():
    favourite = request.args.get('favourite', None)
    status = request.args.get('status', None)

    if status:
        jobs = engine.execute(text(f'SELECT * FROM jobs WHERE status="{status}"'))
    elif favourite:
        jobs = engine.execute(text(f'SELECT * FROM jobs WHERE favourite={favourite}'))
    else:
        jobs = engine.execute(text('SELECT * FROM jobs'))

    jobs_data = [dict(row.items()) for row in jobs]

    return jsonify(jobs_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
