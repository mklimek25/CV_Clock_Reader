import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import sqlite3 as sql
import pandas as pd
from dash.dependencies import Input, Output, State
from textwrap import dedent
import plotly.express as px
from datetime import datetime as dt

columns = []
background_color = '#21252C'
text_color = '#BB820F'
graph_color = '#E2E2E2'
border_color = 'white'
graph_format = {'layout': {'paper_bgcolor': background_color, 'plot_bgcolor': background_color}}
white_label_colors = 'white'
# functions that are played in callbacks:

def df_to_excel_go(file_name, stats_option):
    # print(stats_option)

    if stats_option == ["Yes"]:
        print("hello_this is line 18")
        df1 = df
        """gonna try a condition_block to fix my data and see if my code follows"""
        df1.loc['average'] = df1.mean(axis=0)
        df1.loc['standard deviation'] = df1.std(axis=0)
        df1.loc['max value'] = df1.max(axis=0)
        df1.loc['min value'] = df1.min(axis=0)


        print(df1.tail())
    else:
        df1 = df

    writer = pd.ExcelWriter('{0}.xlsx'.format(file_name))
    df1.to_excel(writer, index=True, freeze_panes=(1, 1), sheet_name="Data Output")
    worksheet = writer.sheets['Data Output']
    worksheet.set_column('B:BZ', 18)

    writer.save()
    print("done")
    print()




conn = sql.connect("../Data_Collection_Unit/Data1.sqlite")


df = pd.read_sql_query("SELECT * FROM data_bank INNER JOIN run_bank ON data_bank.run = run_bank.Run_number "
                             "INNER JOIN MDI_bank ON MDI_bank.MDI_Blend_index_id = run_bank.MDI_Blend_index_id_run "
                             "INNER JOIN polyol_bank ON run_bank.Polyol_Index_id_run = "
                          "polyol_bank.polyol_index_id LEFT JOIN QC_Bank ON data_bank.timestamp = "
                       "QC_bank.Datapoint_Timestamp ORDER BY data_bank.timestamp", conn)

# Why was this created?
# All of these columns are redundant, but nonetheless necessary for the creation of the dataframe
removal_list = ["Pentane_split_percent_MDI", "run_timestamp_start", "run_timestamp_end", "MDI_Blend_Index_id_run",
                "Polyol_Index_id_run", "Run_number", "MDI_timestamp_start", "MDI_timestamp_end",
                "polyol_timestamp_start", "polyol_timestamp_end", "MDI_Batch_Index_id", "Density_Block_Timestamp_1",
                "Density_Block_Timestamp_2", "Density_Block_Timestamp_3", "Density_Block_Timestamp_4",
                "QC_Production_Date_Timestamp", "QC_cut_date", 'Datapoint_Timestamp']
for item in removal_list:
    if item in df.columns:
        df = df.drop([item], axis=1)






for column in df.columns:

    """ONLY USE BELOW LINE FOR SELECT DATAFRAME"""

    """Need to remove all blanks in the database (two - vlues)
    Also need to transfer to datetimes in the dataframe to better conform to the px module"""
    """THIS BS EDITOR CAN BE REMOVED WHEN WE HAVE A BETTER DATASET"""

    if "timestamp" in column:
        # print(df["{0}".format(column)])
        df["{0}".format(column)] = pd.to_datetime(df['{0}'.format(column)], unit='s')

        """With the code below, I am converting all of my data information into floats. Floats and ints are
        the best way to make sure the pandas code, plot code, etc can effectively handle my data."""
    else:
        df.loc[df["{}".format(column)] == 'NA', '{}'.format(column)] = None
        df.loc[df["{}".format(column)] == 'N/A', '{}'.format(column)] = None
        df.loc[df["{}".format(column)] == '-', '{}'.format(column)] = None
        df.loc[df["{}".format(column)] == '', '{}'.format(column)] = None
        df.loc[df["{}".format(column)] == 'NaN', '{}'.format(column)] = None
        try:
            df = df.astype(({"{0}".format(column): float}))
            columns.append(column)
        except ValueError:
            pass
            # print("{0} NOT converted to float".format(column))

command_title = html.H4("Enter your commands below: ", style={'textAlign': 'center', 'color': text_color})
graph_title = html.H4("Timestamp vs density: ", id="graph_title", style={'textAlign': 'center', 'color': text_color})

