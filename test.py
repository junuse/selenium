from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import time
import json

def process_person( person, fref ):

    print ("processing:", person['name'])

    if ( len(person['idcard']) == 20 ):
        elem = browser.find_element_by_id("input_name") # Find the query box
        elem.clear()
        elem.send_keys(person['name'])

        elem = browser.find_element_by_id("input_number") # Find the query box
        elem.clear()
        elem.send_keys(person['idcard'])
        time.sleep(0.1)
        browser.find_element_by_id("login_sub").click()

        try:
            #browser.switch_to.frame("content")
            browser.find_element_by_id("checkad2")
            #print (person['name'], "matched!")
            person['result'] = 'matched'
            person['note'] = browser.find_element_by_id("checkad2").text
        except NoSuchElementException:
            #print (person['name'], "not match!")
            person['result'] = 'not_matched'
            person['note'] = browser.find_element_by_id("checkad1").text
    else:
        person['result'] = 'bad_format'
        person['note'] = 'id card length wrong(' + str(len(person['idcard'])) + ')!'

    fref.write(json.dumps(person, ensure_ascii=False))
    fref.write("\n")
    browser.back()

def get_test_persons():
    return [
            {'name':"孙",   'idcard':"310xxxxxxxxxxB2"},
           ]

def get_persons():
    return [
            {'name':"孙",   'idcard':"310xxxxxxxxxxB2"}
           ]

def count_result( persons, result ):
    count = 0
    for person in persons:
        if ( person['result'] == result ):
            count = count + 1 
    return count

# open driver
print ("now start brower")
browser = webdriver.Firefox() # Get local session of firefox
print ("now get page")
browser.get("http://www./2dzcx") # Load page

time.sleep(5) # Let the page load, will be added to the API
#sreach_window=browser.current_window_handle

#xf = browser.find_element_by_xpath("//iframe[contains(@id,'content')]");
#print (xf)

browser.switch_to.frame("content")
print ("switched to content")


#persons = get_test_persons()
persons = get_persons()

fref = open('test_result.txt','w')
for index in range(len(persons)):
    print( "index:", index)
    process_person( persons[index], fref )

print( persons )
print( "totally ", len(persons), "persons" )

browser.close()

#output to file
'''for person in persons:
    fref.write(json.dumps(person, ensure_ascii=False))
    fref.write("\n")'''
fref.write("========================\n")
fref.write("totally:" + str(len(persons)) + "\n" )
fref.write("matched:" + str(count_result(persons, 'matched')) +  "\n" )
fref.write("not matched:" + str(count_result(persons, 'not_matched')) + "\n")
fref.write("bad format:" + str(count_result(persons, 'bad_format')) )
fref.close()



