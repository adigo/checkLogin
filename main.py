#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Cheng-Yi Lee
# Created Date: 03/15/2021
# Version     : v 1.0.0
# =============================================================================
# use below command to create checkLogin-selenium.spec if not exists
# pyi-makespec main.py --onefile --noconsole --add-binary "./driver/chromedriver.exe;./driver" --add-data "checkLogin.json;." --add-data "checkLogin.ini;." --name checkLogin-selenium
# add below code to the end of checkLogin-selenium.spec if it's newly created
# import shutil
# shutil.copyfile('checkLogin.ini', '{0}/checkLogin.ini'.format(DISTPATH))
# shutil.copyfile('checkLogin.json', '{0}/checkLogin.json'.format(DISTPATH))
# use below command to create the exe file
# pyinstaller --clean checkLogin-selenium.spec
import json
import os
import smtplib
import sys
from email.mime.text import MIMEText
from time import sleep
from configparser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


# for pyinstaller
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def main():
    # non-pythonic way of reading the json file.
    # note that the default path is used because pyinstaller has problem with windows scheduler
    file_path = "checkLogin.json"
    i = 0
    while i < 2:
        try:
            f = open(file_path, "r")
            i = 2
        except EnvironmentError:
            file_path = "C:\\checkLogin\\checkLogin.json"
            i += 1
    with f:
        credentials = json.load(f)
        username = credentials["username"]
        password = credentials["password"]
        sender = credentials["sender"]
        sender_pass = credentials["sender_pass"]
        recipients = credentials["recipients"]
    f.close()

    # reading the ini file
    # note that the default path is used because pyinstaller has problem with windows scheduler
    config = ConfigParser()
    dataset = config.read("checkLogin.ini")
    if len(dataset) == 0:
        config.read("C:\\checkLogin\\checkLogin.ini")
    chrome_driver_path = config.get("chromedriver", "path")
    duration = config.getint("delay", "seconds")

    # getting the driver file
    # note that the default path is used because pyinstaller has problem with windows scheduler
    use_default = False
    try:
        driver = webdriver.Chrome(resource_path(chrome_driver_path))
    except EnvironmentError:
        use_default = True
    if use_default:
        driver = webdriver.Chrome(executable_path=r"C:\checkLogin\driver\chromedriver.exe")
    url = config.get("website", "url")
    driver.get(url)

    # try to login
    sleep(duration)
    username_form_input = driver.find_element_by_id("name-inputEl")
    username_form_input.send_keys(username)
    sleep(duration)

    password_form_input = driver.find_element_by_id("textfield-1009-inputEl")
    password_form_input.send_keys(password)
    sleep(duration)
    password_form_input.send_keys(Keys.ENTER)
    sleep(duration)

    # check if JDBC error occurs
    login_failed = True
    try:
        failed_header_text = driver.find_element_by_id("messagebox-1001_header-title-textEl").text
        failed_msg_text = driver.find_element_by_id("messagebox-1001-msg").text
    except NoSuchElementException:
        login_failed = False

    if login_failed:
        # send email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            message = MIMEText(f"Synoptix login failed with {failed_msg_text}")
            message['Subject'] = "Synoptix login failed"
            message['From'] = sender
            message['To'] = ", ".join(recipients)
            connection.starttls()
            connection.login(sender, sender_pass)
            connection.sendmail(sender, recipients, message.as_string())
    else:
        # log out
        WebDriverWait(driver, duration).until(lambda s: s.find_element_by_id("button-1048").is_displayed())
        to_click = driver.find_element_by_id("button-1048")
        to_click.click()
        sleep(duration)
        to_click = driver.find_element_by_id("syn-menubar-account-btnInnerEl")
        to_click.click()
        sleep(duration)
        to_click = driver.find_element_by_id("syn-logout-btn-btnInnerEl")
        to_click.click()
        sleep(duration)

    driver.quit()


if __name__ == '__main__':
    main()