conditions = []
cond_labels = []
conditions.append(html.Label("Time Range"))
conditions.append(dcc.DatePickerRange(
    id='date_range',  # ID used for callback
    calendar_orientation='horizontal',  # horizontal or vertical
    end_date_placeholder_text='Return',  #Placeholder when no end date was selected
    with_portal=False,  # if true will reopen in a full screen overlay
    first_day_of_week=0,  # (0 = Sunday)
    reopen_calendar_on_clear=True,
    is_RTL=False,  # direction of calender
    clearable=True,  #user can clear the dropdown
    number_of_months_shown=1,  # shows one month at a time
    min_date_allowed=dt(2020, 1, 1),
    max_date_allowed=dt(2020, 12, 31),
    initial_visible_month=dt(2020, 1, 1),
    start_date=dt(2020, 1, 1),
    end_date=dt(2020, 12, 31),
    display_format='MMM Do, YY',  # how selected dates are displayed in the datepicker component
    month_format='MMMM, YYYY',  # How month headers are displayed when the calender is open
    persistence=True,

))





for column in df.columns:
    if df[f"{column}"].dtype == float:
        if df[f"{column}"].max() == 0 and df[f"{column}"].min() == 0 or df[f"{column}"].max() == df[f"{column}"].min():
            pass
        else:
            cond_labels.append(column)
            cond_bar = []

            col_max = df[f"{column}"].max()
            col_min = df[f"{column}"].min()
            col_step = (col_max-col_min)/10
            # if column == "timestamp":
            #     marks_list = {round(col_min + i * col_step, 3): dt.fromtimestamp(round(col_min + i * col_step, 3)) for i in range(11)}
            g = [round(col_min + i * col_step, 3) for i in range(11)]
            marks_list = marks = {int(j) if j % 1 == 0 else j: '{}'.format(j) for j in g}
            cond_bar.append(column)
            cond_bar.append(col_max)
            cond_bar.append(col_min)
            conditions.append(html.Label(f"{column}"))
            conditions.append(dcc.RangeSlider(
                id="{}".format(column),
                marks=marks_list,
                min=col_min,
                max=col_max,
                step=((col_max-col_min)/20),
                value=[col_min, col_max],


            ))
            # print("{0}\n{1}".format(column, marks_list))
# print("cond labels: ")
# print(cond_labels)
select_button = dbc.Button("SELECT", id="button-train", style={'height': '30px', 'width': '200px',
                        'backgroundColor': text_color, 'color': white_label_colors})
"""NOTE: I think that my column marks and ranges are changing as the variables get redefined. 
I might need to make this a class to fix it as I have done before. I will evaluate further later.
CONFIRMED, we need a class"""

# print(cond_labels)
# print(conditions)

        # slider = dcc.RangeSlider(
        #     min=col_min,
        #     max=col_max,
        #     step=((col_max-col_min)/20)
        # )





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
avp_graph = dcc.Graph(id='avp-graph', figure={'layout': {'paper_bgcolor': background_color, 'plot_bgcolor': background_color}}, style={'height': '400px'})
div_alert = dbc.Spinner(html.Div(id="alert-msg"))
conditions_label = html.H4("Enter Conditions Below:", className="card-title", style={'color': text_color})
conditions_card = dbc.Card(conditions, body=True,
style={'height': '200px','overflow': 'scroll', 'backgroundColor': background_color, 'color': text_color}), div_alert





plt_command_title = html.Label("Plot Command Center")
graphtype_dropdown_label = html.Label("Select an Option", style={'color': text_color})
graphtype_dropdown = dcc.Dropdown(
    id='graph_dropdown',
    options=[  #Options must be based on dictionaries within a list
        {"label": "Excel File", "value": "excel"},
        {"label": "2D Graph", "value": "2D"},
        {"label": "3D Graph", "value": "3D"},
        {"label": "Box Plot", "value": "Box"},
    ],
    style={'backgroundColor': white_label_colors}
)

drop_list = ["Run_Number", 'run_timestamp_start', 'run_timestamp_end', 'MDI_Blend_Index_id_run',
             'Polyol_Index_id_run', 'Run_number', 'Density_Block_Timestamp_1',
             'Density_Block_Timestamp_2', 'Density_Block_Timestamp_3',
             'Density_Block_Timestamp_4', 'MDI_timestamp_start', 'MDI_timestamp_end', 'QC_Production_Date_Timestamp',
             'Run_Number', 'Datapoint_Timestamp']
