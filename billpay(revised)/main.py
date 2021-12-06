from dotenv import load_dotenv  # read environment variables from .env file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
import time
import os

load_dotenv()

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

ERROR_AUTOPAY_MSG = "You have a scheduled payment or have AutoPay turned on, please review/edit your Payment Activity prior to making additional payments."

def pay_bill():
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
    
    # create alert object
    alert = Alert(driver)

    # USERNAME = "YOUR USERNAME"
    # PASSWORD = "YOUR PASSWORD"
    AMOUNT = input("enter amount of bill in format xx.xx: " )

    driver.get("https://secure8.i-doxs.net/CityOfPhiladelphiaWRB/SignIn.aspx")
    time.sleep(2)

    user = driver.find_element_by_id('main_UID')
    user.send_keys(USERNAME)

    passw = driver.find_element_by_id("main_PWD")
    passw.send_keys(PASSWORD)

    signin = driver.find_element_by_xpath('//*[@id="main_btnSubmit"]')
    signin.click()
    time.sleep(20)

    make_payment = driver.find_element_by_xpath('//*[@id="main_lnkMakePayment"]')
    make_payment.click()
    time.sleep(5)

    try:
        # check alert message. if autopay mentioned, dismiss alert
        if ERROR_AUTOPAY_MSG in alert.text:
            print("Autopay alert message.\nDismissing alert..")
            alert.dismiss() 
        
        pay_amount = driver.find_element_by_xpath('//*[@id="main_rptPayments_txtRptPaymentsAmount_0"]')
        pay_amount.send_keys(AMOUNT)
        next_button = driver.find_element_by_xpath('//*[@id="main_btnNext"]')
        next_button.click()

        pay_review = driver.find_element_by_xpath('//*[@id="main_lnkContinue"]')
        pay_review.click()

        final_pay = driver.find_element_by_xpath('//*[@id="main_btnPay"]')
        final_pay.click()
        
        print("Done!")
    except Exception as e:
        print(e)
    driver.quit()

# check if env variables are set..
if(CHROMEDRIVER_PATH != None and USERNAME != None and PASSWORD != None):
    pay_bill()
else: 
    # log message and quit program
    print("Please provide the following env variables in .env file:\nCHROMEDRIVER_PATH\nUSERNAME\nPASSWORD")
    exit()

