"""
    This files contains all the major functions

    We have functions for getting the data from file and processing as well 
    as generating the actual charts.

    This file is called by both the main app as well as the business logic

    Note: It's called silently by plotly express, but the statsmodels
    package is also a requirement.  This is because we are using linear
    regression lines in the basic_chart function.

"""
import pandas as pd
import numpy as np
import layout_configs as lc
import plotly.graph_objects as go
import plotly.express as px

#############################################################################
# Configuration - Change these to suit
#############################################################################
# Path location
# If using the code as-is from the repository, this should not need to be
# changed.  If you move the data location, then set this path to where the
# data file exists.
base_path = "./data/"


#############################################################################
# Data Retreival and Handling
#############################################################################
"""
    These functions are designed to get the data, process the data, and ready 
    it for working.

    Generally, I use a database backend, but for the sake of this dashboard,
    I'm using a plain CSV dump from the raw data table.

    The data format is:
        report_date (DATE)
        data (NUMERIC / FLOAT)
        report_name (STRING)
        hash (STRING - MD5 hashed values for table)
        release_date (DATE)

    Functions are defined that they can be easily adapted to pulling the data
    from a different source type if desired.
"""
# Base retrieval function - reads from CSV
def get_fed_data():
    # file_path = base_path + "fed_data.csv"
    file_path = base_path + "fed_dump.csv"
    df = pd.read_csv(file_path, na_values="x")
    df.rename(
        {"data": "report_data", "hash": "report_hash"},
        axis=1,
        inplace=True,
    )
    df["report_date"] = df["report_date"].values.astype("datetime64[D]")
    df["release_date"] = df["release_date"].values.astype("datetime64[D]")

    return df