column_labels = []
df_columns = []
stats_options_list = [{'label': 'Yes', 'value': 'Yes'},
                       {'label': 'No', 'value': 'No'}]
for column in df.columns:
    if column not in drop_list:
        label = {"label": "{}".format(column), "value": "{}".format(column)}
        column_labels.append(label)
        df_columns.append(column)
x_label = html.Label("X Value", style={'color': text_color})
x_dropdown = dcc.Dropdown(
    id='x_value',
    options=(column_labels),
    style={'backgroundColor': white_label_colors})
y_label = html.Label("Y Value", style={'color': text_color})
y_dropdown = dcc.Dropdown(
    id='y_value',
    options=(column_labels),
    style={'backgroundColor': white_label_colors})
z_label = html.Label("Z Value", style={'color': text_color})
z_dropdown = dcc.Dropdown(
    id='z_value',
    options=(column_labels),
    style={'backgroundColor': white_label_colors})
c_label = html.Label("C Value", style={'color': text_color})
c_dropdown = dcc.Dropdown(
    id='c_value',
    options=(column_labels),
    style={'backgroundColor': white_label_colors})
stats_option_label = html.Label("Would you like statistics added to the file?", style={'color': text_color})
stats_option = dcc.Checklist(id="excel_stats",  # these are the values that will be checked at the stat of the GUI
                             options=stats_options_list, style={'color': text_color})
label_input = html.Label("Please input file name", style={'color': text_color})
file_name = dcc.Input(
    id="file_name",
    placeholder="Input",
    type="text"  # 8 to 10 different inputs that can be accepted

)
selection_card_list = [x_label, x_dropdown, html.Br(), y_label,
                       y_dropdown, html.Br(), z_label, z_dropdown, html.Br(), c_label, c_dropdown, stats_option_label, stats_option,
                       label_input, file_name]
selection_card = dbc.Card(children=selection_card_list
    , id="selection_card",
    style={'height': '400px', 'overflow': 'scroll', 'backgroundColor': background_color},
)
command_card = dbc.Card(
    [
        graphtype_dropdown_label, graphtype_dropdown, html.Br(), selection_card
    ], id="command_card",
style={'height': '400px', 'overflow': 'scroll', 'backgroundColor': background_color,
       "border":{"width":"2px", "color":border_color}},
)

query = dedent("SELECT * FROM data_bank INNER JOIN run_bank ON data_bank.run = run_bank.Run_number "
               "INNER JOIN MDI_bank ON MDI_bank.MDI_Blend_index_id = run_bank.MDI_Blend_index_id_run "
               "INNER JOIN polyol_bank ON run_bank.Polyol_Index_id_run = "
               "polyol_bank.polyol_index_id LEFT JOIN QC_Bank ON data_bank.timestamp = "
               "QC_bank.Datapoint_Timestamp ORDER BY data_bank.timestamp")

query_card = dbc.Card(
    [
        html.H4("Auto-generated SQL Query", className="card-title"),
        dcc.Markdown(query, id="sql_query", style={'height': '200px', 'overflow': 'scroll'}),

    ],
    style={'height': '200px', 'overflow': 'scroll', 'color': text_color,
                                                            'backgroundColor': background_color},
body=True
)




"""OUR LAYOUT"""
app.layout = dbc.Container(  # container is a new one for us. we need to figure out how it works
    # it seems to contain everything, WILL UPDATE WITH MORE INFORMATION
    fluid=True,
    children=[html.H1("Eagle Eye", style={'height': '60px',
                                          'textAlign': 'center', 'backgroundColor': background_color, 'color': text_color}),
              html.Br(style={'color': background_color}),  # I believe this is the line separater
        dbc.Row(
            [
            dbc.Col(command_title, md=3),
        dbc.Col(graph_title, md=9),
        ], style={'backgroundColor': background_color}),

        dbc.Row(
            [
                dbc.Col(command_card, md=3),
                dbc.Col(avp_graph, md=9),
                # dbc.Col(["Details"])
            ]
        ),
        conditions_label,
        dbc.Row([dbc.Col(conditions_card),
                 dbc.Col(query_card)
                 ],
                ),
        html.Br(style={'height': '1px'}),
        dbc.Row(

                dbc.Col(select_button,
                        )

        ),
              ],
    style={"margin": "auto", 'backgroundColor': background_color},
)

