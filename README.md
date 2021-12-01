# Surf 'n' Shake: Weather Analysis

## Overview

This analysis was started with the intention to analyse the available weather dataset for Oahu to study weather patterns and determine whether it is an ideal location for a Surf and Shake shop. As part of the analysis, the following were determined:

- The precipitation trend for the most recent year
- The stations used for analysis and the amount of data from each station
- The temperature pattern for the most active station
- The temperature statistics between two dates

At the end of the analysis, some of the above data was made available as a webpage, via Flask, to demostrate to the board of directors. In addition to the above, two more metrics were also calculated to determine whether the shop would be sustainable all through the year.

- Summary statistics of temperature for the month of June
- Summary statistics of temperature for the month of December

The analysis results for the two metrics will be discussed in detail in this report. 

The weather dataset was available as a sqlite file, so sqlalchemy on python was used to perform the analysis.

## Results

![Temperature Statistics](images/Temperature_statistics.png?raw=true "Temperature Statistics")

From the gathered statistics, we can see that:

- The mean temperature difference between the two months is **3.9**, which suggests that temperature conditions remain similar throughout the year. Also, this temperature difference is considerably lower than most parts of the nation, making it a desirable tourist destination.

- The difference between minimum temperature values is **8**, but the difference between 25th quartile values is **4** which is close to the mean difference. This suggests that though there are a few drops in temperature, most of the data has a difference of 4, making it still desirable.

- Likewise, the other paramters also have a difference ranging from only **2 to 4**, further confirming that the weather conditions remain almost similar throughout the year

## Summary

From the analysis, we observed that though there is an overall drop in temperature, it is not considerable enough to have an impact. Therefore, Oahu is still an ideal location to open the Surf 'n' Shake shop.

In addition to the above analysis, we can also perform a few more queries to analyse more patterns and trends. For example,

a. Retrieve year information and group by based on that. This will allow us to analyse recent trends much better.

`
results=session.query(extract('year',Measurement.date),Measurement.tobs).filter(extract('month',Measurement.date)==12).all()
df=pd.DataFrame(results,columns=["year","temp"])
df.groupby(["year"]).describe()
`

While it is possible to groupby directly in the query, doing so would require us to specify each of the statistic separately

b. In case it is concerning as to the number of the days where there is a temperature drop greater than four, we could have retrieved that information as well

`
avg=session.query(func.avg(Measurement.tobs)).filter(extract('month',Measurement.date)==12).all()
avg=list(np.ravel(avg))
session.query(func.count(Measurement.tobs)).filter(extract('month',Measurement.date)==12).\
filter(avg[0]-Measurement.tobs>4).all()
`

Also, we could have retrieved the precipitation information as well and performed a similar analysis. 

