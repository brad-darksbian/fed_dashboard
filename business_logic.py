"""
    is ready to be called by the main app upon init.

    This is called by main.py and in turn calls support functions when needed

"""
import pandas as pd
import numpy as np
import plotly.io as pio
import support_functions as sf

pd.options.plotting.backend = "plotly"
pio.templates.default = "plotly_dark"

# Get data from CSV or other store and hold a master dataframe
fed_df = sf.get_fed_data()

#############################################################################
# Generate the report list
#############################################################################
# Populate a dataframe for the selctor
fed_list = fed_df["report_name"].unique()
fed_list = np.sort(fed_list)

fed_list = pd.DataFrame(fed_list, columns=["report_name"])
fed_list = sf.add_report_long_names(fed_list)
fed_list.sort_values(by=["report_long_name"], inplace=True)

# setup for drop down use
fed_list_abbrev = dict(zip(fed_list["report_name"], fed_list["report_long_name"]))


#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("business logic should not be run like this")
