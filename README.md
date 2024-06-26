# sqlalchemy-challenge

![image](https://github.com/ADotG96/sqlalchemy-challenge/assets/120142473/f7fe89af-b91e-4d50-bba0-fa9a4548624f)


_Background:_ 

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

__Part 1: Analyze and Explore the Climate Data__

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

1. Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

2. Use the SQLAlchemy create_engine() function to connect to your SQLite database.

3. Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

4. Link Python to the database by creating a SQLAlchemy session.

5. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

_Precipitation Analysis_
1. Find the most recent date in the dataset.

2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

3. Select only the "date" & "prcp" values

4. Load the query results into a Pandas DataFrame. Explicitly set the column names.

5. Sort the DataFrame values by "date".

6. Plot the results by using the DataFrame plot method, as the following image shows:

7. Use Pandas to print the summary statistics for the precipitation data.

Screenshot of my analysis. This is displaying precipitation over dates outlined in the x axis and inches displayed on the y - axis

![image](https://github.com/ADotG96/sqlalchemy-challenge/assets/120142473/53ba32d0-fad0-497f-b2f2-aa97423c52f0)



_Station Analysis_
1. Design a query to calculate the total number of stations in the dataset.

2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
  - List the stations and observation counts in descending order.
  - Answer the following question: which station id has the greatest number of observations?

3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

4. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
  - Filter by the station that has the greatest number of observations.
  - Query the previous 12 months of TOBS data for that station.
  - Plot the results as a histogram with bins=12, as the following image shows:
  - Close your session.

Here is a screenshot of my histogram. The x-axis is displaying temperature while the y-axis is highlighting frequency.

![image](https://github.com/ADotG96/sqlalchemy-challenge/assets/120142473/48b4f311-2a5c-4f4f-96c7-d4f5ab53546b)

__Part 2: Design Your Climate App__
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

```/```
- Start at the homepage.
- List all the available routes.

```/api/v1.0/precipitation```
- Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
- Return the JSON representation of your dictionary.

```/api/v1.0/stations```
- Return a JSON list of stations from the dataset.
  
```/api/v1.0/tobs```
- Query the dates and temperature observations of the most-active station for the previous year of data.
- Return a JSON list of temperature observations for the previous year.

```/api/v1.0/<start>``` and ```/api/v1.0/<start>/<end>```
- Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    * In my code this ask is represented in the route:
    *  ```app.route("/api/v1.0/start/<start_date>", methods=['GET'])```
    *  ```@app.route("/api/v1.0/start/end/<start_date>/<end_date>", methods=['GET'])```
- For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    * This code is represented in the route:
    * ```@app.route("/api/v1.0/temperature/<start_date>", methods=['GET'])```
- For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    *This code is similar to the first. It is represented in the route:
    *  ```app.route("/api/v1.0/start/<start_date>", methods=['GET'])```
    *  ```@app.route("/api/v1.0/start/end/<start_date>/<end_date>", methods=['GET'])```
