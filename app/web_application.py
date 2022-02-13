""" Module designated for the web application

Author : Beatriz Negreiros

"""

from app.interac_plotter import InteractivePlotter
from statisticalanalyzer.utils import *
from app.apputils import *
from config import *
from app.appconfig import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

'Instantiates object app of the class Dash'
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True, title='Sediment Analyst')
# server = app.server  # method to serve the app, allows heroku to recognize the server

# App layout
app.layout = html.Div(
    children=[  # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
        html.H1("Sediment Analyst", style={'text-align': 'center'}),  # header
        html.Img(src='https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/river_inn.png',
                 style={'width': '100%', 'height': '500px', 'display': 'inline-block !important', 'margin': 'auto !important'}),  # Image
        dcc.Markdown(  # Web description
            '''
        #### Introduction
        
        Sediment Analyst is a web application coded in Python-3 to leverage a quick, interactive, and 
        visual sedimentological analyses. By inputting datasets of sieved class weights (see examples 
        [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx)), Sediment
        Analyst computes characteristic grain sizes (namely, d10, d16, d25, d30, d50, d60, d75, d84, d90), mean grain 
        size, geometrical mean grain size, porosity, and hydraulic conductivity estimators. Checkout:
        '''
        ),
        html.Br(),
        dcc.Markdown(
            '''
        #### Inputs
        Enter below the information regarding your files. When *index* is indicated, enter the
        __row index__, __column index__, separated by comma (,) in the fields below. For instance, if the 
        sample name lives on the row 0 (first row) and column 2 (third column): type 0,2 in the field *samplename*.
        The fields are filled in by default according to a standard file sheet, which we made available 
        [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx).
        
        '''
        ),
        html.Br(),

        # manual inputs set as default according to the excel template, but can be changed in the interface
        dcc.Input(id="header", type="number", placeholder="table's header", value=9),
        dcc.Input(id="gs_clm", type="number", placeholder="grain sizes table column number (start from zero)", value=1),
        dcc.Input(id="cw_clm", type="number", placeholder="class weight column number (start from zero)", value=2),
        dcc.Input(id="n_rows", type="number", placeholder="class weight column number (start from zero)", value=16),
        dcc.Input(id="porosity", type="number", placeholder="porosity index", value=2.4),
        dcc.Input(id="SF_porosity", type="number", placeholder="SF_porosity index", value=2.5),
        dcc.Input(id="index_lat", type="number", placeholder="latitute index", value=5.2),
        dcc.Input(id="index_long", type="number", placeholder="longitude index", value=5.3),
        dcc.Input(id="index_sample_name", type="number", placeholder="sample name index", value=6.2),
        dcc.Input(id="index_sample_date", type="number", placeholder="sample date index", value=4.2),
        dcc.Input(id="projection", type="text", placeholder="projection ex: epsg:3857", value="epsg:3857"),
        html.Br(),
        html.Br(),
        html.Button("run", id="btn_run"),

        # store input indexes (row column containing sample information)
        dcc.Store(id="store_manual_inputs"),
        html.Br(),
        # files upload
        dcc.Upload(  # drop and drag upload area for inputting files
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style=style_upload,
            multiple=True  # Allow multiple files to be uploaded
        ),

        # store global dataframe
        dcc.Store(id='stored-data'),

        # html.Div(id='output-div'),
        html.Div(id='output-messages'),

        # drop box with sample names
        html.Div(id="dropdown-sample_id"),
        html.Br(),

        # map
        html.Div(id="div-map"),
        html.Br(),

        # dropdown with type of statistics
        html.Div(id="div-stat-drop"),

        # histogram
        html.Div(id="div-histogram"),

        # grain size distribution
        html.Div(id="div-gsd"),

    ])


