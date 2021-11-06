#!/bin/python

# Import libraries

import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# import argparse

# Set up the driver

driver = webdriver.Chrome()

driver.get("https://cmspweb.ip.tv/")

# Set functions

def login(ra, uf, password):
	driver.find_element(By.ID, "access-student").click() # Click on the "Student" button

	driver.find_element(By.ID, "ra-student").send_keys(ra[slice(0, -1)]) # Enter the student's RA
	driver.find_element(By.ID, "digit-student").send_keys(ra[slice(-1, -2, -1)]) # Enter the student's digit

	uf_stdent = driver.find_element(By.ID, "uf-student") # Select the student's UF
	Select(uf_stdent).select_by_value(uf) # Select the student's UF

	driver.find_element(By.ID, "password-student").send_keys(password) # Enter the student's password

	driver.find_element(By.ID, "btn-login-student").click() # Click on the "Login" button

def navigate(team):
	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "chng")).click() # Click on the "Groups" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.NAME, team)).click() # Click on the "Room" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "channelTaskList")).click() # Click on the "TaskList" button

	return driver.find_element(By.TAG_NAME, "iframe").get_attribute("src") # Get the "TaskList" iframe's src

def fill():
	driver.implicitly_wait(1000 * 3) # Wait 3 seconds
	tasks = WebDriverWait(driver, 900).until(lambda driver: driver.find_elements(By.XPATH, "//*[@id='root']/div/div[1]/main/div[1]/div/table/tbody/tr")) # Await load and get the tasks

	while len(tasks) > 0:
		tasks[0].click() # Click on the task

		driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/main/div[1]/div/table/tbody/tr[2]/td/div/div/div/div/div/button").click() # Click on the "Start" button

		driver.implicitly_wait(1000 * 6) # Wait 6 seconds
		radio = driver.find_elements(By.XPATH, "//div[@role='radiogroup']/div") # Get the radio buttons
		try:
			radio[random.randint(0, len(radio) - 1)].click() # Select a random option
		except:
			print("No radio buttons")

		checkbox = driver.find_element(By.XPATH, "//div[@class='question__body--multi']/div/div/span/span/input") # Get the checkbox buttons
		try:
			checkbox.click() # Select the checkbox
		except:
			print("No checkbox buttons")

		time.sleep(1) # Wait 1 seconds
		driver.implicitly_wait(1000 * 6) # Wait 6 seconds
		driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/button[1]").click() # Click on the "Confirm" button

		time.sleep(1) # Wait 1 seconds
		driver.implicitly_wait(1000 * 6) # Wait 6 seconds

		tasks = WebDriverWait(driver, 900).until(lambda driver: driver.find_elements(By.XPATH, "//*[@id='root']/div/div[1]/main/div[1]/div/table/tbody/tr")) # Await load and get the tasks

		print(int(len(tasks) / 2), "tasks found") # Print the number of tasks found

# Run the script

login("1082438340", "sp", "ju5lm9kw") # Login

task_url = navigate("[TURMA] 2ª C EM AMERICO DE MOU") # Navigate to the "TaskList" iframe
driver.get(task_url) # Get the "TaskList" iframe's src

fill() # Fill the tasks

driver.close() # Close the browser