# Function to add report labels to the dataframe
# ** Don't run this on the full data set - it's brutal
# Run this on a subset to provide labels and context.
def add_report_long_names(df1):
    df = df1.copy()
    for index in df.index:
        if df.loc[index, "report_name"] == "WM1NS":
            df.loc[index, "report_long_name"] = "M1 Money Supply"
            df.loc[index, "category"] = "Economy - Weekly"
        if df.loc[index, "report_name"] == "WM2NS":
            df.loc[index, "report_long_name"] = "M2 Money Supply"
            df.loc[index, "category"] = "Economy - Weekly"
        if df.loc[index, "report_name"] == "ICSA":
            df.loc[index, "report_long_name"] = "Initial Unemployment"
            df.loc[index, "category"] = "Employment - Weekly"
        if df.loc[index, "report_name"] == "CCSA":
            df.loc[index, "report_long_name"] = "Continued Unemployment"
            df.loc[index, "category"] = "Employment - Weekly"
        if df.loc[index, "report_name"] == "JTSJOL":
            df.loc[index, "report_long_name"] = "Job Openings: Total Nonfarm"
            df.loc[index, "category"] = "Employment"
        if df.loc[index, "report_name"] == "PAYEMS":
            df.loc[index, "report_long_name"] = "Non-Farm Employment"
            df.loc[index, "category"] = "Employment"
        if df.loc[index, "report_name"] == "NPPTTL":
            df.loc[
                index, "report_long_name"
            ] = "Total Nonfarm Private Payroll Employment (ADP)"
            df.loc[index, "category"] = "Employment"
        if df.loc[index, "report_name"] == "RSXFS":
            df.loc[index, "report_long_name"] = "Retail Sales"
            df.loc[index, "category"] = "Economy"
        if df.loc[index, "report_name"] == "TCU":
            df.loc[index, "report_long_name"] = "Capacity Utilization"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "UMCSENT":
            df.loc[index, "report_long_name"] = "Consumer Sentiment Index"
            df.loc[index, "category"] = "Economy"
        if df.loc[index, "report_name"] == "BUSINV":
            df.loc[index, "report_long_name"] = "Business Inventories"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "INDPRO":
            df.loc[index, "report_long_name"] = "Industrial Production Index"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG331S":
            df.loc[index, "report_long_name"] = "Primary Metal Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG332S":
            df.loc[index, "report_long_name"] = "Fabricated Metal Products Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG334S":
            df.loc[
                index, "report_long_name"
            ] = "Computer and Electronic Products Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG335S":
            df.loc[
                index, "report_long_name"
            ] = "Electrical Equipment, Appliance, and Component Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG3361T3S":
            df.loc[index, "report_long_name"] = "Motor Vehicles and Parts Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPMINE":
            df.loc[
                index, "report_long_name"
            ] = "Mining, Quarrying, and Oil and Gas Extraction Production"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "GACDFSA066MSFRBPHI":
            df.loc[index, "report_long_name"] = "Philidelphia Fed Manufacturing Index"
            df.loc[index, "category"] = "Manufacturing"
        if df.loc[index, "report_name"] == "GACDISA066MSFRBNY":
            df.loc[index, "report_long_name"] = "Empire State Manufacturing Index"
            df.loc[index, "category"] = "Manufacturing"
        if df.loc[index, "report_name"] == "BACTSAMFRBDAL":
            df.loc[index, "report_long_name"] = "Texas Fed Manufacturing Index"
            df.loc[index, "category"] = "Manufacturing"
        if df.loc[index, "report_name"] == "IR":
            df.loc[index, "report_long_name"] = "Import Price Index"
            df.loc[index, "category"] = "Economy"
        if df.loc[index, "report_name"] == "IQ":
            df.loc[index, "report_long_name"] = "Export Price Index"
            df.loc[index, "category"] = "Economy"
        if df.loc[index, "report_name"] == "PPIACO":
            df.loc[index, "report_long_name"] = "Producer Price Index (All)"
            df.loc[index, "category"] = "Inflation"
        if df.loc[index, "report_name"] == "PCUOMINOMIN":
            df.loc[index, "report_long_name"] = "Producer Price Index Mining"
            df.loc[index, "category"] = "Inflation"
        if df.loc[index, "report_name"] == "CPIAUCSL":
            df.loc[index, "report_long_name"] = "Consumer Price Index (All)"
            df.loc[index, "category"] = "Inflation"
        if df.loc[index, "report_name"] == "CPILFESL":
            df.loc[index, "report_long_name"] = "Consumer Price Index (Core)"
            df.loc[index, "category"] = "Inflation"
        if df.loc[index, "report_name"] == "MICH":
            df.loc[index, "report_long_name"] = "U of M: Inflation Expectation"
            df.loc[index, "category"] = "Inflation"
        if df.loc[index, "report_name"] == "AMDMUO":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturers Unfilled Orders: Durable Goods"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "AMTMUO":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturers Unfilled Orders: Total Manufacturing"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "ANXAUO":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturers Unfilled Orders: Nondefense Capital Goods Excluding Aircraft"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "AMVPUO":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturers Unfilled Orders: Motor Vehicles and Parts"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPB53122S":
            df.loc[
                index, "report_long_name"
            ] = "Industrial Production: Durable Goods Materials: Semiconductors, Printed Circuit Boards, and Other"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPG3254N":
            df.loc[
                index, "report_long_name"
            ] = "Industrial Production: Manufacturing: Non-Durable Goods: Pharmaceutical and Medicine"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPDMAN":
            df.loc[
                index, "report_long_name"
            ] = "Industrial Production: Durable Manufacturing"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "IPFINAL":
            df.loc[index, "report_long_name"] = "Industrial Production: Final Products"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "CSCICP03USM665S":
            df.loc[
                index, "report_long_name"
            ] = "Consumer Opinion Surveys: Confidence Indicators"
            df.loc[index, "category"] = "Economy"
        if df.loc[index, "report_name"] == "MNFCTRIRSA":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturers: Inventories to Sales Ratio"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "DGORDER":
            df.loc[index, "report_long_name"] = "Manufacturer New Orders: Durable Goods"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "NEWORDER":
            df.loc[
                index, "report_long_name"
            ] = "Manufacturer New Orders: Nondefense Capital Goods Excluding Aircraft"
            df.loc[index, "category"] = "Production"
        if df.loc[index, "report_name"] == "JTSQUL":
            df.loc[index, "report_long_name"] = "Job Quits: Total Nonfarm"
            df.loc[index, "category"] = "Employment"

    return df


