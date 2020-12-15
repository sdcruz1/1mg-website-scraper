#importing stuff
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep

#DB vars
db = sqlite3.connect('drugsRelated.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS drugs(name TEXT,related TEXT)''')
drugList=[]

relatedDrugsList=[]
#sele vars
driver = webdriver.Firefox()

def getDrugs(pagelink):
	driver.get(pagelink)
	sleep(1)

	for i in range(200):

		if i==0:
			sleep(2)

		try:
			drugpath = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/div/div/div[3]/div/div[4]/div[4]/div[{}]/div/div/a[1]/div[2]".format(i+1))
			cancer = driver.find_element_by_xpath("/html/body/div[1]/div/div/a[1]/svg/g/path")
			cancer.click()
			drugpath.click()
			relatedDrugs=[]
			for j in range(5):
				relatedDrug = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[{}]/div/div[2]/a".format(j+1))
				driver.execute_script("return arguments[0].scrollIntoView();",relatedDrug)
				relatedDrugs.append(relatedDrug.text)

			relatedDrugsList.append(','.join(relatedDrugs))
			print relatedDrugsList
			driver.get(pagelink)
			sleep(2)
		except NoSuchElementException:
			sleep(0.5)

		drugpath = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/div/div/div[3]/div/div[4]/div[4]/div[{}]/div/div/a[1]/div[2]".format(i+1))
		drugName = drugpath.text
		driver.execute_script("return arguments[0].scrollIntoView();",drugpath)
		drugList.append(drugName)

		if i%10==0:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	for name in drugList,relatedDrugsList:
		cursor.execute('''INSERT INTO drugs(name,related) VALUES(?,?)''', (name,related))
	print"Added:"+pagelink
	db.commit()

	print "Done: "+pagelink
getDrugs("https://www.1mg.com/categories/featured-128")
getDrugs("https://www.1mg.com/categories/exclusive-65")
getDrugs("https://www.1mg.com/categories/fitness-supplements-5")
getDrugs("https://www.1mg.com/categories/health-conditions/diabetes-care-29")
getDrugs("https://www.1mg.com/categories/personal-care-18")
getDrugs("https://www.1mg.com/categories/health-conditions-28")
getDrugs("https://www.1mg.com/categories/ayurveda/all-products-56")
getDrugs("https://www.1mg.com/categories/homeopathy/all-products-64")

driver.close()

#/html/body/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/a
#/html/body/div[5]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/a
#/html/body/div[5]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/a
#related xpath2------->   /html/body/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/a
#/html/body/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]
#/html/body/div[5]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]

#/html/body/div[4]/div[1]/div/div/div/div/div[3]/div/div[4]/div[4]/div[1]/div/div/a[1]/div[2]
#/html/body/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/a
#/html/body/div[5]/div[1]/div/div/div/div/div[3]/div/div[4]/div[4]/div[1]/div/div/a[1]/div[2]
#/html/body/div[4]/div[1]/div/div/div/div/div[3]/div/div[4]/div[4]/div[1]/div/div/a[1]/div[2]
