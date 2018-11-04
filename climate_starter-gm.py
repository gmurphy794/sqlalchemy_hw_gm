import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
### Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start where start = 'YYYY-MM-DD'<br/>"
        f"/api/v1.0/start/end where start and end = 'YYYY-MM-DD'"
    )

'/api/v1.0/precipitation'
    #Convert the query results to a Dictionary using 'date' as the key and `prcp` as the value.

    #Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp():
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    prcp_date = []
    for measurement in prcp:
        prcp_dict = {}
        prcp_dict["date"] = measurement.date
        prcp_dict["prcp"] = measurement.prcp
        prcp_date.append(prcp_dict)

    return jsonify(prcp_date)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    stations = list(np.ravel(stations))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    dates = session.query(Measurement.date).all()
    dates = pd.DataFrame(dates)
    dates['date'] = pd.to_datetime(dates['date'], format='%Y-%m-%d')
    start_date = dates['date'].max() - dt.timedelta(days=365)
    start_date = start_date.date()
    prcp = session.query(Measurement.prcp).\
        filter(Measurement.date >= str(start_date)).all()
    prcp = list(np.ravel(prcp))
    
    return jsonify(prcp)

@app.route("/api/v1.0/<start>")
def start(start):
    
    start_date = start
    info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    info = list(np.ravel(info))

    return jsonify(info)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):

    start_date = start
    end_date = end
    info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    info = list(np.ravel(info))

    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)