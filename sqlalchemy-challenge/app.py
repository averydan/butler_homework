import numpy as np
import pandas as pd
import datetime as dt
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement= Base.classes.measurement
latest_date=dt.date(2017,8,23)
delta=dt.timedelta(days=365)
one_year=latest_date-delta
@app.route("/")
def welcome():
    """Main Menu"""
    return (
        f"Available Routes:<br/><br/>"
        f"This endpoint will get you all of the precipation data by date going back one year from the latest date in the data set:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"This endpoint will get you a list of the stations in the data set:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"This endpoint will get you the temperature data for the last year from the most active station in the data set:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"This endpoint will get you the min, avg, and max temperature data going back to the entered start date:<br/>"
        f"/api/v1.0/startdate:/<start><br/><br/>"
        f"This endpoint will get you the min, avg, and max temperature data from the entered start date to the end date:<br/>"
        f"/api/v1.0/startdate:/<start>/enddate:/<end>"
    )

@app.route("/api/v1.0/precipitation")
def date_prcp():
    session = Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>one_year).all()
    session.close()
    date_prcp = list(np.ravel(results))
    return jsonify(date_prcp)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results=session.query(Station.name).filter(Measurement.station==Station.station).group_by(Measurement.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def active():
    session = Session(engine)
    results=session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date>one_year).\
        filter(Measurement.station=="USC00519281").all()
    session.close()
    active = list(np.ravel(results))
    return jsonify(active)
@app.route("/api/v1.0/startdate:/<start>")
def startdate(start):
    session = Session(engine)
    start = dt.datetime.strptime(start, '%m-%d-%Y')
    inter=[func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results=session.query(*inter).\
        filter(Measurement.date>=start).all()
    session.close()
    startdate = list(np.ravel(results))
    return jsonify(startdate)
@app.route("/api/v1.0/startdate:/<start>/enddate:/<end>")
def startend(start,end):
    session = Session(engine)
    start = dt.datetime.strptime(start, '%m-%d-%Y')
    end = dt.datetime.strptime(end, '%m-%d-%Y')
    inter=[func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results=session.query(*inter).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()
    startend = list(np.ravel(results))
    return jsonify(startend)
if __name__ == '__main__':
    app.run(debug=True)