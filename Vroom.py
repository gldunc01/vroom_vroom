from cgi import test
from doctest import master
from turtle import width
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.layouts import gridplot
from math import pi



#Importing Specs file
specs = pd.read_excel('Specs.xlsx')
specs

#Importing Cars file
cars = pd.read_csv('Cars_22-23.csv')
cars

#Data Cleaning, convert year from int to string
cars['year'] = cars['year'].astype(str)
specs['Year'] = specs['Year'].astype(str)

#Data Cleaning, capitalize car makes
cars['make'] = cars['make'].str.capitalize()
cars

#Data Cleaning car models misspellings
cars['model'].replace(to_replace="LYRIQ",
           value="Lyriq", inplace=True)

cars['model'].replace(to_replace="CR-V",
           value="CRV", inplace=True)

cars['model'].replace(to_replace="RX",
           value="RX 350", inplace=True)
cars

#Creating unique ID for join/merging then removing trailing and leading empty spaces
cars["Year_Make_Model"] = cars[['year', 'make', 'model']].agg('_'.join, axis=1)
cars["Year_Make_Model"] = cars["Year_Make_Model"].str.strip()
cars

#Data Cleaning, removing trailing and leading empty spaces
#cars["Year_Make_Model"] = cars["Year_Make_Model"].str.strip()
#cars

#Creating unique ID for join/merging, then removing trailing and leading empty spaces
specs["Year_Make_Model"] = specs[['Year', 'Make', 'Model']].agg('_'.join, axis=1)
specs["Year_Make_Model"] = specs["Year_Make_Model"].str.strip()
specs

#Data Cleaning, removing trailing and leading empty spaces
#specs["Year_Make_Model"] = specs["Year_Make_Model"].str.strip()
#specs

#Joining cars and specs based on year, make and model
master_df=pd.merge(cars,specs, on='Year_Make_Model', how='left')
master_df

#Data Cleaning, dropping and renaming columns
master_df.drop(columns=['Year', 'Make', 'Model', 'ID'], inplace=True)
master_df.rename(columns={'year':'Year', 'make':'Make', 'model':'Model'}, inplace=True)
master_df.rename(columns={'body_styles':'Body Styles'}, inplace=True)
master_df

#Data Cleaning, calculating new column
master_df['Combined_Legroom'] = master_df['Front Legroom'] + master_df['Second Row Legroom']
master_df

#Number of models for each maker in 2022
cars_2022_df = master_df[master_df["Year"] == "2022"]
master_2022_cars_df = cars_2022_df['Make'].value_counts().rename_axis('Make').reset_index(name='Number of Models')
master_2022_cars_df

#Filtering to only see cars we are considering purchasing
my_choices_df = master_df[master_df["Gwen's Choice"] == "Y"]
my_choices_df

#Plotting with Bokeh

#Sorting my choices based on different sort values, this will be used to sort my plots.
my_choices_Legroom_df = my_choices_df.sort_values(by='Combined_Legroom')
my_choices_MSRP_df = my_choices_df.sort_values(by='MSRP')
my_choices_MPG_df = my_choices_df.sort_values(by='Combined Gas')


#Create ColumnDataSource from data frame, this will allow me to bring in column names in my plots.
source1 = ColumnDataSource(my_choices_MSRP_df)
source2 = ColumnDataSource(master_2022_cars_df)
source3 = ColumnDataSource(my_choices_Legroom_df)
source4 = ColumnDataSource(my_choices_MPG_df)

#Creating an output file, where the bokeh plots will be outputted to.
output_file('index.html')

#Car list
car_list1 = source1.data['Model'].tolist()
car_list2 = source2.data['Make'].tolist()
car_list3 = source3.data['Model'].tolist()
car_list4 = source4.data['Model'].tolist()


#Add plots. Creating 4 different plots to be in my bokeh grid.

#Plot #1
plot1 = figure(
       x_range=car_list1,
       plot_width=800,
       plot_height=600,
       title='Cars MSRP',
       y_axis_label='MSRP'
)

#Render glyph
plot1.vbar(
    x='Model',
    top='MSRP',
    bottom=0,
    width=0.4,
    color='lightsteelblue',
    fill_alpha = 0.7,
    source=source1
)
plot1.y_range.start = 0
plot1.xgrid.grid_line_color = None


#Plot #2
plot2 = figure(
       x_range=car_list2,
       plot_width=800,
       plot_height=600,
       title='Number of Models per Maker',
       y_axis_label='Number of Models'
)


#Render glyph
plot2.vbar(
    x='Make',
    top='Number of Models',
    bottom=0,
    width=0.4,
    color='lightsalmon',
    fill_alpha=0.7,
    source=source2
)
plot2.xaxis.major_label_orientation = pi/4
plot2.y_range.start = 0
plot2.xgrid.grid_line_color = None


#Plot 3
plot3 = figure(
       y_range=car_list3,
       #plot_width=800,
       #plot_height=600,
       title='Cars Legrooom',
       x_axis_label='Legroom (inches)'
)

#Render glyph
plot3.hbar(
    y='Model',
    right='Combined_Legroom',
    left=0,
    height=0.4,
    color='salmon',
    fill_alpha=0.9,
    source=source3
)
plot3.x_range.start = 0
plot3.ygrid.grid_line_color = None


#Plot #4
plot4 = figure(
       x_range=car_list4,
       plot_width=800,
       plot_height=600,
       title='Cars Combined Gas Mileage',
       y_axis_label='Combined Gas Mileage (mpg)'
)

#Render glyph
plot4.vbar(
    x='Model',
    top='Combined Gas',
    bottom=0,
    width=0.4,
    color='steelblue',
    fill_alpha=0.9,
    source=source4
)
plot4.y_range.start = 0
plot4.xgrid.grid_line_color = None



#Add Tooltips. These tooltips will pop up an image of the car when a bar in the plot is hovered over.
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Make @Model</h3>
        <div><strong>Price: </strong>$@MSRP</div>
        <div><strong>Legroom: </strong>@Combined_Legroom in</div>
        <div><img src="@Image" alt="" width="200" /></div>
    </div>
"""

plot1.add_tools(hover)
plot3.add_tools(hover)
plot4.add_tools(hover)



#Make a grid
grid = gridplot([[plot1, plot2], [plot3, plot4]], width=700, height=300)

#Show and save grid
save(grid)