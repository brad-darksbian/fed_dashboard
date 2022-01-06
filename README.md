# fed-dashboard
A simple dashboard to view federal economic data.

This system uses the included CSV file of federal economic data to populate the dashboard.  Live data is available for anyone interested, but it does require registering for an API key from the St. Louis Fed system.  In my live system for analysis, I obtain the data regularly and load it into a database where the data is read.  For this example, I pulled an abbreviated dump of the table beginning 1/1/2008 through 12/31/2021.  That gives quite a bit of data to play with.

I regualrly use this for my own analytics work so the repository will update as needs change.  However, I am treating this mostly as a teaching tool, so I will endeavor to keep the code clean and approachable by any skill level.

Within the code, you will find a number of examples of various plotly chart types with ways to lay them out and call them.  Addtionally, there are several examples of Dash configuration such as various call backs and other elements that provide decent examples into the system.  Some of the examples include:

 - Basic construction of a Dash application
 - Bootstrap components
 - Drop Down lists
 - Date Selectors
 - 3D Plots
 - Line charts
 - Scatter charts with regression
 - Layout configurations
 - Call backs for dynamic updates
 - Data Processing
 - Processing files in a dataframe

This system goes through a bit of data processing from various angles to construct the charts.

This is a python project using Dash and plotly to contextualize federal economic data retreived from the FRED system.

To use:

1. Download the files in the repository to a directory.
2. In the support_functions.py file, ensure your paths are correct.

**NOTE** - I developed this on a Mac and run it on a Linux machine.  Files are set to reside in a subdirectory "data" under the main folder.

3. Review the requirements.txt and make sure all libraries are installed.  These are relatively minimal and easily obtained.
4. Run the main.py file using 'python /path/to/directory/main.py'
5. Navigate your browser to the ip address of the machine (perhaps 127.0.0.1 or other if installed remotely) on port 8050.
6. Enjoy!

Use the code how you please.  If you use it as a basis for your own project, be cool and give me a shout out.

Any questions, comments, or concerns - create an issue or just shoot me an email brad@darksbian.com

Brad

Note: Some users have pointed out that when running this code on OSX, you can sometimes get an error like "[SSL: CERTIFICATE_VERIFY_FAILED]".

This error might pop up in relation to running the pull_fed_data.py script once set up with an API key.

This is a known issue with python >=3.6 and OSX.  The fix is simple and outlined here:  https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error