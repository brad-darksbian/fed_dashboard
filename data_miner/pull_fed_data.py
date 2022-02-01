"""
  This is a basic data downloader to obtain report data from the federal
  reserve's FRED system.

  The full_fred module does the heavy lifting.
  Read up on it at https://github.com/7astro7/full_fred

  Follow the instructions:
   - pip install full-fred
   - set up your api key file
   - set the full path the api key file
   - set up the output path
   - Boom! Bob's your uncle (i.e., you're good to go)
"""

import pandas as pd
import numpy as np
from full_fred.fred import Fred

output_file = "../data/fed_dump.csv"

# path to the api key file
# this is just a bare text file that only contains the api key
fred = Fred("fed_api_key.txt")

# list of reports to obtain
report_list = [
    "WM1NS",  # M1 Supply
    "WM2NS",  # M2 Supply
    "ICSA",  # Unemployment
    "CCSA",  # Continued Unemployment
    "JTSJOL",  # Job Openings: Total Nonfarm
    "JTSQUL",  # Job Quits: Total Nonfarm
    "PAYEMS",  # Non-Farm Employment
    "NPPTTL",  # Total Nonfarm Private Payroll Employment (ADP)
    "RSXFS",  # Retail Sales
    "TCU",  # Capacity Utilization
    "UMCSENT",  # Consumer Sentiment Index
    "BUSINV",  # Business Inventories
    "INDPRO",  # Industrial Production Index
    "IPG331S",  # Primary Metal Production
    "IPG332S",  # Fabricated Metal Products
    "IPG334S",  # Computer and Electronic Products
    "IPG335S",  # Electrical Equipment, Appliance, and Component
    "IPG3361T3S",  # Motor Vehicles and Parts
    "IPMINE",  # Mining, Quarrying, and Oil and Gas Extraction
    "GACDFSA066MSFRBPHI",  # Philidelphia Fed Manufacturing Index
    "GACDISA066MSFRBNY",  # Empire State Manufacturing Index
    "IR",  # Import Price Index
    "IQ",  # Export Price Index
    "PPIACO",  # Producer Price Index - all
    "PCUOMINOMIN",  # Producer Price Index Mining
    "CPIAUCSL",  # Consumer Price Index - all
    "CPILFESL",  # Consumer Price Index (Core)
    "MICH",  # University of Michigan: Inflation Expectation
    "AMDMUO",  # Manufacturers Unfilled Orders: Durable Goods
    "AMTMUO",  # Manufacturers Unfilled Orders: Total Manufacturing
    "ANXAUO",  # Manufacturers Unfilled Orders: Nondefense Capital Goods Excluding Aircraft
    "AMVPUO",  # Manufacturers Unfilled Orders: Motor Vehicles and Parts
    "BACTSAMFRBDAL",  # Current General Business Activity; Diffusion Index for Texas
    "IPB53122S",  # Industrial Production: Durable Goods Materials: Semiconductors, Printed Circuit Boards, and Other
    "IPG3254N",  # Industrial Production: Manufacturing: Non-Durable Goods: Pharmaceutical and Medicine
    "IPDMAN",  # Industrial Production: Durable Manufacturing
    "IPFINAL",  # Industrial Production: Final Products
    "CSCICP03USM665S",  # Consumer Opinion Surveys: Confidence Indicators: Composite Indicators: OECD Indicator for the United States
    "MNFCTRIRSA",  # Manufacturers: Inventories to Sales Ratio
    "DGORDER",  # Manufacturers' New Orders: Durable Goods
    "NEWORDER",  # Manufacturers' New Orders: Nondefense Capital Goods Excluding Aircraft
]

# Logic to get the reports and process for ingestion
def get_report(report_name):
    try:
        df = fred.get_series_df(report_name, realtime_start="2000-01-01")
        df.rename(
            columns={
                "realtime_start": "release_date",
                "value": "data",
                "date": "report_date",
                "report": "report_name",
            },
            inplace=True,
        )
        df = df.drop(columns="realtime_end")
        df["report_name"] = report_name
    except:
        df = pd.DataFrame(
            columns=["release_date", "report_date", "data", "report_name"]
        )
        print(report_name + " Empty Set")
    return df


# Pull all the reports into a big honking dataframe
all_rep = []
for i in report_list:
    df1 = get_report(i)
    all_rep.append(df1)

df = pd.concat(all_rep)
df["hash"] = df.apply(lambda x: hash(tuple(x)), axis=1)
# Make sure all data is numeric
df.data = pd.to_numeric(df.data, errors="coerce").fillna(0).astype("float")

# output to file
df.to_csv(output_file, index=False)
