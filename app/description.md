## Overview
Our capstone project this year is to build an API that simulate the solar farm performance. The application logic is shown in the figure below.

<a href="https://ibb.co/0GYQwxd"><img src="https://i.ibb.co/sVstBZM/simulation-API-run-model.png" alt="simulation-API-run-model" border="0"></a>

The simulation API will tie the user configuration and real-time weather data together, then it will generate the simulation result and store it in `Elasticsearch` database.

## User
Endpoints under user is designed to integrate with monitoring dashboard. User model is the center of the star schema, which it contains ID for configured location, device and solar farm layout

## Location
Once login, you are able to configure the location of the solar by supplying latitude and longitude

## Device 

Configure the model solar panel and inverter of your solar farm

## Pvsystem
configure the layout of the solar farm. Once the layout is configured, you can use `/run_model` endpoint to simulate the solar farm performance

## Analytics
The number of data points return will be based on how many time user call the `/run_model` and the time interval between each call. There are two analytic endpoints

- **live**: live endpoint return past 24 hours of simulation result

- **historical**: If user only specify year, the historical endpoint will do annual analysis for the users, which will return statistic result of each day in the year. If user specify month and year, the endpoint will return statistic result of each hour in the month


