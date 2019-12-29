"#! InundationAnalysisScraper"

This program scrapes data the NOAA Inundation Analysis web application. It uses selenium to automate the inputs, then saves the data in a dictionary. It writes the data to a text file when finished. Written in python 3.7.4

Installation
1. Install python library dependencies: pip install -r requirements.txt
   Or just pip install selenium. This was written with selenium version 3.141.0

2. Requires Google Chrome and appropriate version of Chromedriver.
   https://chromedriver.chromium.org/

3.  Create an environment variable to chromedriver's path.
    https://selenium.dev/documentation/en/webdriver/driver_requirements/#adding-executables-to-your-path

--TODO--
- Add exception handling.
- Needs a better way to manage the returned data.
- Run selenium in the background. 
- Work on text displayed in terminal while loading the web pages( create a working loading bar...)

