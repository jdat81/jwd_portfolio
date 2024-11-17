import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.plotting import curdoc, figure
from pybaseball import statcast_batter, playerid_lookup

# Event colors with more diverse hues
COLORS = {
    'single': '#2ecc71',      # Green
    'double': '#3498db',      # Blue
    'triple': '#9b59b6',      # Purple
    'home_run': '#e74c3c',    # Red
    'walk': '#f39c12',        # Orange
    'strikeout': '#e67e22',   # Dark Orange
    'field_out': '#34495e'    # Navy Blue
}

# Top 10 HR hitters
TOP_10_PLAYERS = [
    'Aaron Judge',  # 58 HR
    'Shohei Ohtani',  # 54 HR
    'Anthony Santander',  # 44 HR
    'Juan Soto',  # 41 HR
    'Jose Ramirez',  # 39 HR
    'Brent Rooker',  # 39 HR
    'Marcell Ozuna',  # 39 HR
    'Kyle Schwarber',  # 38 HR
    'Gunnar Henderson',  # 37 HR
    'Ketel Marte'  # 36 HR
]


def get_player_data(player_name):
    try:
        parts = player_name.split()
        last_name = parts[-1]
        first_name = ' '.join(parts[:-1])

        player_info = playerid_lookup(last_name, first_name)
        if not player_info.empty:
            player_id = player_info.iloc[0]['key_mlbam']
            data = statcast_batter('2024-03-22', '2024-09-29', player_id)
            return data
    except Exception as e:
        print(f"Error getting data for {player_name}: {str(e)}")
    return pd.DataFrame()


# Set up columns for plotting
stats_columns = [
    'launch_speed',
    'launch_angle',
    'hit_distance_sc',
    'estimated_ba_using_speedangle',
    'estimated_woba_using_speedangle',
    'bat_speed',
    'swing_length'
]

# Get initial data
df = get_player_data('Aaron Judge')


def create_figure():
    if df.empty:
        p = figure(height=600, width=800, tools='pan,box_zoom,hover,reset')
        p.text(x=0, y=0, text=['No data available'])
        return p

    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.replace('_', ' ').title()
    y_title = y.value.replace('_', ' ').title()

    p = figure(height=600, width=800, tools='pan,box_zoom,hover,reset')
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    # Set Arial font
    p.title.text_font = "Arial"
    p.xaxis.axis_label_text_font = "Arial"
    p.yaxis.axis_label_text_font = "Arial"

    # Set up colors based on events or default color
    if color.value != 'None':
        c = [COLORS.get(event, '#bdc3c7') if event == color.value else '#bdc3c7'
             for event in df['events']]
    else:
        c = '#31AADE'  # Default color when no event is selected

    # Add hover tooltips
    p.hover.tooltips = [
        ('Player', player.value),
        ('Event', '@events'),
        (x_title, f'@{x.value}'),
        (y_title, f'@{y.value}')
    ]

    p.scatter(x=xs, y=ys, color=c, size=9, line_color="white",
              alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p


def update(attr, old, new):
    global df
    if attr == 'value' and player.value != old:
        df = get_player_data(player.value)
    layout.children[1] = create_figure()


# Create Select widgets
player = Select(title='Player', value='Aaron Judge', options=TOP_10_PLAYERS)
player.on_change('value', update)

x = Select(title='X-Axis', value='launch_speed', options=stats_columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='launch_angle', options=stats_columns)
y.on_change('value', update)

color = Select(title='Event Type', value='None',
               options=['None', 'single', 'double', 'triple', 'home_run',
                        'walk', 'strikeout', 'field_out'])
color.on_change('value', update)

# Layout
controls = column(player, x, y, color, width=200)
layout = row(controls, create_figure())

# Initialize
curdoc().add_root(layout)
curdoc().title = "Baseball Statistics"