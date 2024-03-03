# sqlalchemy-challenge

This repo contains Module 10 SQL ALchemy Challenge. Below steps were performed as requested. The app.py and climate.ipynb files are self explanatory. 

Additionally added few screenshots for the results from app.py api routes.

Part 1: Analyze and Explore the Climate Data

To begin, use Python and SQLAlchemy to do a basic climate analysis and data exploration of climate database.
1. Used the provided files (climate_starter.ipynb and hawaii.sqlite) from the startercode to complete climate analysis and data exploration.
2. Used the SQLAlchemy create_engine() function to connect to SQLite database.
3. Used the SQLAlchemy automap_base() function to reflect tables into classes, and then saved references to the classes named station and measurement.
4. Link Python to the database by creating a SQLAlchemy session.

Precipitation Analysis
1. Find the most recent date in the dataset.
    Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
2. Load the query results into a Pandas DataFrame. Explicitly set the column names.
3. Sort the DataFrame values by "date".
4. Plot the results by using the DataFrame plot method, image is shown in the jupyter notebook
5. Use Pandas to print the summary statistics for the precipitation data.

Station Analysis

1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
    List the stations and observation counts in descending order.
3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query
4. Design a query to get the previous 12 months of temperature observation (TOBS) data. 
    Filter by the station that has the greatest number of observations.
    Query the previous 12 months of TOBS data for that station.
    Plot the results as a histogram with bins=12, Image is shown in the climate.ipynb

Climate App

Flask API designed has the following routes:

1. `/`
    Start at the homepage.
    List all the available routes. [api_home_page.png](./Screenshots/api_home_page.png)

2. `/api/v1.0/precipitation`
    Retrieves only the last 12 months of precipiation data to a dictionary using date as the key and prcp as the value. [api_precipitation_route.png](Screenshots/api_precipitation_route.png)

3. `/api/v1.0/stations`
    Return a JSON list of stations from the dataset. [api_stations_route.png](Screenshots/api_stations_route.png)

4. `/api/v1.0/tobs`
    Query the dates and temperature observations of the most-active station for the previous year of data.  
    Return a JSON list of temperature observations for the previous year.[api_tobs_route.png](Screenshots/api_tobs_route.png)

5. `/api/v1.0/<start>`
    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date 
    [api_start_date_valid_response.png](Screenshots/api_start_date_valid_response.png)
    [api_start_date_404_not_found.png](Screenshots/api_start_date_404_not_found.png)

6. `/api/v1.0/<start>/<end>`
    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
    [api_start_end_date_valid_response.png](Screenshots/api_start_end_date_valid_response.png)
    [api_start_end_date_404_not_found.png](Screenshots/api_start_end_date_404_not_found.png)


