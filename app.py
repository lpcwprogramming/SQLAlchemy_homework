import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Set up database
#######################################################################

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


#Set up Flask
#######################################################################
app = Flask(__name__)


#Flask Routes
#######################################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
    )


@app.route("/api/v1.0/precipitation")
def measurement():
    # Create  session from Python to the DB
    session = Session(engine)

    #Precipitation query
    precipitation = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    #Create a precipitation dictionary from the row data and append to a list
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    #Return JSON format
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station(): 

    #Station query
    stations = session.query(Station.station).all()

    session.close()

    #Return JSON format
    return jsonify(stations)


if __name__ == '__main__':
    app.run(debug=True)