# Functions to allow for easier filtering later
# These can be used indpendently as long as the get_fed_data function
# has been called.

# Each funcion maintains a consistent layout
# The dataframe is copied - pandas yells if we work off a slice
# The function occurs and the result is sorted and index is reset

# function to pull specific report
def get_report_from_fed_data(df1, report_name):
    df = df1.copy()
    df = df[df["report_name"] == report_name]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull a specific report_date
def get_report_date_from_fed_data(df1, report_date):
    df = df1.copy()
    df1 = df[df["report_date"] == report_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull reports after report_date
def get_report_after_date_fed_data(df1, report_date):
    df = df1.copy()
    df = df[df["report_date"] >= report_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull a specific release_date
def get_release_date_from_fed_data(df1, release_date):
    df = df1.copy()
    df = df[df["release_date"] == release_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull release_dates after a date
def get_release_after_date_fed_data(df1, release_date):
    df = df1.copy()
    df = df[df["release_date"] >= release_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# Setup a function for calculating rates of change
def period_change(df):
    df["period_change"] = df.report_data.pct_change()
    df["relative_change"] = 1 - df.iloc[0].report_data / df.report_data
    return df


# function to return a dataframe with only a single report with the latest
# data as updated
def get_latest_data(df1):
    df = df1.copy()
    df = df.sort_values("release_date").groupby("report_date").tail(1)
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull out data by larger category and normalize each report
# independently.  This assumes the master dataframe is passed in along
# with the report and a start_date.
def get_category_data_from_fed_data(df1, report_name, report_date):
    df = df1.copy()
    # we need to form a list of unique reports and their categories
    master_list = df["report_name"].unique()
    master_list = pd.DataFrame(master_list, columns=["report_name"])
    master_list = add_report_long_names(master_list)
    # Grab only the reports based on the report_name from the list
    filtered_list = master_list[master_list["report_name"] == report_name]
    filtered_list = master_list[
        master_list["category"] == filtered_list.category.iloc[0]
    ]

    df_out = pd.DataFrame()
    for index, row in filtered_list.iterrows():
        temp_df = get_report_from_fed_data(df, row.report_name)
        temp_df = get_report_after_date_fed_data(temp_df, report_date)
        temp_df = get_latest_data(temp_df)
        temp_df = period_change(temp_df)
        temp_df = add_report_long_names(temp_df)
        df_out = df_out.append(
            temp_df,
            ignore_index=True,
        )

    df_out["period_change"] = df_out["period_change"].fillna(0)

    return df_out


#############################################################################
# Charts
#############################################################################
# Basic chart for direct values
# Assumes report is pre-filtered so dataset only has one report - see callback
def basic_chart(df, long_name):
    # Add some color to the various release dates
    # Since the marker_color needs an array of ints, we do a conversion to
    # seconds since the epoch
    df["release_int"] = (df.release_date - pd.Timestamp("1970-01-01")) // pd.Timedelta(
        "1s"
    )

    fig = px.scatter(
        df,
        x="report_date",
        y="report_data",
        trendline="lowess",
        color="release_int",
        color_continuous_scale=px.colors.sequential.YlOrRd_r,
        hover_name="report_long_name",
        hover_data={
            "release_int": False,
            "release_date": "| %b %d, %Y",
            "category": True,
        },
    )

    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + " Raw Data"),
        xaxis_title="",
        yaxis_title="",
        coloraxis_colorbar=dict(
            title="Release Date<br> -",
            thicknessmode="pixels",
            thickness=50,
            tickmode="array",
            tickvals=df.release_int,
            ticktext=df.release_date.dt.strftime("%m/%d/%Y"),
            ticks="inside",
        ),
    )
    # fig.show()
    return fig


# Chart for displaying change since the baseline
# We need a dataframe with only one distinct report_date per period
# filter for only the latest release_date
def baseline_change_chart(df, long_name):
    fig = go.Figure(layout=lc.layout)
    fig.add_traces(
        go.Scatter(
            x=df.report_date,
            y=df.relative_change,
            name="Baseline",
            line_width=2,
            fill="tozeroy",
        )
    )

    fig.add_hline(y=0, line_color="white")
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + " Change from Baseline"),
        xaxis_title="",
        yaxis_title="",
    )
    # fig.show()
    return fig


