""" Module designated for the Interactive Plotter

Author : Federica Scolari

"""

from config import *
from app.appconfig import *
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots


class InteractivePlotter:
    def __init__(self, df):
        self.df = df

    def convert_coordinates(self, df, projection):
        """
        transform coordinates of a give projection in degrees
        :param df:
        :param projection:
        :return:
        """
        # import projections
        inproj = CRS.from_string(projection)  # Pseudo mercator
        outproj = CRS.from_string('epsg:4326')  # WGS 83 degrees

        iter = 0
        for y1, x1 in df[["lat", "lon"]].itertuples(index=False):
            x2, y2 = transform(inproj, outproj, x1, y1)

            # solution with out correction
            df.at[iter, "lat"] = x2
            df.at[iter, "lon"] = y2

            iter += 1

        return df

    def create_map(self, df, projection="epsg:3857", samples=None):
        """
        create a scatter map based on the dataframe
        :param df:
        :param projection:
        :param samples:
        :return:
        """

        # convert coordinates to input projection
        df = self.convert_coordinates(df=df,
                                      projection=projection)
        # filter samples given inside dropdown
        df = df[df["sample name"].isin(samples)]

        # create scatter with Open Street Map
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df["lon"],
                                hover_name="sample name",
                                hover_data=df.columns[4:22],
                                color='sample name',
                                zoom=11)
        # Open street map mapbox/works for everywhere

        # USGS mapbox/works is a very good resolution for the US
        # but not for EU.

        fig.update_layout(
            mapbox_style="open-street-map",
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    def plot_histogram(self, param, samples):

        # Create a new dataframe, with two columns:
        # one to identify the samples' name and one for their corresponding value

        new_df = {"sample name": samples, "parameters": self.df[f"{param}"]}
        new_df = pd.DataFrame(new_df)
        # Bar Chart creation
        fig = px.bar(new_df,
                     x="sample name",
                     y="parameters",
                     labels={"sample name": "Sample Name", "parameters": f"{param} Value"},
                     color="sample name", title="Bar Chart of Statistics")

        # Modify title font size
        fig.update_layout(title_font_size=20,
                          legend_bordercolor='darkgrey')

        # Plot's layout is modified to improve visuals
        fig.update_xaxes(linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        fig.update_yaxes(linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        return fig

    # def plot_histogram(self, param, samples):
    #     params = self.df.columns[0:9].tolist()
    #     fig = make_subplots(rows=3, cols=3, subplot_titles=params)
    #     xpos = 1
    #     ypos = 1
    #     # I had to create this "for cycle" with xpos and ypos to avoid manually adding every trace one by one
    #     for par in params:
    #         fig.append_trace(go.Bar(x=samples, y=self.df[par]), ypos, xpos)
    #         if xpos % 3 == 0:
    #             xpos = 1
    #             ypos += 1
    #         else:
    #             xpos += 1
    #
    #     fig.update_layout(title_text="Samples divided by parameter", showlegend=False)
    #
    #     return fig

    def plot_gsd(self, samples):
        # filter samples given sample name
        df = self.df[self.df["sample name"].isin(samples)]

        # filter only grain size, samples name and class weight
        df_gsd = df.set_index("sample name").iloc[:, 33:49].stack().reset_index()

        # rename columns for future reference
        df_gsd.rename(columns={df_gsd.columns[1]: "gsd", df_gsd.columns[2]: "cw"}, inplace=True)

        # create Grain Size Distribution plot
        fig = px.line(df_gsd, x="gsd", y="cw",
                      labels={"gsd": "Grain Size [mm]", "cw": "Percentage [%]", "sample name": "Sample Name"},
                      color='sample name', title="Grain Size Distribution Curve")

        # Set xaxis scale as log
        fig.update_xaxes(type="log")

        # Modify title font size
        fig.update_layout(title_font_size=20,
                          legend_bordercolor='darkgrey')

        # Plot's layout is modified to improve visuals

        fig.update_xaxes(type='category', autorange="reversed",
                         showline=True, mirror=True,
                         ticks='outside', linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        fig.update_yaxes(showline=True, mirror=True,
                         ticks='outside', linewidth=2,
                         linecolor='black', title_font_size=14,
                         gridcolor='darkgrey')

        return fig
