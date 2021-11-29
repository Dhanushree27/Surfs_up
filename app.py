# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import sqlalchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask dependencies
from flask import Flask, jsonify

# Set up connection to database and reflect the databases
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Assign the reflected classes to variables for easier access
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session to query and work with
session = Session(engine)

# Setup for Flask
app = Flask(__name__)
# Setup of root
@app.route("/")
def welcome():
    return(
    f" Welcome to the Climate Analysis API!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/start/end<br\>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precipitation=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # Jsonify the data
    precip={date:prcp for date,prcp in precipitation}
    return jsonify(precip)
@app.route("/api/v1.0/stations")
def stations():  
    results=session.query(Station.station).all()
    # Converting data to list
    stations=list(np.ravel(results))
    return jsonify(stations=stations)
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(Measurement.tobs).filter(Measurement.date >= prev_year).filter(Measurement.station == 'USC00519281').all()
    temps=list(np.ravel(results))
    return jsonify(temps=temps)
# Routes to get start and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    