# Chart for displaying change since the last value
# Same as above chart
def periodic_change_chart(df, long_name):
    fig = go.Figure(layout=lc.layout)
    fig.add_traces(
        go.Scatter(
            x=df.report_date,
            y=df.period_change,
            name="Relative",
            line_width=2,
            fill="tozeroy",
        )
    )

    fig.add_hline(y=0, line_color="white")
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + " Change from Prior Period"),
        xaxis_title="",
        yaxis_title="",
    )
    # fig.show()
    return fig


# Chart of category changes period-to-period
def category_chart_perodic(df1, report_name, report_date):
    # Start with the data
    df = get_category_data_from_fed_data(df1, report_name, report_date)

    # Dynamically build out the chart from the dataframe
    # The official docs don't show this, but it works.
    x_data = df["report_date"].unique()
    y_data = df["report_long_name"].unique()
    z_data = []
    for i in y_data:
        z_data.append(df[df["report_long_name"] == i]["period_change"] * 100)

    fig = go.Figure(
        go.Surface(
            contours={
                "z": {
                    "show": True,
                    "start": -0.01,
                    "end": 0.01,
                    "size": 0.05,
                    "width": 1,
                    "color": "black",
                },
            },
            x=x_data,
            y=y_data,
            z=z_data,
        )
    )

    # Title Formatting
    category = df.category.iloc[0]
    begin_date = np.datetime_as_string(x_data.min(), unit="D")
    end_date = np.datetime_as_string(x_data.max(), unit="D")

    fig.update_layout(
        title=category
        + " Report Prior Period Comparison (% Change): <br>"
        + begin_date
        + " - "
        + end_date,
        scene={
            "xaxis_title": "",
            "yaxis_title": "",
            "zaxis_title": "",
            "camera_eye": {"x": 1, "y": -1, "z": 0.75},
            "aspectratio": {"x": 0.75, "y": 0.75, "z": 0.5},
        },
        margin=dict(
            b=10,
            l=10,
            r=10,
        ),
    )
    # fig.show()
    return fig


# Chart of category changes period-to-period - see above
def category_chart_baseline(df1, report_name, report_date):
    df = get_category_data_from_fed_data(df1, report_name, report_date)

    x_data = df["report_date"].unique()
    y_data = df["report_long_name"].unique()
    z_data = []
    for i in y_data:
        z_data.append(df[df["report_long_name"] == i]["relative_change"] * 100)

    fig = go.Figure(
        go.Surface(
            contours={
                "z": {
                    "show": True,
                    "start": -0.01,
                    "end": 0.01,
                    "size": 0.05,
                    "width": 1,
                    "color": "black",
                },
            },
            x=x_data,
            y=y_data,
            z=z_data,
        )
    )

    category = df.category.iloc[0]
    begin_date = np.datetime_as_string(x_data.min(), unit="D")
    end_date = np.datetime_as_string(x_data.max(), unit="D")

    fig.update_layout(
        title=category
        + " Report Baseline Comparison (% Change): <br>"
        + begin_date
        + " - "
        + end_date,
        scene={
            "xaxis_title": "",
            "yaxis_title": "",
            "zaxis_title": "",
            "camera_eye": {"x": 1, "y": -1, "z": 0.75},
            "aspectratio": {"x": 0.75, "y": 0.75, "z": 0.5},
        },
        margin=dict(
            b=10,
            l=10,
            r=10,
        ),
    )
    # fig.show()
    return fig


#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("Support Functions has nothing to run directly")
