from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    printout = (
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/<start>/<end>"
    )

    return printout


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list)


@app.route("/api/v1.0/stations")
def station():
    #create session
    session = Session(engine)
    stations = {}
    #query
    results = session.query(Station.station, Station.name).all()
    for stat,name in results:
        stations[stat] = name
    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)
    #Get last date contained in the dataset and date from one year ago
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d')\
        - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #query for the dates and temp values

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year_date).\
            order_by(Measurement.date).all()

    #conver to list of dictionaries to jsonify
    tobs_date_list = []

    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_date_list.append(new_dict)

    session.close()

    return jsonify(tobs_date_list)


if __name__ == "__main__":
    app.run(debug=True)
