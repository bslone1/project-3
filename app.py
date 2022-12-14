import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
import pandas as pd
import sqlite3



#################################################
# Database Setup
#################################################
def add_data_to_db():
    engine = create_engine("sqlite:///data_jobs_db.sqlite")
    conn = engine.connect()
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    df = pd.read_csv('data/working_table.csv')
    df = df.loc[:,'job_title':]
    df.to_sql('jobs',con=engine,if_exists='replace',index=True)
    #sql_df = pd.read_sql_table('jobs',con=engine)
    df2 = pd.read_csv('data/working_table2.csv')
    df2.to_sql('states',con=engine,if_exists='replace',index=True)

def attempt_2_connect(): 
    conn = sqlite3.connect('data_jobs_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    # """guess you need text here"""
    conn = attempt_2_connect()
    data = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
