# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
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
Base.prepare(autoload_with=engine)

# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Avialable Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<start_date><br/>"
        f"/api/v1.0/start/end/<start_date><end_date><br/>"
        f"/api/v1.0/temperature/<start_date>"
    ) 


@app.route("/api/v1.0/precipitation")
def percip_data():
    session = Session(engine)

    """retreive only last 12 months of percipitation analysis data"""
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_results = session.query(Measure.date, Measure.prcp).filter(Measure.date >= one_year_ago).all()

    session.close()

    #create a dictionary for precipitation in the last year
    precipitation_data = {date: prcp for date, prcp in precip_results}

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """return list of stations from dataset"""
    #Query all the stations
    stations_results = session.query(Station.station).all()

    session.close()

    #convert list of tupes into normal list
    all_stations = list(np.ravel(stations_results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #calculate date 1 year ago from last data point in database
    last_date = session.query(Measure.date).order_by(Measure.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days = 365)

    """Query dates & temp observation of the most active station for the previous year"""
    #pull most active station from climate_starter
    most_active = session.query(Measure.date, Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= one_year_ago).all()
    
    #produce list
    #tobs_info = list(np.ravel(most_active))

    #produces list of dictionaries
    tobs_info = []
    for date, tobs in most_active:
        tobs_info.append({'date': date, 'temperature': tobs})

    return jsonify(tobs_info)


@app.route("/api/v1.0/start/<start_date>", methods=['GET'])
@app.route("/api/v1.0/start/end/<start_date>/<end_date>", methods=['GET'])
def start(start_date, end_date=None):
    session = Session(engine)

    """For a specified start date & for a specified range of start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    #test list of temp dates
    #temperature_data = [
        #{"date": "2016-08-24", "temperature": 77.0},
        #{"date": "2016-08-25", "temperature": 80.0},
        #{"date": "2016-08-26", "temperature": 80.0},
        #{"date": "2016-08-27", "temperature": 75.0},
        #{"date": "2016-08-28", "temperature": 73.0},
        #{"date": "2016-08-29", "temperature": 78.0},
        #{"date": "2016-08-30", "temperature": 77.0},
        #{"date": "2016-08-31", "temperature": 78.0},
        #{"date": "2016-09-01", "temperature": 80.0},
        #{"date": "2016-09-02", "temperature": 80.0}
    #]
    #create list of min temp, avg temp, & max temp for start-end range
    #create logic for just start date
    if not end_date:
        temperatures = session.query(
             func.min(Measure.tobs), 
            func.avg(Measure.tobs), 
            func.max(Measure.tobs)
        ).filter(Measure.date >= start_date).all()[0]
    
    #add logic for start & end date range
    else:
        temperatures = session.query(
            func.min(Measure.tobs), 
            func.avg(Measure.tobs), 
            func.max(Measure.tobs)
        ).filter(Measure.date.between(start_date, end_date)).all()[0]

    temperature_stats = {
        "min_temperature": temperatures[0],
        "avg_temperature": temperatures[1],
        "max_temperature": temperatures[2]
    }
    
    session.close()

    return jsonify(temperature_stats)


@app.route("/api/v1.0/temperature/<start_date>", methods=['GET'])
def temperature(start_date):
    session = Session(engine)

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    # Query to calculate TMIN, TAVG, TMAX for all dates >= start_date
    temperatures = session.query(
        func.min(Measure.tobs), 
        func.avg(Measure.tobs), 
        func.max(Measure.tobs)
    ).filter(Measure.date >= start_date).all()[0]

    # Create JSON response
    temperature_stats = {
        "min_temperature": temperatures[0],
        "avg_temperature": temperatures[1],
        "max_temperature": temperatures[2]
    }

    session.close()
    return jsonify(temperature_stats)

if __name__ == '__main__':
    app.run(debug=True)