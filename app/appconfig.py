try:
    import base64
    import io
    from app import interac_plotter
    import dash
    import plotly.express as px
    from dash import dcc, Input, Output, State, html
    from pyproj import Proj, transform, CRS
except ImportError:
    print(
        "Error importing necessary packages")

