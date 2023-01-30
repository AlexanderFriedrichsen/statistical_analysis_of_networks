import networkx
import pandas
import plotly as pl
pop_data = pandas.read_csv("population_statistics.csv")

print(pop_data.head())

pl.px