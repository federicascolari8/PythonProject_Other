""" Module designated for the Interactive Plotter

Author : Federica Scolari

"""

from config import *
from app.appconfig import *

class InteractivePlotter:
    def __init__(self, df):
        self.df = df

    def plot_histogram(self, param, samples):

        #Create a new dataframe, with two columns: one to identify the samples' name and one for their corresponding value

        new_df = {"sample name": samples, "parameters": self.df[f"{param}"]}
        new_df = pd.DataFrame(new_df)
        # Bar Chart creation
        fig = px.bar(new_df,
                           x="sample name",
                           y="parameters",
                           labels = { "sample name": "Sample Name", "parameters": f"{param} Value"},
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
        # filter samples given sample name
        df = self.df[self.df["sample name"].isin(samples)]

        # filter only grain size, samples name and class weight
        df_gsd = df.set_index("sample name").iloc[:, 33:49].stack().reset_index()

        # rename columns for future reference
        df_gsd.rename(columns={df_gsd.columns[1]: "gsd", df_gsd.columns[2]: "cw"}, inplace=True)

        # create Grain Size Distribution plot
        fig = px.line(df_gsd, x="gsd", y="cw",
                      labels={"gsd": "Grain Size [m]", "cw": "Percentage [%]", "sample name": "Sample Name"},
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
