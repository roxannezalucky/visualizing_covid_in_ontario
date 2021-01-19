import sys
import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdates

#data source: https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario

#reading in the file
df = pd.read_csv('/Users/roxy/Documents/covid/conposcovidloc1.csv')

#filtering out when date is null
df = df[~df['Accurate_Episode_Date'].isnull()]

#filtering for just city of observation, some options: 'Mississauga'|'Windsor'
city = "Toronto"

df = df[(df['Reporting_PHU_City'] == city)]

#include only cases that were fatal
#df = df[(df['Outcome1'] == 'Fatal')]

#sorting by onset date
df['Accurate_Episode_Date'] = pd.to_datetime(df.Accurate_Episode_Date)
df = df.sort_values(by='Accurate_Episode_Date')

print("\nLatest Available Date")
print(df['Accurate_Episode_Date'].iloc[-1])

print("\nNumber of Positive Covid-19 Cases in {}, Ontario".format(city))
print(df.shape[0] - 1)

deaths = df[df['Outcome1'] == 'Fatal']

print("\nNumber of Positive Covid-19 Deaths in {}, Ontario".format(city))
print(deaths.shape[0] - 1)

#adding cumulative sum of cases for each date
daily_counts = df['Accurate_Episode_Date'].value_counts(sort=False)
df_daily_counts = pd.DataFrame(daily_counts)
df_daily_counts = df_daily_counts.reset_index()
df_daily_counts.columns = ['Accurate_Episode_Date', 'count']
df_daily_counts = df_daily_counts.sort_values(by='Accurate_Episode_Date')
df_daily_counts['Cumulative_Sum_of_Cases'] = df_daily_counts['count'].cumsum()

#there is a 3 day data delay for completed data
data_delay = 3
df_daily_counts = df_daily_counts.drop(df_daily_counts.tail(data_delay).index)
print(df_daily_counts)

#df.plot.line(title="Covid Curve")
#plot.show(block=True)

plot.plot(df_daily_counts['Accurate_Episode_Date'], df_daily_counts['Cumulative_Sum_of_Cases'], c='b', linewidth=7.0)
plot.xlabel('date')
plot.xticks(rotation=40)
plot.ylabel('Cumulative Sum of New Cases')
plot.title('Confirmed Positive Cases of Covid-19 in {}, Ontario, \n Source: Government of Ontario'.format(city))
#https://matplotlib.org/3.1.1/gallery/pyplots/dollar_ticks.html#sphx-glr-gallery-pyplots-dollar-ticks-py
#fig = plot.figure()
#ax = fig.gca()

#date_format = mdates.DateFormatter('%d')
#ax.xaxis.set_major_formatter(date_format)

#plot.set_horizontalalignment('right')

#date_format = mdates.DateFormatter('%d')
#ax.xaxis.set_major_formatter(date_format)

#https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
#plot.scatter(x=df['Reporting_PHU_Longitude'], y=df['Reporting_PHU_Latitude'])

plot.show()