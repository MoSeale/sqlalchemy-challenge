#############Dependencies

import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

##############Create engine for the hawaii.sqlite database

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)


###Reflect Database ORM classes

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()


#####Save a reference to the measurement table as 'Measurement' 
#and station table as 'Station'

Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a database session object
session = Session(engine)


#Flask Setup
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Analysis for Hawaii<br/><br/>"
        f"You may navigate to the following: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"        
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"        
    )

####Precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database

    year_ago = dt.date(2017, 8, 23)-  dt.timedelta(365)
    year_ago
    
    # Perform a query to retrieve the data and precipitation scores
    climate_data= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
    precipitation_dict= dict(climate_data)
    return jsonify(precipitation_dict)

############Stations
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.station).all()
    #station_dict= dict(station_names)
    return jsonify(station_names)

#Run App
if __name__=='__main__':
    app.run()
