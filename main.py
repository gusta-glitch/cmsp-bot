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

from _info import __version__

# Set the arguments

max_amount = 100

parser = argparse.ArgumentParser(usage="%(prog)s [opitions]" ,description="Script to autofill tasklist o CMSP, write in Python", epilog="Developed by: @gustavofreitas", formatter_class=argparse.MetavarTypeHelpFormatter)

parser.add_argument("-V", "--version", help="show version and exit", action="version", version=f"%(prog)s {__version__}")

parser_login = parser.add_argument_group("Login")

parser_login.add_argument("-u", "--ra", type=str, help="RA of the student, with digit")
parser_login.add_argument("-c", "--uf", type=str, help="UF of the student", default="sp")
parser_login.add_argument("-p", "--password", type=str, help="password of the student")
parser_login.add_argument("-t", "--team", type=str, help="team of the student")
parser_login.add_argument("-a", "--amount", type=str, help="amount of tasks to fill", default="10")

parser_login.add_argument("--list", "-l", type=str, help="list of user to fill tasks [NOT WORKING]")

parser_debug = parser.add_argument_group("Debug")

parser_debug.add_argument("-v", "--verbose", help="verbose mode", action="store_true", default=False)

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
	print("No arguments")
	exit()

def debug(type, message):
	if args.verbose:
		if type == "error":
			print(f"\033[91m[ERROR]\033[0m {message}")
		elif type == "info":
			print(f"\033[92m[INFO]\033[0m {message}")
		elif type == "warning":
			print(f"\033[93m[WARNING]\033[0m {message}")
		elif type == "success":
			print(f"\033[94m[SUCCESS]\033[0m {message}")
		else:
			print(f"\033[95m[DEBUG]\033[0m {message}")

# Set up the driver

driver = webdriver.Chrome()

driver.get("https://cmspweb.ip.tv/") # Open the "CMSP" website

# Set functions

def login(ra, uf, password):
	debug("info", f"Logging in with RA:{ra} and UF:{uf}")

	driver.find_element(By.ID, "access-student").click() # Click on the "Student" button

	driver.find_element(By.ID, "ra-student").send_keys(ra[slice(0, -1)]) # Enter the student's RA
	driver.find_element(By.ID, "digit-student").send_keys(ra[slice(-1, -2, -1)]) # Enter the student's digit

	uf_stdent = driver.find_element(By.ID, "uf-student") # Select the student's UF
	Select(uf_stdent).select_by_value(uf) # Select the student's UF

	driver.find_element(By.ID, "password-student").send_keys(password) # Enter the student's password

	driver.find_element(By.ID, "btn-login-student").click() # Click on the "Login" button

	debug("success", f"Logged in with RA:{ra} and UF:{uf}")

	return 0
def navigate(team):
	debug("info", f"Navigating to team:{team}")

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "chng")).click() # Click on the "Groups" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.NAME, team)).click() # Click on the "Room" button

	driver.implicitly_wait(1000 * 1) # Wait 1 second
	WebDriverWait(driver, 900).until(lambda driver: driver.find_element(By.ID, "channelTaskList")).click() # Click on the "TaskList" button

	debug("success", f"Navigated to team:{team}")

	return driver.find_element(By.TAG_NAME, "iframe").get_attribute("src") # Get the "TaskList" iframe's src
def fill(amount):
	_amount = int(amount)

	tasks = driver.execute_script("return document.querySelectorAll(\"#root > div > div.homeuser > main > div.scrollable.homeuser__body--my-tasks > div > table > tbody > tr.MuiTableRow-root.row\")") # Get the tasks
	set_amount = 0 # Set the amount of tasks to fill
	conclued = 0 # Set the amount of tasks completed

	if tasks: # If there are tasks
		if amount == "all": # If the amount is "all"
			set_amount = len(tasks)
		elif _amount > 0 and _amount <= len(tasks): # If the amount is between 1 and the amount of tasks
			set_amount = _amount
		elif _amount > len(tasks): # If the amount is greater than the amount of tasks
			set_amount = len(tasks)
		else: # If the amount is invalid
			debug("error", f"Invalid amount of tasks to fill: {amount}")
			driver.close() # Close the driver

		debug("info" ,f"Filling {amount} tasks of {tasks}")

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
		debug("error", f"No tasks to fill")
		driver.close() # Close the driver

	debug("success", f"{conclued} tasks are completed")

# Run the script

login(arg_ra, arg_uf, arg_password) # Login

task_url = navigate(arg_team) # Navigate to the "TaskList" iframe
driver.get(task_url) # Get the "TaskList" iframe's src

fill(arg_amount) # Fill the tasks

driver.close() # Close the browser
