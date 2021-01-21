from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from datetime import datetime
from time import sleep
from csv import reader
from csv import writer

''' THIS SECTION GETS THE VEHICLE REGS '''

#sets the url to be loaded
url = "https://app.ibexres.com/legacy/accomreports/ac_GuestNightStat.php"

#sets the options for the selenium Chrome driver
options = webdriver.ChromeOptions() 
#sets chrome driver to use the default chrome profile - which is logged in to ibex.
options.add_argument("user-data-dir=Users/admin/Library/Application Support/Google/Chrome/Default") #Path to your chrome profile

#sets up the chome driver.
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

#calls the url
driver.get(url)

#waits until it detects that the iframe has been loaded. 
wait = WebDriverWait(driver, 20)
print("Guest nights report is loading...")
wait.until((EC.presence_of_element_located((By.ID, "theFrame"))))

#switches the target of the driver to the iframe.
frame = driver.find_element_by_name('theFrame')
driver.switch_to.frame(frame)


#waits until the date selection form fields have loaded. 
wait.until((EC.presence_of_element_located((By.NAME, "button_search"))))

#initialize a list of dicts - one for each month where the days can be paired with the capacity.
dateslist = {}

select = Select(driver.find_element_by_name("pid_sel"))
select.select_by_value("9717")

for i in range(1, 13, 1):

    #selects the start of each month from the dropdown form and submits
    select = Select(driver.find_element_by_name("dst"))
    select.select_by_value("1")
    select = Select(driver.find_element_by_name("mst"))
    select.select_by_value(str(i))
    select = Select(driver.find_element_by_name("yst"))
    select.select_by_value("2021")

    driver.find_element_by_name("button_search").click()
    
    #sleep delay allows the new results to begin loading
    sleep(3)

    try:
        #waits until the results table has loaded. 
        wait.until((EC.presence_of_element_located((By.XPATH,"//*[text()='Totals:']"))))

        #get the value date and capacity fields - NOTE THIS IS WHERE IT'S LIKELY TO FALL OVER IF THE LAYOUT OF THE TABLE CHANGES.
        dates = driver.find_elements_by_xpath("//*[@id='AutoNumber2']/tbody/tr[6]/td/table/tbody/tr/td[1]")
        capacities = driver.find_elements_by_xpath("//*[@id='AutoNumber2']/tbody/tr[6]/td/table/tbody/tr/td[9]")

        #enter the date/capacity pair into the correct dict.
        for x in range(0, len(dates)-1, 1):
            dateslist[dates[x].text] = capacities[x-1].text
    
    except:
        pass

#close the selenium chrome driver
driver.close()

#initialise a new dict to hold a cleaned version of the scrapped data.
cleaneddict = {}

#check the length of the key to ensure it is 11 chars long e.g. '01-Jan-2021' and copy k, v pair to cleaned dict
for k, v in dateslist.items():
        if len(k) == 11:
            cleaneddict[k] = v


#open the stopsell.csv file and copy to lines list
lines = []
with open('stopsell.csv', 'r') as csvfile:
    reader = reader(csvfile)
    for row in reader:
        lines.append(row)

#complete one pass of cleaneddict to check status of each day and sort into categories
#initialise dicts to hold the categories
nearingcapacity = {}
overcapacity = {}
movedtoundercapacity = {}
alreadystopped = {}

for k, v in cleaneddict.items():

    if int(v) < 101:
        for line in lines:
            for field in line:
                if k in field:
                    movedtoundercapacity[k] = v
    
    if int(v) > 30 and int(v) <= 100:
        nearingcapacity[k] = v
    
    if int(v) > 100:
        for line in lines:
            if k in line:
                alreadystopped[k] = v
            else:
                overcapacity[k] = v

#print report from pass.           
print("\n")

print("******************")

print("\n")

print("The following dates are nearing capacity:")
for k, v in nearingcapacity.items():
    print(k, v)

print("\n")

print("It is understood that a stop-sell has been implemented for the following dates on a previous pass:")
for k, v in alreadystopped.items():
    print(k, v)

print("\n")

print("The following dates have dropped below capacity and need stop sell released:")
for k, v in movedtoundercapacity.items():
    print(k, v)

print("\n")

print("A stop-sell should be implemented on the following dates:")
for k, v in overcapacity.items():
    print(k, v)

print("\n")

print("******************")

print("\n")