a = ", ".join(cond_labels)
print(a)


"""In this app callback, the result of the conditions will impact my SQL Query"""
"""So apparently all outputs can only serve one callback function"""

# Need a callback to determine what is in my command line
@app.callback(
    Output("selection_card", "children"),
    Input('graph_dropdown', "value"),
)
def command_options(dropdown_value):  # below I am trying to limit what is being displayed to the selected option.

    # I need the ids to exist but the layout to chang
    if dropdown_value == "excel":
        label_input1 = label_input
        file_name1 = file_name
        stats_option1 = stats_option
        stats_option_label1 = stats_option_label
        x_dropdown1 = html.Label(None, id="x_value", style={'height': '0px'})
        x_label1 = html.Label(None, style={'height': '0px'})
        y_dropdown1 = html.Label(None, id="y_value", style={'height': '0px'})
        y_label1 = html.Label(None, style={'height': '0px'})
        z_dropdown1 = html.Label(None, id="z_value", style={'height': '0px'})
        z_label1 = html.Label(None, style={'height': '0px'})
        c_dropdown1 = html.Label(None, id="c_value", style={'height': '0px'})
        c_label1 = html.Label(None, style={'height': '0px'})
        select_options = [label_input1, file_name1, html.Br(),
            stats_option_label1, stats_option1, html.Br(),
            x_label1, x_dropdown1, html.Br(), y_label1,
            y_dropdown1, html.Br(), c_label1, c_dropdown1,
            z_label1, z_dropdown1]
        # print(select_options)

    elif dropdown_value == "2D":
        label_input1 = html.Label(None, style={'height': '0px'})
        file_name1 = html.Label(None, id="file_name", style={'height': '0px'})
        x_dropdown1 = x_dropdown
        x_label1 = x_label
        y_dropdown1 = y_dropdown
        y_label1 = y_label
        z_dropdown1 = html.Label(None, id="z_value", style={'height': '0px'})
        z_label1 = html.Label(None, style={'height': '0px'})
        c_dropdown1 = c_dropdown
        c_label1 = c_label
        stats_option1 = html.Label(None, id='excel_stats')
        select_options = [
             x_label1, x_dropdown1, html.Br(), y_label1,
            y_dropdown1, html.Br(), c_label1, c_dropdown1,
            z_label1, z_dropdown1, stats_option1, label_input1, file_name1
        ]
    elif dropdown_value == "3D":
        label_input1 = html.Label(None, style={'height': '0px'})
        file_name1 = html.Label(None, id="file_name", style={'height': '0px'})
        x_dropdown1 = x_dropdown
        x_label1 = x_label
        y_dropdown1 = y_dropdown
        y_label1 = y_label
        z_dropdown1 = z_dropdown
        z_label1 = z_label
        c_dropdown1 = c_dropdown
        c_label1 = c_label
        stats_option1 = html.Label(None, id='excel_stats')
        select_options = [
            x_label1, x_dropdown1, html.Br(), y_label1,
            y_dropdown1, html.Br(), z_label1, z_dropdown1, html.Br(), c_label1, c_dropdown1, stats_option1
            , label_input1, file_name1
        ]
    elif dropdown_value == "Box":
        label_input1 = html.Label(None, style={'height': '0px'})
        file_name1 = html.Label(None, id="file_name", style={'height': '0px'})
        x_dropdown1 = x_dropdown
        x_label1 = x_label
        y_dropdown1 = y_dropdown
        y_label1 = y_label
        z_dropdown1 = html.Label(None, id="z_value", style={'height': '0px'})
        z_label1 = html.Label(None, style={'height': '0px'})
        c_dropdown1 = html.Label(None, id="c_value", style={'height': '0px'})
        c_label1 = html.Label(None, style={'height': '0px'})
        stats_option1 = html.Label(None, id='excel_stats')
        x_value = x_label.children
        # print(x_value)
        # boxplot_label = dcc.RangeSlider(
        #     min=df[x_value].min(),
        #     max=df[x_value].max(),


        # )
        select_options = [
            x_label1, x_dropdown1, html.Br(), y_label1,
            y_dropdown1, html.Br(), c_label1, c_dropdown1,
            z_label1, z_dropdown1, stats_option1,
            label_input1, file_name1
        ]
    else:
        label_input1 = html.Label(None, style={'height': '0px'})
        file_name1 = html.Label(None, id="file_name", style={'height': '0px'})
        x_dropdown1 = x_dropdown
        x_label1 = x_label
        y_dropdown1 = y_dropdown
        y_label1 = y_label
        z_dropdown1 = html.Label(None, id="z_value", style={'height': '0px'})
        z_label1 = html.Label(None, style={'height': '0px'})
        c_dropdown1 = c_dropdown
        c_label1 = c_label
        stats_option1 = html.Label(None, id='excel_stats')
        select_options = [
            x_label1, x_dropdown1, html.Br(), y_label1,
            y_dropdown1, html.Br(), c_label1, c_dropdown1,
            z_label1, z_dropdown1, stats_option1, label_input1, file_name1
        ]



    return select_options




