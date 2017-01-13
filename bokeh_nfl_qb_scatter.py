import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool

#store csv as data frame 
df = pd.read_csv('2016_nfl_week15_qbs.csv')

output_file("nfl_qb_passes.html")

#source data for plot
source = ColumnDataSource(data=dict(x=df['comp_pass'],y=df['td_pass'],desc=df['player'], desc1=df['team']))

#pandas column named mapped to hovertools that show up when 'hovering' over each glyph 
hover = HoverTool(
        tooltips=[
            ("Player", "@desc"),
            ("Team", "@desc1")
        ]
    )

#configure color settings
p = figure(background_fill_color='black', plot_width=650, plot_height=500, tools=[hover])

#changes gridline colors 
p.xgrid.grid_line_color = 'white'
p.ygrid.grid_line_color = 'white'

#set axes and title 
p.title = "Quarterback Data"
p.xaxis.axis_label = 'Pass Completions'
p.yaxis.axis_label = 'Touchdown Passes'

#define type of glyph to use and color...
p.circle('x', 'y', size=10, source=source, color = 'black', line_color='white', alpha= 0.5)

#launch in browser
show(p)
