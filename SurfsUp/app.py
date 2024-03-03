# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Get the table names
print(Base.classes.keys() )

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

################################################
# Common Functions
################################################
# Function to fetch most recent date from the database 
# and calculate date for the last one year
def query_dates():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Query precipitations for last 12 months of data
    date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d').date()
    print(f"recent date: {date}")

    # Calculate the date one year from the last date in data set.
    query_date = date - dt.timedelta(days=365)
    print(f"query date: {query_date}")

    # returns recent_date and 1 year ago date from recent date
    return (recent_date, query_date)


# Common function to get the lowest, highest and average temperatures for given dates
def get_temperatures(start, end = None):

    # attributes to select from table
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    return_msg = ""
    results = []

    # start date is mandatory - returns message if start date is null
    if (start is None):
        return_msg = f"start date cannot be null"
    

    # if end date is not null, fetches the metrics between start date and end date
    elif not (end is None) :
        results  = session.query(*sel).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
        print(f"results in IF: {results}")
        
        return_msg = f"No records were found in the database for the given start date: {start} and end date: {end}"
    
    # if end date is null, fetches the metrics between start date to the most recent date in the database
    else:
        results  = session.query(*sel).\
            filter(Measurement.date >= start).all()
        return_msg = f"No records were found in the database for the given start date: {start} "

    # loops through the result and formulates the json response
    temperatures = []
    for min, max, avg in results:
        if not ((min is None) | (max is None) | (avg is None)) :
            temp_dict = {}
            temp_dict["min"] = round(min,2)
            temp_dict["max"] = round(max,2)
            temp_dict["avg"] = round(avg,2)
            temperatures.append(temp_dict) 

    if(len(temperatures) > 0):
        session.close()
        return jsonify(temperatures)
    else:
        session.close()
        return jsonify({"error": return_msg}), 404 
    

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home_page():
    """Available Routes:"""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/2010-01-01<br>"
        f"/api/v1.0/2010-01-01/2011-01-01<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # get one year past date from the query_dates() function
    dates = query_dates()
    query_date = dates[1]

    # Query Database for the precipitation info for dates >= query_date 
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).all()

    # formulate the dictionary
    precipitations = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precipitations.append(prcp_dict) 

    # close session and return the data
    session.close()
    return jsonify(precipitations)


@app.route("/api/v1.0/stations")
def stations():
    # query station data and return
    stations = session.query(Station.station).all()

    session.close()
    return jsonify (list(np.ravel(stations)))


@app.route("/api/v1.0/tobs")
def tobs():
    # get one year past date from the query_dates() function
    dates = query_dates()
    query_date = dates[1]

    # find most active station
    active_stations = session.query(Measurement.station, func.count(Measurement.id)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()) .\
        all()
    most_active_station = active_stations[0][0]

    # query the last one year temperatures for the most active station 
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= query_date).all()

    temperatures = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict[date] = tobs
        temperatures.append(temp_dict) 

    
    session.close()
    return jsonify(temperatures)

# Route to find the lowest, highest and average temperatures from a given date
@app.route("/api/v1.0/<start>")
def start(start):

    return get_temperatures(start)
 

# Route to find the lowest, highest and average temperatures between given start date and end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    return get_temperatures(start, end)

# main function
if __name__ == '__main__':
    app.run(debug=True)