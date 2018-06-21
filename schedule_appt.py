import os.path
import string
from splinter import Browser
from datetime import datetime

executable_path = {'executable_path':'/usr/local/bin/chromedriver'}

def compare(string1, string2):
    remove = string.whitespace
    return string1.translate(None, remove) == string2.translate(None, remove)

with Browser("chrome", **executable_path) as browser:
    # visit url
    url = "https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit&localeName=en"
    browser.visit(url)
    browser.cookies.delete()
    apptfiledir = os.path.abspath(os.path.dirname(__file__)) #This would give the absolute path to the directory in which your script exists.
    apptfile = os.path.join(apptfiledir,'appt.txt')

    # constants
    # list of dmv offices are found in dmvlist.txt
    default_office = "503"
    task_numbers = ["1", "2", "3"]
    reasons_for_visit = ["taskRID", "taskCID", "taskVR"]
    first_name = "First"
    last_name = "Last"
    tel_area = "XXX"
    tel_prefix = "XXX"
    tel_suffix = "XXXX"
    email = "something@gmail.com"
    # Make sure you have a future date set in the appt.txt file
    current_appt_time = None
    with open(apptfile, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        current_appt_time = data
        print(data)

    # select dmv office
    dmv_office = browser.find_by_id("officeId").first
    dmv_office.select(default_office)

    # select amount of items to process
    browser.choose("numberItems", task_numbers[0])

    # select reason for your visit
    browser.check(reasons_for_visit[0])

    # fill out personal info
    browser.find_by_name("firstName").fill(first_name)
    browser.find_by_name("lastName").fill(last_name)
    browser.find_by_name("telArea").fill(tel_area)
    browser.find_by_name("telPrefix").fill(tel_prefix)
    browser.find_by_name("telSuffix").fill(tel_suffix)

    # continue to appointment page
    browser.find_by_value("Continue").click()

    if browser.is_element_present_by_id('formId_1', 20):
        appt_xpath = '//div[@class="r-table col-xs-12"]'
        appt_table = browser.find_by_xpath(appt_xpath).first.text
        print appt_table
        appt_time_str = appt_table.split('\n')[5]
        current_appt_datetime = datetime.strptime(current_appt_time, '%A, %B %d, %Y at %I:%M %p')
        new_appt_datetime_object = datetime.strptime(appt_time_str, '%A, %B %d, %Y at %I:%M %p')
        is_new_appttime_earlier = new_appt_datetime_object < current_appt_datetime
        if is_new_appttime_earlier:
            continue_xpath = "//a[contains(text(), 'Continue')]"
            browser.find_by_xpath(continue_xpath).click()
            # if you already have a prior appt it goes here to confirm
            if browser.is_element_present_by_id("keepApptDate", 20):
                print browser.find_by_value("Confirm New Appointment")
                browser.find_by_value("Confirm New Appointment").click()
                if browser.is_element_present_by_value("Continue", 20):
                    browser.choose("notificationMethod", "EMAIL")
                    browser.find_by_name("notify_email").fill(email)
                    browser.find_by_name("notify_email_confirm").fill(email)
                    browser.find_by_value("Continue").click()
                    if browser.is_element_present_by_value("Confirm", 20):
                        browser.find_by_value("Confirm").click()
                        file = open(apptfile, 'w')
                        file.write(appt_time_str)
                        file.close()
                        print("Successfully booked your new appointment at {}".format(appt_time_str))
                        quit()
            if browser.is_element_present_by_name('ApptForm', 20):
                # if you don't have a prior appt it goes here to confirm
                browser.choose("notificationMethod", "SMS")
                browser.find_by_name("notify_smsTelArea").fill(tel_area)
                browser.find_by_name("notify_smsTelPrefix").fill(tel_prefix)
                browser.find_by_name("notify_smsTelSuffix").fill(tel_suffix)
                browser.find_by_name("notify_smsTelArea_confirm").fill(tel_area)
                browser.find_by_name("notify_smsTelPrefix_confirm").fill(tel_prefix)
                browser.find_by_name("notify_smsTelSuffix_confirm").fill(tel_suffix)
                browser.find_by_value("Continue").click()

                if browser.is_element_present_by_value("Confirm", 20):
                    browser.find_by_value("Confirm").click()
                    file = open(apptfile, 'w')
                    file.write(appt_time_str)
                    file.close()
                    print("Successfully booked your appointment at {}".format(appt_time_str))
                    quit()

        else:
            print("Appointment time is later than the one you currently have :(")
            quit()
