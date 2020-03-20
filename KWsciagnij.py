from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import codecs
import tkinter
import subprocess
import os, sys
from selenium.common.exceptions import NoSuchElementException 


def GetTXTfile():
    TXTpath=r'C:\Users\Daniel\Documents\programy\KWpython\LaziskabezWlodka.txt'
    TXTFile=open(TXTpath,'r')
    return TXTFile

def CreateDriver():
    
    #acessing Chrome user profile
    chrome_options = Options()
    chrome_options.add_argument("profile-directory=Profile 1")
    chrome_options.add_argument(r"user-data-dir=C:\Users\Daniel\AppData\Local\Google\Chrome\User Data")

    #Creating chrome webdriver and opening page
    driver=webdriver.Chrome(executable_path=r'C:\Users\Daniel\Documents\programy\KWpython\.vscode\chrome\chromedriver.exe',chrome_options=chrome_options)
    driver.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false")
    return driver
  
#input KW data
def InputKWdata(NumerKW):
    SpltdKW=NumerKW.split("_")
    kodWydzialuInput = driver.find_element_by_id("kodWydzialuInput")
    kodWydzialuInput.send_keys(SpltdKW[0])
    numerKsiegiWieczystej = driver.find_element_by_id('numerKsiegiWieczystej')
    numerKsiegiWieczystej.send_keys(SpltdKW[1])
    cyfraKontrolna= driver.find_element_by_id('cyfraKontrolna')
    cyfraKontrolna.send_keys(SpltdKW[2])
#wait for recaptcha tick img to show up
def Anticaptcha():
    try:
        wait = WebDriverWait(driver, 20000000000)
        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'solved_flag')))
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'status'), 'Solved'))
        #driver.implicitly_wait(100000000000)
    finally:
        #driver.implicitly_wait(100000000000)
            driver.find_element_by_id('wyszukaj').click()
            bledKW=bledneKW()
            if bledKW==True:
                sys.exit("bledne KW") 
            bledKW=bledneKW2()
            if bledKW==True:
                sys.exit("bledne KW") 


def bledneKW():
    try:
        driver.find_element_by_css_selector('div.error')
    except NoSuchElementException:
        return False
    return True

def bledneKW2():
    try:
        driver.find_element_by_css_selector('span#cyfraKontrolna--cyfra-kontrolna.error.visible')
    except NoSuchElementException:
        return False
    return True

                


#saves page source to Html file in download folder
def SaveHtml(filename, index):
    MyDocpath=os.path.join(os.path.expanduser('~/Documents'),filename+str(index))
    file_object = codecs.open(MyDocpath +".htm", "w", "utf-8")
    html = driver.page_source
    file_object.write(html)

#Clicks given dzial link
def NextDzial(dzial):
    DzialLink=driver.find_element_by_xpath("//input[@value='"+dzial+"']")
    DzialLink.click()

#Iterates and saves Html from each dzial
def IterateDzialy(NumerKW):
    DzialyList= ["Dział I-O", "Dział I-Sp", "Dział II", "Dział III", "Dział IV"]
    i=0
    for dzial in DzialyList:
        i+=1
        NextDzial(dzial)
        #spltedzial=dzial.split(" ")
        #SaveHtml(file=spltedzial[1])
        SaveHtml(filename=NumerKW, index=i)

def rest():
    #driver.find_element_by_id('przyciskWydrukZupelny').click()
    SaveHtml(filename=NumerKW, index="0")
    IterateDzialy(NumerKW)
    driver.close()
    subprocess.call(["Htm2pdf.exe",NumerKW])

def tst2(driver):
    InputKWdata(NumerKW)
    Anticaptcha()
    #click wydrukZupelny
    #wait = WebDriverWait(driver, 20000000)
    #while wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'solved_flag'))):
    #    tst2()
    #wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'status'), 'Solved'))
    """while EC.text_to_be_present_in_element((By.CLASS_NAME, 'status'), 'Solved')==False:
        Anticaptcha()
    else:"""
    try:
        driver.find_element_by_id('przyciskWydrukZupelny').click()
    except NoSuchElementException:
        tst2(driver)

    """"while wyn==False:
        try:
            driver.find_element_by_id('przyciskWydrukZupelny').click()
        except NoSuchElementException:
            tst2()
            wyn=False
        wyn=True"""
    #driver.find_element_by_id('wyszukaj').click()
    """try:
        wait.until(EC.element_to_be_clickable((By.ID, 'przyciskWydrukZupelny')))
    finally:"""
    #driver.find_element_by_id('przyciskWydrukZupelny').click()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Main Logic!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

TXTFile=GetTXTfile()
for NumerKW in TXTFile:
    wyn=False
    NumerKW=NumerKW[:-1]
    print(NumerKW)
    driver=CreateDriver()
    tst2(driver)


    SaveHtml(filename=NumerKW, index="0")
    IterateDzialy(NumerKW)
    subprocess.call(["Htm2pdf.exe",NumerKW])
    driver.close()
