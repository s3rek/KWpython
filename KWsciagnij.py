from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import codecs
import tkinter


def GetNumerKW():
    TXTpath=r'C:\Users\Daniel\Documents\programy\KWpython\LaziskabezWlodka.txt'
    TXTfile=open(TXTpath,'r')
    for NumerKW in TXTfile:
        print(NumerKW)
        return NumerKW

GetNumerKW()

def CreateDriver():
    chrome_options = Options()
    chrome_options.add_argument("profile-directory=Profile 1")
    chrome_options.add_argument(r"user-data-dir=C:\Users\Daniel\AppData\Local\Google\Chrome\User Data")


def tst():
    chrome_options = Options()
    chrome_options.add_argument("profile-directory=Profile 1")
    chrome_options.add_argument(r"user-data-dir=C:\Users\Daniel\AppData\Local\Google\Chrome\User Data")

    driver=webdriver.Chrome(executable_path=r'C:\Users\Daniel\Documents\programy\KWpython\.vscode\chrome\chromedriver.exe',chrome_options=chrome_options)
    driver.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false")
    kodWydzialuInput = driver.find_element_by_id("kodWydzialuInput")


    kodWydzialuInput.send_keys("GL1W")
    numerKsiegiWieczystej = driver.find_element_by_id('numerKsiegiWieczystej')
    numerKsiegiWieczystej.send_keys('00012278')
    cyfraKontrolna= driver.find_element_by_id('cyfraKontrolna')
    cyfraKontrolna.send_keys('7')



    wait = WebDriverWait(driver, 200)
    #Anticaptcha= driver.find_element_by_class_name('antigate_solver recaptcha error')
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'solved_flag')))

    #CLick wyszukaj
    driver.find_element_by_id('wyszukaj').click()

    #click wydrukZupelny
    driver.find_element_by_id('przyciskWydrukZupelny').click()

    #Dział III Dział II Dział I-Sp Dział I-O Dział IV
    file_object = codecs.open("dzial0"+"plik.html", "w", "utf-8")
    html = driver.page_source
    file_object.write(html)

    dzial=driver.find_element_by_xpath("//input[@value='Dział IV']")
    dzial.click()
    file_object = codecs.open("dzial4"+"plik.html", "w", "utf-8")
    html = driver.page_source
    file_object.write(html)


    print("end")
    driver.close()
