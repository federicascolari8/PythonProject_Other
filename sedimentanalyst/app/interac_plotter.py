""" Module designated for the Interactive Plotter

Author : Federica Scolari

"""

from sedimentanalyst.app.appconfig import *


class InteractivePlotter:
    def __init__(self, df):
        self.df = df

    def convert_coordinates(self, df, projection):
        """
        Method which transforms the coordinates of a give projection to degrees
        :param df: dataframe on which the coordinate transformation is applied
        :param projection: name of the initial projection
        :return: df
        """
        # import projections
        inproj = CRS.from_string(projection)  # Pseudo mercator
        outproj = CRS.from_string('epsg:4326')  # WGS 83 degrees

        iter = 0
        for y1, x1 in df[["lat", "lon"]].itertuples(index=False):
            x2, y2 = transform(inproj, outproj, x1, y1)

            # solution without correction
            df.at[iter, "lat"] = x2
            df.at[iter, "lon"] = y2

            iter += 1

        return df

    def create_map(self, df, projection='epsg:3857', samples=None):
        """
        create a scatter map based on the dataframe
        :param df: dataframe on which the coordinate transformation is applied
        :param projection: name of the initial projection
        :param samples: sample names
        :return: fig
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

        fig.update_layout(
            mapbox_style="open-street-map",
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    def plot_barchart(self, param, samples):
        """
        Method to outputs the results in a bar chart for the interactive comparison of the results
        :param param: statistical parameters selectable from the user
        :param samples: sample names
        :return: fig
        """

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

    def plot_gsd(self, samples):
        """
        Method which plots the cumulative grain size distribution curve for all selected samples
        :param samples: sample names
        :return: fig
        """
        # filter samples given sample name
        df = self.df[self.df["sample name"].isin(samples)]

        # filter only grain size, samples name and class weight
        df_gsd = df.set_index("sample name").iloc[:, 33:49].stack().reset_index()

        # rename columns for future reference
        df_gsd.rename(columns={df_gsd.columns[1]: "gsd", df_gsd.columns[2]: "cw"}, inplace=True)

        # create Grain Size Distribution outputs
        fig = px.line(df_gsd, x="gsd", y="cw",
                      labels={"gsd": "Grain Size [mm]", "cw": "Percentage [%]", "sample name": "Sample Name"},
                      color='sample name', title="Grain Size Distribution Curve")

        fig.update_xaxes(type="log")

        fig.update_layout(title_font_size=20,
                          legend_bordercolor='darkgrey')

        # the plot's layout is modified to improve visuals
        fig.update_xaxes(type='category', autorange="reversed",
                         showline=True, mirror=True,
                         ticks='outside', linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        fig.update_yaxes(showline=True, mirror=True,
                         ticks='outside', linewidth=2,
                         linecolor='black', title_font_size=14,
                         gridcolor='darkgrey')

        return fig

    def plot_diameters(self, samples):
        """
        Method which plots the cumulative grain size distribution curve for all selected samples
        :param samples: sample names
        :return: fig
        """
        # filter samples given sample name
        df = self.df[self.df["sample name"].isin(samples)]

        x = df["sample name"].tolist()
        fig = go.Figure()

        diams_values_per_sample = df.iloc[:, 4:13]

        diams_title = df.columns[4:13].tolist()

        # enables proper view of the barchart with the overlay barmode
        for n in range(8, -1, -1):
            fig.add_trace(go.Bar(x=x, y=diams_values_per_sample.iloc[:, n].tolist(), name=diams_title[n]))

        fig.update_layout(barmode='overlay', title="Overview of Diameters",
                          title_font_size=20, legend_title="Diameters",
                          legend_bordercolor='darkgrey')

        fig.update_xaxes(title="Sample Name", linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        fig.update_yaxes(title="Diameter Size [mm]", linewidth=2, title_font_size=14,
                         linecolor='black', gridcolor='darkgrey')

        return fig
