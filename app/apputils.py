"""
Utils for the web application
"""
from config import *
from app.appconfig import *
from statisticalanalyzer.statistical_analyzer import StatisticalAnalyzer

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
