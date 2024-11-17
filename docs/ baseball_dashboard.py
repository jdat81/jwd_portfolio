from bokeh.io import output_notebook, show
from bokeh.layouts import column, row
from bokeh.models import Select, CustomJS
from bokeh.plotting import figure
import pandas as pd
from pybaseball import statcast_batter, playerid_lookup

output_notebook()

# Get initial data
initial_data = get_player_data('Aaron Judge')
source = ColumnDataSource(initial_data)

# Create figure
p = figure(height=600, width=800, tools='pan,box_zoom,hover,reset')

# Add scatter
scatter = p.scatter('launch_speed', 'launch_angle', source=source)

# Create JavaScript callback
callback = CustomJS(args=dict(source=source), code="""
    // JavaScript callback code here
    // This would update the data when selections change
""")

# Create widgets with JS callbacks
x_select = Select(title='X-Axis', value='launch_speed', options=columns)
x_select.js_on_change('value', callback)

y_select = Select(title='Y-Axis', value='launch_angle', options=columns)
y_select.js_on_change('value', callback)

# Create layout
layout = row(column(x_select, y_select), p)

# Show the plot
show(layout)