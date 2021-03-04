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
        f"/api/v1.0/< start > Enter the start date in the format yyyy-mm-dd <br/>"
        f"/api/v1.0/< start >/< end > Enter the start date and end date in the format yyyy-mm-dd <br/>"        
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


############Temperature
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database

    year_ago = dt.date(2017, 8, 23)-  dt.timedelta(365)
    year_ago

    ##Temperature observations for most active station for the last year of data

    most_active_summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.station == 'USC00519281').all()

    return jsonify(most_active_summary)

@app.route("/api/v1.0/<start>")
def tempstart(start):
    session = Session(engine)

    start_dt = dt.date(*map(int, start.split('-')))

    tobs_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start_dt).all()
    session.close()

    list_tobs = []

    for tob in tobs_start:
        tobs_dict = {}
        tobs_dict[' Min Temperature Recorded'] = tobs_start[0][0]
        tobs_dict[' Max Temperature Recorded'] = tobs_start[0][1]
        tobs_dict[' Avg Temperature Recorded'] = tobs_start[0][2]
        list_tobs.append(tobs_dict)
    return jsonify(list_tobs)


@app.route("/api/v1.0/<start>/<end>")
def temprange(start,end):
    session = Session(engine)

    start_dt = dt.date(*map(int, start.split('-')))
    end_dt = dt.date(*map(int, end.split('-')))

    if (end_dt == ""):

        tobs_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start_dt).all()
    
    else: 
        tobs_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt).all()        

    session.close()

    list_tobs = []

    for tob in tobs_start:
        tobs_dict = {}
        tobs_dict[' Min Temperature Recorded'] = tobs_start[0][0]
        tobs_dict[' Max Temperature Recorded'] = tobs_start[0][1]
        tobs_dict[' Avg Temperature Recorded'] = tobs_start[0][2]
        list_tobs.append(tobs_dict)
    return jsonify(list_tobs)

    
#Run App
if __name__=='__main__':
    app.run()
