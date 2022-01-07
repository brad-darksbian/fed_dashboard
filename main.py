import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date
import business_logic as bl
import layout_configs as lc
import support_functions as sf

#############################################################################
# Style modifications
#############################################################################
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
}

TEXT_STYLE = {"textAlign": "center"}

DROPDOWN_STYLE = {"textAlign": "left"}

#############################################################################
# Content
#############################################################################
# Create drop-down selector and initial date picker
report_select = dbc.Row(
    [
        dbc.Col(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="report",
                            options=[
                                {
                                    "label": label,
                                    "value": value,
                                }
                                for value, label in bl.fed_list_abbrev.items()
                            ],
                            # default report to populate
                            value="CPIAUCSL",
                        ),
                    ],
                    className="dash-bootstrap",
                ),
            ],
            md=6,
        ),
        dbc.Col(
            [
                html.Div(
                    [
                        dcc.DatePickerSingle(
                            id="start-date",
                            min_date_allowed=date(2008, 1, 1),
                            initial_visible_month=date(2020, 1, 1),
                            date=date(2020, 1, 1),
                        ),
                    ],
                    className="dash-bootstrap",
                )
            ],
            md=2,
        ),
    ]
)

# Info Bar
info_bar = html.Div(
    id="summary",
)

# Container for raw data charts
basic_data = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="basic-chart",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

# Container for periodic charts
baseline_data = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="change-from-baseline-chart",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="change-from-period-chart",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

# Container for category survey charts
category_data = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="category-baseline-chart",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="category-period-chart",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

####################################################
# Layout Creation Section
####################################################
main_page = html.Div(
    [
        html.Hr(),
        html.H4("Federal Reserve Economic Data Analysis", style=TEXT_STYLE),
        html.Hr(),
        report_select,
        html.Hr(),
        info_bar,
        html.Hr(),
        basic_data,
        html.Hr(),
        baseline_data,
        html.Hr(),
        html.H5("Comparison of Data in Broad Category", style=TEXT_STYLE),
        html.Hr(),
        category_data,
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)

#############################################################################
# Application parameters
#############################################################################
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
)
app.config.suppress_callback_exceptions = True
app.title = "Federal Reserve Data Analysis"
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Multi-page selector callback - not really used, but left in for future use
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    # Left in because I'm not sure if this will be a muli-page app at some point

    # if pathname == "/market-sentiment":
    #     return volumes
    # else:
    return main_page


####################################################
#  Callbacks - Modals
####################################################


####################################################
#  Callbacks - charts
####################################################
# Basic Chart with raw report data
@app.callback(
    dash.dependencies.Output("basic-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def basic_report(report, init_date):
    # set the date from the picker
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    # Filter to the report level
    df = sf.get_report_from_fed_data(bl.fed_df, report)
    df1 = sf.get_report_after_date_fed_data(df, date_string)
    # Filter again to the release
    df2 = sf.get_release_after_date_fed_data(df1, date_string)

    # Assign long names
    df2 = sf.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]

    fig = sf.basic_chart(df2, long_name)
    return fig


# Baseline Chart - sets change relative to the baseline date
@app.callback(
    dash.dependencies.Output("change-from-baseline-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def change_from_baseline_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    df = sf.get_report_from_fed_data(bl.fed_df, report)
    # Hook function for slider or other date range finder
    df1 = sf.get_report_after_date_fed_data(df, date_string)
    df2 = sf.get_latest_data(df1)
    df2 = sf.period_change(df2)
    df2 = sf.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]
    fig = sf.baseline_change_chart(df2, long_name)

    return fig


# Period Chart - sets change relative to the previous period
@app.callback(
    dash.dependencies.Output("change-from-period-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def change_from_period_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    # This is effecitvely the baseline function just updated to call the other
    # chart for period
    df = sf.get_report_from_fed_data(bl.fed_df, report)
    df1 = sf.get_report_after_date_fed_data(df, date_string)
    df2 = sf.get_latest_data(df1)
    df2 = sf.period_change(df2)
    df2 = sf.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]

    fig = sf.periodic_change_chart(df2, long_name)
    return fig


# Category Data Comparison to survery larger economic landscape
# Period Chart
@app.callback(
    dash.dependencies.Output("category-period-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def category_period_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    # we need a few things since logic is handled in the helper function
    # The master dataframe
    # The selected report
    # The starting date
    fig = sf.category_chart_perodic(bl.fed_df, report, date_string)

    return fig


# Period Chart
@app.callback(
    dash.dependencies.Output("category-baseline-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def category_baseline_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    fig = sf.category_chart_baseline(bl.fed_df, report, date_string)

    return fig


###################################################
# Summary Block
###################################################
@app.callback(
    dash.dependencies.Output("summary", "children"),
    [dash.dependencies.Input("report", "value")],
)
def dashboard_summary_numbers(report):
    # Grab some values from the most recent DA datafame
    df1 = sf.get_report_from_fed_data(bl.fed_df, report)

    # I only care about the most recent row so pull it
    #  It makes reference easier further down.
    df2 = df1.iloc[-1:]

    # Return the entire structured block
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Latest Date: "),
                            html.H6(df2.report_date.dt.strftime("%m/%d/%Y")),
                        ],
                        color="light",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Latest Release: "),
                            html.H6(df2.release_date.dt.strftime("%m/%d/%Y")),
                        ],
                        color="success",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Most Recent Data: "),
                            html.H6(df2.report_data),
                        ],
                        color="primary",
                    ),
                    md=2,
                ),
            ]
        )
    )


###################################################
# Server Run
###################################################
if __name__ == "__main__":
    # This line works for linux / OSX. Change debug to True to turn on debugging
    app.run_server(debug=False, host="0.0.0.0", port=8050, dev_tools_hot_reload=True)
    # Windows seems to dislike running with the host set to 0.0.0.0
    # app.run_server(
    #   debug=False,
    #   port=8050,
    #   dev_tools_hot_reload=True
    #   )