@app.callback(
    Output("sql_query", "children"),
    [Input("button-train", "n_clicks"),
    Input('date_range', 'start_date'),
     Input('date_range', 'end_date')],
    [State("{}".format(column), "value") for column in cond_labels])

def update_output(n_clicks, start_date, end_date, density, premix_flowrate, MDI_flowrate, Cat_1_flowrate,
                  Cat_2_flowrate, Cat_3_flowrate, Pentane_flowrate_MDI, Pentane_flowrate_Premix,
                  Total_Throughput, Total_percent_Catalyst, Blowing_Ratio, Premix_Temperature, MDI_Temperature,
                  Pentane_Temperature, Ambient_Temperature, Manifold_back_pressure, MDI_Line_Pressure,
                  Polyol_Line_Pressure, Mixer_Speed, Conveyor_Speed, Nucleation_Air_flow, Surfactant_part_by_weight,
                  TCPP_part_by_weight, Epon_part_by_weight, Water_part_by_weight,
                  Cat1_part_by_weight, Cat2_part_by_weight, Cat3a_part_by_weight, Cat3b_part_by_weight,
                  BlowingAgent_part_by_weight, Polyester_OH_content, Surfactant_OH_content, MDI_Blend_Index_id, MDI_Blended_Acidity,
                  MDI_Blended_pNCO_Content, MDI_Blended_Viscosity, polyol_index_id, polyol_bulk_OH_number,
                  polyol_fraction_HPU, polyol_fraction_Investa, QC_Block_Number, Density_Zone_1, Density_Zone_5,
                  Density_Zone_7, K_Factor_Zone_1, K_Factor_Zone_5, K_Factor_Zone_7, Friability, Average_cold_aging,
                  Average_Parralel_to_Rise_Compressive_Strength_Zone1,
                  Average_Parrallel_to_Rise_Compressive_Strength_Zone5,
                  Average_Parrallel_to_Rise_Compressive_Strength_Zone7,
                  Average_Parrallel_to_Rise_Compressive_Strength,
                  Perpendicular_to_Width_Compressive_Strength_Zone1,
                  Perpendicular_to_Width_Compressive_Strength_Zone5,
                  Perpendicular_to_Length_Compressive_Strength_Zone2):
    g = []
    changed_list = []
    try:
        start_date_timestamp = dt.strptime(start_date, '%Y-%m-%d').timestamp()
    except ValueError:
        start_date_timestamp = dt.strptime(start_date, '%Y-%m-%dT%H:%M:%S').timestamp()
    try:
        end_date_timestamp = dt.strptime(end_date, '%Y-%m-%d').timestamp()
    except ValueError:
        end_date_timestamp = dt.strptime(end_date, '%Y-%m-%dT%H:%M:%S').timestamp()

    # print(start_date_timestamp)
    # print(end_date_timestamp)
    # print(dt.timestamp(df["timestamp"].min()))
    ref = [density, premix_flowrate, MDI_flowrate, Cat_1_flowrate,
           Cat_2_flowrate, Cat_3_flowrate, Pentane_flowrate_MDI, Pentane_flowrate_Premix,
           Total_Throughput, Total_percent_Catalyst, Blowing_Ratio, Premix_Temperature,
           MDI_Temperature, Pentane_Temperature, Ambient_Temperature, Manifold_back_pressure,
           MDI_Line_Pressure, Polyol_Line_Pressure, Mixer_Speed, Conveyor_Speed, Nucleation_Air_flow,
           Surfactant_part_by_weight, TCPP_part_by_weight, Epon_part_by_weight,
           Water_part_by_weight, Cat1_part_by_weight, Cat2_part_by_weight, Cat3a_part_by_weight,
           Cat3b_part_by_weight, BlowingAgent_part_by_weight, Polyester_OH_content,
           Surfactant_OH_content, MDI_Blend_Index_id, MDI_Blended_Acidity, MDI_Blended_pNCO_Content,
           MDI_Blended_Viscosity, polyol_index_id, polyol_bulk_OH_number, polyol_fraction_HPU,
           polyol_fraction_Investa, QC_Block_Number, Density_Zone_1, Density_Zone_5, Density_Zone_7,
           K_Factor_Zone_1, K_Factor_Zone_5, K_Factor_Zone_7, Friability, Average_cold_aging,
           Average_Parralel_to_Rise_Compressive_Strength_Zone1,
           Average_Parrallel_to_Rise_Compressive_Strength_Zone5,
           Average_Parrallel_to_Rise_Compressive_Strength_Zone7, Average_Parrallel_to_Rise_Compressive_Strength,
           Perpendicular_to_Width_Compressive_Strength_Zone1, Perpendicular_to_Width_Compressive_Strength_Zone5,
           Perpendicular_to_Length_Compressive_Strength_Zone2]
    ref_string = (", ".join(df_columns))
    n = 0
    rr = "SELECT {} FROM data_bank INNER JOIN run_bank ON data_bank.run = run_bank.Run_number " \
         "INNER JOIN MDI_bank ON MDI_bank.MDI_Blend_index_id = run_bank.MDI_Blend_index_id_run " \
         "INNER JOIN polyol_bank ON run_bank.Polyol_Index_id_run = " \
         "polyol_bank.polyol_index_id LEFT JOIN QC_bank ON data_bank.timestamp = " \
         "QC_bank.Datapoint_Timestamp".format(ref_string)
    if float(dt.timestamp(df["timestamp"].min())) < float(start_date_timestamp) or float(dt.timestamp(df["timestamp"].max())) > float(end_date_timestamp):
        g.append('{0} BETWEEN {1} AND {2}'.format("timestamp", int(start_date_timestamp), int(end_date_timestamp)))
        changed_list.append('timestamp')
    for category in ref:
        m = cond_labels[n]
        if df["{}".format(m)].min() < category[0] or df["{}".format(m)].max() > category[1]:
            g.append('{0} BETWEEN {1} AND {2}'.format(cond_labels[n], category[0], category[1]))
            changed_list.append(cond_labels[n])

        n += 1
    if len(changed_list) == 0:
        pass
    else:
        rr += " WHERE " + " AND ".join(g)
    rr += " ORDER BY timestamp"
    print(rr)
    return rr

