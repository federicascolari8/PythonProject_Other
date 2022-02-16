""" Utils for the web application

Author: Beatriz Negreiros

"""


from sedimentanalyst.app.appconfig import *
from sedimentanalyst.analyzer.statistical_analyzer import StatisticalAnalyzer

# Global variable for style args
style_upload = {
    'width': '100%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px'
}

intro_text = dcc.Markdown(
        '''
        ### Welcome
        
        Sediment Analyst is a web application coded in Python-3 to leverage a quick, interactive, and 
        visual sedimentological analyses. By inputting datasets of sieved class weights (see examples 
        [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx)), Sediment
        Analyst computes characteristic grain sizes (namely, d10, d16, d25, d30, d50, d60, d75, d84, d90), mean grain 
        size, geometrical mean grain size, porosity, and hydraulic conductivity estimators. Checkout:
        '''
        )
inputs_text = dcc.Markdown(
            '''
        ### Inputs
        Enter below the information regarding your files. When *index* is indicated, enter the
        __row index__, __column index__, separated by comma (,) in the fields below. For instance, if the 
        sample name lives on the row 0 (first row) and column 2 (third column): type 0,2 in the field *samplename*.
        The fields are currently filled in by default according to our template, which we made available 
        [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx).
        
        '''
        )
input_boxes = [
    dcc.Markdown(
        '''
        Delete default input values below for personalizing the parsing of the files contents when not using our 
        [template](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx).
        In following, press the 'RUN' buttom below '''),
    dcc.Input(id="header", type="number", placeholder="table's header", value=9),
    dcc.Input(id="gs_clm", type="number", placeholder="grain sizes table column number (start from zero)",
             value=1),
    dcc.Input(id="cw_clm", type="number", placeholder="class weight column number (start from zero)",
             value=2),
    dcc.Input(id="n_rows", type="number", placeholder="class weight column number (start from zero)",
             value=16),
    dcc.Input(id="porosity", type="number", placeholder="porosity index", value=2.4),
    dcc.Input(id="SF_porosity", type="number", placeholder="SF_porosity index", value=2.5),
    dcc.Input(id="index_lat", type="number", placeholder="latitute index", value=5.2),
    dcc.Input(id="index_long", type="number", placeholder="longitude index", value=5.3),
    dcc.Input(id="index_sample_name", type="number", placeholder="sample name index", value=6.2),
    dcc.Input(id="index_sample_date", type="number", placeholder="sample date index", value=4.2),
    dcc.Input(id="projection", type="text", placeholder="projection ex: epsg:3857", value="epsg:3857"),
               ]


# Auxiliary function for parsing contents of the files
def parse_contents(contents, filename, date, input):
    """
    Args:
        contents (Input('upload-data', 'contents'): contents of the file containing the sample data (class weights and
        corresponding grain sizes)
        filename (State('upload-data', 'filename')): filename
        date (State('upload-data', 'last_modified')):
        input (dict): index parameters input by the user necessary to read and parse the contents of the file
    Returns:
        Object of StatisticalAnalyzer and Div with reading messages
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), engine="openpyxl", header=None)

        # clean dataset
        dff = df.copy()
        columns_to_get = [input["gs_clm"], input["cw_clm"]]
        dff_gs = dff.iloc[input["header"]: input["header"] + input["n_rows"], columns_to_get]
        dff_gs.reset_index(inplace=True, drop=True)
        dff_gs = dff_gs.astype(float)

        # Get metadata from the dataframe
        # get sample name
        try:
            samplename = dff.iat[input["index_sample_name"][0], input["index_sample_name"][1]]
        except:
            samplename = None
            pass

        # get sample date
        try:
            sampledate = dff.iat[input["index_sample_date"][0], input["index_sample_date"][1]]
        except:
            sampledate = None
            pass

        # get sample coordinates
        try:
            lat = dff.iat[input["index_lat"][0], input["index_lat"][1]]
            long = dff.iat[input["index_long"][0], input["index_long"][1]]
        except:
            lat, long = None, None
            pass

        # get porosity
        try:
            porosity = dff.iat[input["porosity"][0], input["porosity"][1]]
        except Exception as e:
            porosity = None
            print(e)
            pass

        # get sf_porosity
        try:
            sf_porosity = dff.iat[input["SF_porosity"][0], input["SF_porosity"][1]]
        except Exception as e:
            sf_porosity = 6.1  # default for rounded sediments
            print(e)
            pass

        metadata = [samplename, sampledate, (lat, long), porosity, sf_porosity]

        # Rename and standardize the Grain Size dataframe
        dff_gs.rename(columns={dff_gs.columns[0]: "Grain Sizes [mm]", dff_gs.columns[1]: "Fraction Mass [g]"},
                      inplace=True)

        analyzer = StatisticalAnalyzer(input=input, sieving_df=dff_gs, metadata=metadata)

    except Exception as e:
        print(e)
        return html.Div([filename,
                         ': There was an error processing the file. '
                         'Ensure that your file does not contain too many columns (< 15).'
                         ])

    return analyzer, html.Div([filename, ': File successfully read'])
