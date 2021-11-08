#!/usr/bin/python

# Import libraries

import argparse
import json
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# Set the arguments

max_amount = 100

parser = argparse.ArgumentParser(description="Fill the tasklist", formatter_class=argparse.MetavarTypeHelpFormatter)

parser.add_argument("--ra", "-u", type=str, help="RA of the student, with digit")
parser.add_argument("--uf", "-c", type=str, help="UF of the student", default="sp")
parser.add_argument("--password", "-p", type=str, help="Password of the student")
parser.add_argument("--team", "-t", type=str, help="Team of the student")
parser.add_argument("--amount", "-a", type=str, help="Amount of tasks to fill", default="10")

parser.add_argument("--list", "-l", type=str, help="List of user to fill tasks, files superteds: .json")

args = parser.parse_args()

if args.ra and args.password and args.team:
	arg_ra = args.ra
	arg_uf = args.uf
	arg_password = args.password
	arg_team = args.team
	arg_amount = args.amount

	if args.ra.find(".") or args.ra.find("-"):
		try:
			arg_ra = args.ra.replace(".", "")
		except:
			print("Invalid RA, use pattern")
			exit()
		else:
			arg_ra = arg_ra.replace("-", "")
	if args.list:
		with open(args.list, "r") as file:
			if file.name.endswith(".json"):
				arg_list = json.load(file)["users"]
else:
	print("No args")
	exit()

# Set up the driver

driver = webdriver.Chrome()

driver.get("https://cmspweb.ip.tv/") # Open the "CMSP" website

# Set functions

def login(ra, uf, password):
	driver.find_element(By.ID, "access-student").click() # Click on the "Student" button

	driver.find_element(By.ID, "ra-student").send_keys(ra[slice(0, -1)]) # Enter the student's RA
	driver.find_element(By.ID, "digit-student").send_keys(ra[slice(-1, -2, -1)]) # Enter the student's digit

	uf_stdent = driver.find_element(By.ID, "uf-student") # Select the student's UF
	Select(uf_stdent).select_by_value(uf) # Select the student's UF

	driver.find_element(By.ID, "password-student").send_keys(password) # Enter the student's password

	driver.find_element(By.ID, "btn-login-student").click() # Click on the "Login" button

	print(f"Logged in as {ra[slice(0, -1)]}-{ra[slice(-1, -2, -1)]} in {uf}")

	return 0
def navigate(team):
	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "chng")).click() # Click on the "Groups" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.NAME, team)).click() # Click on the "Room" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "channelTaskList")).click() # Click on the "TaskList" button

	print(f"Navigated to {team}")

	return driver.find_element(By.TAG_NAME, "iframe").get_attribute("src") # Get the "TaskList" iframe's src
def fill(amount):
	time.sleep(1) # Wait 1 second

	tasks = driver.execute_script("return document.querySelectorAll(\"#root > div > div.homeuser > main > div.scrollable.homeuser__body--my-tasks > div > table > tbody > tr.MuiTableRow-root.row\")") # Get the tasks
	set_amount = 0 # Set the amount of tasks to fill
	conclued = 0 # Set the amount of tasks completed

	if tasks: # If there are tasks
		if amount == "all": # If the amount is "all"
			set_amount = len(tasks)
		elif int(amount) > 0 and int(amount) <= len(tasks): # If the amount is between 1 and the amount of tasks
			set_amount = int(amount)
		elif amount > len(tasks): # If the amount is greater than the amount of tasks
			set_amount = len(tasks)
		else: # If the amount is invalid
			print("The amount of tasks is invalid")
			driver.close() # Close the driver

		print(f"Filling {amount} tasks of {tasks}")

		for filled in range(0, set_amount):
			for task in tasks:
				task.click() # Click on the task

				driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/main/div[1]/div/table/tbody/tr[2]/td/div/div/div/div/div/button").click() # Click on the "Start" button

				driver.implicitly_wait(1000 * 6) # Wait 6 seconds
				radio_group = WebDriverWait(driver, 900).until(lambda driver: driver.find_elements(By.XPATH, "//div[@role='radiogroup']"))

				for input_radio in radio_group:
					time.sleep(0.6) # Wait 600 milliseconds
					input_radio.find_elements(By.TAG_NAME, "input")[random.randint(0, len(input_radio.find_elements(By.TAG_NAME, "input")) - 1)].click() # Click on a random radio button
				driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/button[1]").click() # Click on the "Confirm" button

			print(f"{filled} tasks are filled")
			conclued += 1 # Increase the amount of tasks completed
	else:
		print("No tasks to fill")
		driver.close() # Close the driver

	print(f"{conclued} tasks are conclued")

# Run the script

login(arg_ra, arg_uf, arg_password) # Login

task_url = navigate(arg_team) # Navigate to the "TaskList" iframe
driver.get(task_url) # Get the "TaskList" iframe's src

fill(arg_amount) # Fill the tasks

driver.close() # Close the browser
