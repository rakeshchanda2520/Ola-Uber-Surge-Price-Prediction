# import the packages
import numpy as np
import pandas as pd
from selenium import webdriver as driver
from time import sleep
from selenium.webdriver.common.by import By
import re
import time



# crate the class name as time_travel
# where it crates and returns the traveling time

class Time_travel:

    def __init__(self, destination, source, driver):
        self.destination = destination
        self.source = source
        self.driver = driver
        self.__url = " "
        # self.driver.minimize_window()

    def car_button_click(self):
        first_part = "https://www.google.com/maps/dir/"
        second_part = self.source + "/"
        third_part = self.destination
        last_part = "/"
        self.__url = first_part + second_part + third_part + last_part

        # crate the url to run selinum

        self.driver.get(self.__url)
        print(self.__url)
        sleep(10)

        # press the car button
        car_botton_driver = self.driver.find_element(By.XPATH,
                                                     "/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button")

        car_botton_driver.click()

        self.__url = self.driver.current_url
        print(self.__url)

    def add_time_traveling(self, time_stamp):
        # change the url and add the time stamp to it
        current_url = self.__url
        add_8_to_it = re.search("4m1", current_url)
        current_url = current_url[:add_8_to_it.end()] + "8" + current_url[add_8_to_it.end() + 1:]
        # print(current_url)
        add_7to_it = re.search("8!4m1", current_url)
        current_url = current_url[:add_7to_it.end()] + "7" + current_url[add_7to_it.end() + 1:]
        unknow_part = "!2m3!6e0!7e2!8j"
        str_time_stamp = str(int(time_stamp / 1000))
        car_code = "!3e0"
        new_url = current_url + unknow_part + str_time_stamp + car_code
        print(new_url)

        self.driver.get(new_url)

        # fatech the time to travel from destination to the source
        distance = self.driver.find_element(By.XPATH,
                                            "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/span[2]/span")

        distance_2 = self.driver.find_element(By.XPATH,
                                              "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div")

        return (distance.text, distance_2.text)





