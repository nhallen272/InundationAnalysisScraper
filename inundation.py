#! Inundation Analysis Scraper 
# scrapes inundation analysis data from noaa
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time
import json

class InundationQuery:
    """Type to hold user-entered query for the inundation analysis tool."""
    def __init__(self):
        self.ask_date('from')
        self.ask_date('to')
        self.elevation = input("Enter an elevation: ")
        self.dates = {'beginMonth': self.from_month, 'beginDay': self.from_day, 'beginYear': self.from_year, 
                      'endMonth': self.end_month, 'endDay': self.end_day, 'endYear': self.end_year}

    def ask_date(self, to_from):
        if to_from == 'from':
            raw_date = input("Enter start date(mm/dd/yyyy): ").split("/")
            # dropdown lists are indexed starting at 0.
            self.from_month = str(int(raw_date[0])-1) # convert back to string
            self.from_day = str(int(raw_date[1])-1)
            self.from_year = raw_date[2]

        elif to_from == 'to':
            raw_date = input("Enter end date(mm/dd/yyyy): ").split("/")
            # dropdown lists are indexed starting at 0.
            self.end_month = str(int(raw_date[0])-1) # convert back to string
            self.end_day = str(int(raw_date[1])-1)
            self.end_year = raw_date[2]

        

    
    def get_elevation(self):
        return self.elevation

class InundationAnalysis(webdriver.Chrome):
    def __init__(self, base_url ):
        super().__init__() # initialize the webdriver

        self.get(base_url)
        self.query = InundationQuery()
    
    def wait_page(self, css_selector, message, endmessage):
        loadbar = CheckPresenceofElement(self, css_selector, message, endmessage)


    def input_dropdown_date(self, css_selector, mdy):
        try:
            input_element = self.find_element_by_css_selector(css_selector)

        except:
            print("Error")   
        finally:
            options = input_element.find_elements_by_tag_name("option")
            for option in options:
                if option.get_attribute("value") == self.query.dates[mdy]:
                    option.click()
    
    def box_input(self, css_selector, input_value):
        if input_value == 'beginYear' or input_value == 'endYear':
                isYear = True
        else:
            isYear = False

        if input_value in self.query.dates:
            input_value = self.query.dates[input_value]

        try:
            binput = self.find_element_by_css_selector(css_selector)
        finally:
            binput.click()
            if isYear:
                for i in range(4):
                    binput.send_keys(Keys.BACK_SPACE)
                    binput.send_keys(input_value)
                    
            else:
                binput.send_keys(input_value)
            

    def submit(self, css_selector):
        try:
            submit_btn = self.find_element_by_css_selector(css_selector)
            submit_btn.click()
        except:
            print("Error\n")
    
    def get_table_data(self, css_selector, tag):
        table_body = self.find_element_by_css_selector(css_selector)
        data_rows = table_body.find_elements_by_tag_name(tag)
        self.data = []
        for i in range(1, len(data_rows)):
            data_row = data_rows[i].find_elements_by_tag_name('td')
            data_set = {'period_start':data_row[0].text.strip(), 
                    'period_end':data_row[1].text.strip(), 
                    'time_high_tide':data_row[2].text.strip(), 
                    'elevation_above_datum':float(data_row[3].text.strip()),
                    'tide_type':data_row[4].text.strip(),
                    'duration':float(data_row[5].text.strip()) }

            self.data.append(data_set)
    
    def get_data(self):
        return self.data

#TODO
#class InundationData(): 
  #  """Command line user interface to handle returned data."""
  
        
    



class CheckPresenceofElement:
    def __init__(self, driver, css_selector, message, endmessage):
        self.wait(css_selector, message, endmessage)
        
    def wait(self, css_selector, message, endmessage):
        
        start_time = time.time()
        x = 1
        while time.time() - start_time < 30:
            dots = "." * x
            print("{}\r".format(message + dots))
            time.sleep(0.5)
            #sys.stdout.write("\033[K")
            if EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)):
                self.found = True
                break
        print(endmessage+"\n")


# -----Functions-----

def input_dropdown_date(input_element, date):
    options = input_element.find_elements_by_tag_name("option")
    for option in options:
        if option.get_attribute("value") == date:
            option.click()


def main():
    # -----get query from user-----
    # ex. wrightsville beach station id=8658163
    station_id = input("Enter station ID: ")
    base_url = "https://tidesandcurrents.noaa.gov/inundation/AnalysisParams?id={0}".format(station_id)
    
    # -----setup selenium-----
    maindriver = InundationAnalysis(base_url)

    # if (EC.presence_of_element_located.
    try:

        maindriver.wait_page('#paramform > table.table > tbody > tr:nth-child(9) > td > input[type=text]', "Loading page", "Success")
       
    finally:
        
        # -----find the elevation input-----
        maindriver.box_input('#paramform > table.table > tbody > tr:nth-child(9) > td > input[type=text]', maindriver.query.get_elevation())
        #elevation_input = driver.find_element_by_css_selector('#paramform > table.table > tbody > tr:nth-child(9) > td > input[type=text]')    # input the elevation
        #elevation_input.click()
        #elevation_input.send_keys(query.get_elevation())

        # -----find & input dates-----
        
        maindriver.input_dropdown_date('#beginDate_Month_ID', 'beginMonth')
        #from_month_input = driver.find_element_by_css_selector('#beginDate_Month_ID')
        maindriver.input_dropdown_date('#beginDate_Day_ID', 'beginDay')
        #from_day_input = driver.find_element_by_css_selector('#beginDate_Day_ID')
        #from_year_input = driver.find_element_by_css_selector('#beginDate_Year_ID')
        maindriver.box_input('#beginDate_Year_ID', 'beginYear')

        maindriver.input_dropdown_date('#endDate_Month_ID', 'endMonth')
        #end_month_input = driver.find_element_by_css_selector('#endDate_Month_ID')
        maindriver.input_dropdown_date('#endDate_Day_ID', 'endDay')

        #end_day_input = driver.find_element_by_css_selector('#endDate_Day_ID')
        maindriver.box_input('#endDate_Year_ID', 'endYear')
        #end_year_input = driver.find_element_by_css_selector('#endDate_Year_ID')
        
            
        # submit the form
        maindriver.submit('#paramform > input[type=submit]:nth-child(31)')
        

    try:
        maindriver.wait_page('body > div.container-fluid.custom-padding > div > div > div.span9 > table > tbody > tr:nth-child(11) > td > table > tbody', "Loading Results", "Page Loaded")
        
    finally:
        # save the table into memory as a lsit of dicts
        maindriver.get_table_data('body > div.container-fluid.custom-padding > div > div > div.span9 > table > tbody > tr:nth-child(11) > td > table > tbody', 'tr')
        data = maindriver.get_data()
        #data_analysis = InundationData(maindriver.get_data  )  need to add some way to deal with the data better

        maindriver.close()

    # write data to a txt file
    
    with open("inundation_data.txt", 'w') as datfile:
        datfile.write("period_start\t period_end\t time_high_tide\t elevation_above_datum\t tide_type\t duration")
        datfile.write("\n")
        for dataset in data:
            datfile.write(json.dumps(dataset))
            datfile.write('\n')

        datfile.close()

main()
    

            


    


    
