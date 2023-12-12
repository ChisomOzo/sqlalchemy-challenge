# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Base.metadata.create_all(conn)
# Save references to each table


# Create our session (link) from Python to the DB
# Base.prepare(conn, reflect=True)
HawaiiMeasure = Base.classes.measurement
HawaiiStation = Base.classes.station
session = Session(conn)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def index():
    """List all available api routes."""
    return (
        "/api/v1.0/precipitation"
        "/api/v1.0/stations"
        "/api/v1.0/tobs"
        "/api/v1.0/<start>"
        "/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results = session.query(HawaiiMeasure).all()
    session.close()
    prcps = []

    for prcp, date in results:
       prcps_dict = {}
       prcps_dict["prcp"] = prcp
       prcps_dict["date"] = date
       prcps.append(prcps_dict)

    return jsonify(prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(HawaiiMeasure.station, func.count(HawaiiMeasure.station)).\
          group_by(HawaiiMeasure.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
   session = Session(engine)
   last_date = dt.date(2017, 8, 23)
   year_ago = last_date - dt.timedelta(days=365)

   """Return a list of all passenger names"""
    # Query all passengers
   results = session.query(HawaiiMeasure.tobs).\
                                filter(HawaiiMeasure.date >= year_ago).\
                                order_by(HawaiiMeasure.date.desc()).all()
    # group_by(HawaiiMeasure.station).all()

   session.close()

    # Convert list of tuples into normal list
   prev_year = list(np.ravel(results))

   return jsonify(prev_year)
@app.route("/api/v1.0/<start>")
def tobs_start():
    session=Session(engine)
    results = session.query(HawaiiMeasure.tobs, HawaiiMeasure.date).all()
    for date in HawaiiMeasure.tobs :
        if date >= 2016-8-23:
            results.append(HawaiiMeasure.tobs)
    return jsonify(results)

@app.route('/api/v1.0/<start> tobs /<end>')
def tobs_stats_range(start, end):
    session=Session(engine)
    results = session.query(HawaiiMeasure.tobs, HawaiiMeasure.date).all()
    for date in HawaiiMeasure.tobs:
        if start <= date <= end:
            results.append(HawaiiMeasure.tobs)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)