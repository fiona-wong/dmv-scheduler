from splinter import Browser
from datetime import datetime

with Browser("chrome") as browser:
    # visit url
    url = "https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit&localeName=en"
    browser.visit(url)
    browser.cookies.delete()

    # constants
    default_office = "503"
    task_numbers = ["1", "2", "3"]
    reasons_for_visit = ["taskRID", "taskCID", "taskVR"]
    first_name = "Mike"
    last_name = "Jones"
    tel_area = "281"
    tel_prefix = "330"
    tel_suffix = "8004"
    email = "mikejones@gmail.com"
    # if you don't have a current appt time, just make one really far out or the latest possible
    current_appt_time = 'Monday, June 4, 2018 at 5:00 PM'

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
        appt_time_str = appt_table.split('\n')[5]
        current_appt_datetime = datetime.strptime(current_appt_time, '%A, %B %d, %Y at %I:%M %p')
        new_appt_datetime_object = datetime.strptime(appt_time_str, '%A, %B %d, %Y at %I:%M %p')
        is_new_appttime_earlier = new_appt_datetime_object < current_appt_datetime
        if is_new_appttime_earlier:
            continue_xpath = "//a[contains(text(), 'Continue')]"
            browser.find_by_xpath(continue_xpath).click()
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
                current_appt_time = appt_time_str
                print("Successfully booked your appointment at {}".format(appt_time_str))
                quit()
                # if you already have a prior appt it goes here to confirm
                if browser.is_element_present_by_value("Confirm New Appointment", 20):
                    current_appt_time = appt_time_str
                    browser.find_by_value("Confirm New Appointment").click()
                    if browser.is_element_present_by_value("Continue", 20):
                        browser.choose("notificationMethod", "EMAIL")
                        browser.find_by_name("notify_email").fill(email)
                        browser.find_by_name("notify_email_confirm").fill(email)
                        browser.find_by_value("Continue").click()
                        current_appt_time = appt_time_str
                        print("Successfully booked your new appointment at {}".format(appt_time_str))
                        quit()
        else:
            print("Appointment time is later than the one you currently have :(")
            quit()
