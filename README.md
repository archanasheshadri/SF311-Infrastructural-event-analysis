# SF311-Infrastructural-event-analysis

This repository includes data analysis of the SF311 data related to infrastructural events(requests).

We have considered the [SF311 data](https://data.sfgov.org/City-Infrastructure/Case-Data-from-San-Francisco-311-SF311-/vw6y-z8j6) for the city infrastructural events in San Francisco,which contains a tabular list of reports. The duration of the data collected is from May 2014 to August 2015.
SF311.org is the official data portal for the city of San Francisco providing access to city-related data through file downloads and APIs. I was motivated to use a data driven approach to analyze characteristics of various issues reported by people.
I retrieved city infrastructure data from SF311 using their API endpoint, which includes report of issues such as potholes, overflowing sewers, and graffiti. Data retrieved from API was stored in a local MySQL database for further analysis. 
I performed exploratory data analysis to glean insights of most common issues/issue-types, locations with prone to issues, and spatio-temporal visualization of these issues on a city map. 