# Callback for the Upload (Drag and Drop or Select Files) box
@app.callback(Output('output-messages', 'children'),
              Output('stored-data', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State("store_manual_inputs", 'data'),
              Input("btn_run", "n_clicks"),
              prevent_initial_call=True,
              )
def update_output(list_of_contents, list_of_names, list_of_dates, input, click):
    if list_of_contents is not None:
        df_global = pd.DataFrame()
        children = []
        analyzers = []

        # iterating through files and appending reading messages as well as
        # analysis objects (analyzers)
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            from_parsing = parse_contents(c, n, d, input)
            # children.append(from_parsing[1])
            analyzers.append(from_parsing[0])
        # append all information from the list of analyzers into a global df
        for inter_analyzer in analyzers:
            df_global = append_global(obj=inter_analyzer,
                                      df=df_global
                                      )
        # return children
        data2 = df_global.to_dict("split")
        children.append(html.Div([
            html.Button("Download Summary Statistics", id="btn_download"),
            dcc.Download(id="download-dataframe-csv"),
        ])
        )
        children.append(data2)

        return children


# Callback for button for downloading summary statistics of all input samples
@app.callback(
    Output("download-dataframe-csv", "data"),
    State('stored-data', 'data'),
    Input("btn_download", "n_clicks"),
    prevent_initial_call=True,
)
def download_summary_stats(data, n_clicks):
    dataframe_global = pd.DataFrame(data=data["data"], columns=data["columns"])
    return dcc.send_data_frame(dataframe_global.to_csv, "overall_statistics.csv")


# Callback for creating map with sample locations and computed sed. statistics
@app.callback(
    Output('div-map', 'children'),
    State('stored-data', 'data'),
    Input("sample_id", "value"),
    prevent_initial_call=True
)
def update_map(data, samples):
    df = pd.DataFrame(data=data["data"], columns=data["columns"])
    int_plot = InteractivePlotter(df)
    fig = int_plot.create_map(df=df, samples=samples)
    fig.update_layout(transition_duration=500)
    return dcc.Graph(id="map", figure=fig)


# Callback for storing input dictionary necessary to read the user-inputed files
@app.callback(
    Output("store_manual_inputs", "data"),
    State('header', 'value'),
    State('gs_clm', 'value'),
    State('cw_clm', 'value'),
    State('n_rows', 'value'),
    State('porosity', 'value'),
    State('SF_porosity', 'value'),
    State('index_lat', 'value'),
    State('index_long', 'value'),
    State('index_sample_name', 'value'),
    State('index_sample_date', 'value'),
    State('projection', 'value'),
    Input("btn_run", "n_clicks"),
    # prevent_initial_call=True,
)
def save_inputs(header, gs_clm, cw_clm, n_rows, porosity,
                sf_porosity, index_lat, index_lon,
                sample_name_index, sample_date_index,
                projection, clicks):
    # transform float values into list
    porosity_index = list(map(int, str(porosity).split("."))) if porosity is not None else None
    sf_porosity_index = list(map(int, str(sf_porosity).split("."))) if sf_porosity is not None else None
    lat_index = list(map(int, str(index_lat).split("."))) if index_lat is not None else None
    lon_index = list(map(int, str(index_lon).split("."))) if index_lon is not None else None
    name_index = list(map(int, str(sample_name_index).split("."))) if sample_name_index is not None else None
    date_index = list(map(int, str(sample_date_index).split("."))) if sample_date_index is not None else None

    # create dictionary with all inputs
    input = dict(header=header, gs_clm=gs_clm, cw_clm=cw_clm, n_rows=n_rows, porosity=porosity_index,
                 SF_porosity=sf_porosity_index, index_lat=lat_index, index_long=lon_index,
                 index_sample_name=name_index, index_sample_date=date_index, projection=projection)
    return input


# Callback for plotting histogram of the statistic; uses the class InteracPlotter
@app.callback(
    Output('div-histogram', 'children'),
    State('stored-data', 'data'),
    Input("sample_id", "value"),
    Input("statistics_id", "value"),
    prevent_initial_call=True
)
def update_histogram(data, samples, stat_value):
    # save into dataframe
    df = pd.DataFrame(data=data["data"], columns=data["columns"])

    # filter samples given sample name
    df = df[df["sample name"].isin(samples)]

    # filter samples given statistic
    df = df.iloc[:, 4:23]
    i_plotter = interac_plotter.InteractivePlotter(df)
    fig = i_plotter.plot_histogram(param=stat_value, samples=samples)
    # fig.update_layout(transition_duration=500)
    return dcc.Graph(id='output-histogram',
                     figure=fig,
                     style={'display': 'inline-table',
                            'width': '75%',
                            'text-align': 'center'}
                     )


# Callback for updating campaign information (or id)
@app.callback(Output("dropdown-sample_id", "children"),
              Input("btn_run", "n_clicks"),
              State('stored-data', 'data'),
              prevent_initial_call=True  # prevents that this callback is ran
              # before the inputs (outputs of previous callbacks) are available
              )
def update_sample_id(n_clicks, data):  # n_clicks is mandatory even if not used
    df = pd.DataFrame(data=data["data"], columns=data["columns"])
    samples = df["sample name"].tolist()

    return dcc.Dropdown(id="sample_id",
                        options=[{"label": x, "value": x}
                                 for x in samples],
                        value=samples,
                        multi=True
                        )


# Callback for dropdown for the user to select the desired statistic
@app.callback(Output("div-stat-drop", "children"),
              Input("btn_run", "n_clicks"),
              State('stored-data', 'data'),
              prevent_initial_call=True,
              )
def update_stat_drop(n_clicks, data):
    df = pd.DataFrame(data=data["data"], columns=data["columns"])
    statistics = df.columns[4:23].tolist()

    return dcc.Dropdown(id="statistics_id",
                        options=[{"label": x, "value": x}
                                 for x in statistics],
                        value=statistics[0],
                        multi=False
                        )


@app.callback(
    Output('div-gsd', 'children'),
    State('stored-data', 'data'),
    Input("sample_id", "value"),
    prevent_initial_call=True
)
def update_gsd(data, samples):
    # save into dataframe
    df = pd.DataFrame(data=data["data"], columns=data["columns"])

    # filter samples given sample name
    df = df[df["sample name"].isin(samples)]

    i_plotter_2 = interac_plotter.InteractivePlotter(df)
    fig = i_plotter_2.plot_gsd(samples)

    return dcc.Graph(id="gsd",
                     figure=fig,
                     style={'display': 'inline-table',
                            'width': '75%',
                            'text-align': 'center'},
                     )


if __name__ == '__main__':
    app.run_server(debug=True)
