# COVID API
A simple API to access covid-19 daily numbers, including case counts, deaths, and recovered. This project uses FastAPI for the server, and postgresql for the database. Data is taken from [COVID-19 CSSE Data Repository](https://github.com/CSSEGISandData/COVID-19). Uses wait-for-it script taken from [here](https://github.com/vishnubob/wait-for-it).

## Getting Started
This project uses the daily report data from the [repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports). Create a folder called data under database. Make sure your working directory looks like this:
```
- app/
- COVID-19/
- database/
    - data
    - sql/
        - init.sql
        - load.sql
- .gitignore
- convert-data.py
- docker-compose.debug.yml
- docker-compose.loadtest.yml
- docker-compose.test.yml
- docker-compose.yml
- readme.md
```
Run the command
```
python convert-data.py -d COVID-19 -o database/data/final.csv
```
This will run a data processing script and outputs a final.csv file in database/data/final.csv.

For privacy reasons, the passwords and usernames in certain areas have been filled with placeholder values. Please fill in the data in .envtocustomise and rename the file to ".env".

## Building
Once processed date is prepared, navigate to this folder in terminal/command prompt. You can instantly get an instance of this API running with the command

```
docker compose -f docker-compose.yml up
```

This creates a docker network containing the database which loads the airport dataset data, and the API for you to query from. Default port for the API is set to 8000. Navigate to localhost:8000 or 127.0.0.1:8000 to access the server. Go to localhost:8000/docs or 127.0.0.1:8000/docs to access a list of APIs available.

When you want to delete the network and its containers, you can run the command below:

```
docker compose down
```

You can also run it with the -v flag to remove the volume which helps persist the database info. If you want to remove the images as well, you can run:

```
docker compose down --rmi all
```

If you wish to run the API in live debug mode to see your changes in real-time, you can use the debug version of the docker compose file. This can be done by running:

```
docker compose -f docker-compose.debug.yml up
```


## Testing

There is a separate pipeline to use for testing, by using the docker-compose.test.yml file instead.

```
docker compose -f docker-compose.test.yml up
```

## Load Testing
To run load testing container, run the command

```
docker-compose -f docker-compose.loadtest.yml up
```

and head to localhost:8089 to access the locust interface.

