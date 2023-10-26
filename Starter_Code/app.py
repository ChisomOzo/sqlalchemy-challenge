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
Base.metadata.create_all(conn)
# Save references to each table


# Create our session (link) from Python to the DB
Base.prepare(conn, reflect=True)
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
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def welcome():
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
def names():
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
def names():
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


if __name__ == '__main__':
    app.run(debug=True)