@app.callback(
    Output("avp-graph", "figure"),
    Output("graph_title", 'children'),
    [Input("sql_query", "children")],
    [State('graph_dropdown', "value"),
    State("x_value", "value"),
     State("y_value", "value"),
     State("c_value", "value"),
     State("z_value", "value"),
     State("file_name", "value"),
     State("excel_stats", "value")
     ]
)
def update_sql(sql_query, graph_option, x_value, y_value, c_value, z_value, file_name, stats_option):
    new_con = sql.connect("../Data_Collection_Unit/Data1.sqlite")
    df = pd.read_sql_query(sql_query, new_con)

    for column in df.columns:

        """ONLY USE BELOW LINE FOR SELECT DATAFRAME"""

        """Need to remove all blanks in the database (two - vlues)
        Also need to transfer to datetimes in the dataframe to better conform to the px module"""
        """THIS BS EDITOR CAN BE REMOVED WHEN WE HAVE A BETTER DATASET"""

        if "timestamp" in column:
            # print(df["{0}".format(column)])
            df["{0}".format(column)] = pd.to_datetime(df['{0}'.format(column)], unit='s')


            """With the code below, I am converting all of my data information into floats. Floats and ints are
            the best way to make sure the pandas code, plot code, etc can effectively handle my data."""
        else:
            df.loc[df["{}".format(column)] == 'NA', '{}'.format(column)] = None
            df.loc[df["{}".format(column)] == 'N/A', '{}'.format(column)] = None
            df.loc[df["{}".format(column)] == 'NaN', '{}'.format(column)] = None
            df.loc[df["{}".format(column)] == 'nan', '{}'.format(column)] = None
            df.loc[df["{}".format(column)] == '', '{}'.format(column)] = None
    df['run'] = df['run'].str.slice(3)
                # print("{0} NOT converted to float".format(column))









    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    graph_title = "Timestamp vs. Density Plot"
    title_list = []
    for value in [x_value, y_value, z_value, c_value]:
        if value is not None:
            title_list.append(value.capitalize())
    if len(title_list) != 0:
        graph_title = " vs. ".join([word for word in title_list])



    # if graph_option == "excel":
    #
    if graph_option == "excel":
        df_to_excel_go(file_name=file_name, stats_option=stats_option)
        avp_fig = None
        graph_title = None

    if graph_option == "2D":
        if x_value == None or y_value == None:
            print("Please Enter an x or y value")  # want this presented on the file at some point
            avp_fig = px.scatter()
        elif c_value == None:
            avp_fig = px.scatter(
                x=df["{}".format(x_value)],
                y=df["{}".format(y_value)],
                labels={"x": "{}".format(x_value), "y": "{}".format(y_value)},
                )
            # avp_fig.update_layout(paper_bgcolor=background_color, plot_bgcolor=graph_color, xaxis={"color": white_label_colors},
            #                       yaxis={"color": white_label_colors})
        else:
            avp_fig = px.scatter(
                x=df["{}".format(x_value)],
                y=df["{}".format(y_value)],
                color=df["{}".format(c_value)],
                labels={"x": "{}".format(x_value), "y": "{}".format(y_value), "color": "{}".format(c_value)})
            # avp_fig.update_layout(paper_bgcolor=background_color, plot_bgcolor=graph_color, xaxis={"color": white_label_colors},
            #                       yaxis={"color": white_label_colors}, legend={"color": white_label_colors})
    elif graph_option == "3D":
        if x_value is None or y_value is None or z_value is None:
            print("Please Enter an x, y, and z value")
            avp_fig = px.scatter()
        elif c_value is None:
            avp_fig = px.scatter_3d(data_frame=df, x=x_value, y=y_value, z=z_value,
                                    labels={"x": "{}".format(x_value), "y": "{}".format(y_value), "z": "{}".format(z_value)},
                                    )
        else:
            avp_fig = px.scatter_3d(data_frame=df, x=x_value, y=y_value, z=z_value, color=c_value,
                                    labels={"x": "{}".format(x_value), "y": "{}".format(y_value), "z": "{}".format(z_value), "color": "{}".format(c_value)},
                                    )
    elif graph_option == "Box":
        l = "{}_span".format(x_value)
        # Dataframe needed some serious cleanup before the box plot was able to work
        df1 = df[[x_value, y_value]].dropna()  # eliminated all rows with a none value
        df1 = df1.astype(({y_value: float}))  # converting necessary columns to floats to perform float related functions
        if x_value == "timestamp":
            df1[x_value] = pd.to_numeric(df[x_value])
            df1 = df1.astype(({x_value: float}))
            range_scope = (df1[x_value].max() - df1[x_value].min()) / 5
            df1['range_value'] = round(df1[x_value] / range_scope)
            df1[l] = (df1['range_value'] * range_scope)
            df1[l] = pd.to_datetime(df1[l])
            avp_fig = px.box(data_frame=df1, x=l, y=y_value, points='all')
        else:
            try:
                df1 = df1.astype(({x_value: float}))


                range_scope = (df1[x_value].max() - df1[x_value].min()) / 5
                df1['range_value'] = round(df1[x_value] / range_scope)
                df1[l] = (df1['range_value'] * range_scope)
                avp_fig = px.box(data_frame=df1, x=l, y=y_value, points='all')
            except ValueError:
                avp_fig = px.box(data_frame=df1, x=x_value, y=y_value, points='all')

    else:
        avp_fig = px.scatter(data_frame=df, x="timestamp", y="density",
        labels={"x": "{}".format(x_value), "y": "{}".format(y_value)})

    # avp_fig.update_layout(paper_bgcolor=background_color, plot_bgcolor=graph_color, xaxis={"color": white_label_colors},
    #                       yaxis={"color": white_label_colors}, colorway={'color': white_label_colors})

    # print("The following IDs are being displayed:\n"
    #       "x value: {0}\n y value: {1}\n z value: {2}\n c value: {3}".format(x_value, y_value, z_value, c_value))
    return avp_fig, graph_title

"""I just want a function that will return where I am on a ranged slider."""

if __name__ == "__main__":
    app.run_server(debug=True)