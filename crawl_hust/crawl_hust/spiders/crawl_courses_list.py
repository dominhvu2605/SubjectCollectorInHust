import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exception

import logging
import time

class CoursesList(scrapy.Spider):
    name = "course"
    allowed_domains = ['sis.hust.edu.vn']
    # start_urls = ["http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx"]

    # PATH = "D:\chromedriver\chromedriver.exe"
    # driver = webdriver.Chrome(PATH)
    # driver.get("http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx")

    def start_requests(self):
        url = "http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx"
        yield scrapy.Request(url=url, callback=self.parse_sourse)

    def parse_sourse(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe",desired_capabilities=desired_capabilities)

        driver.get("http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx")
        driver.implicitly_wait(2)

        while True:
            sel = Selector(text=driver.page_source)
            courses = sel.xpath("//table[@class='dxgvTable_SisTheme']//tr[@class='dxgvDataRow_SisTheme']")

            cnt = len(courses)

            for i in range(0, cnt, 1):
                data = courses[i].xpath("td[@class='dxgv']/text()").getall()
                yield {
                    "Mã HP": data[0],
                    "Tên HP": data[1],
                    "Thời lượng": data[2],
                    "Số tín chỉ": data[3],
                    "TC học phí": data[4],
                    "Trọng số": data[5]
                }
                # yield items
            # next_page = driver.find_element(By.XPATH, "//img[@alt='Next']")
            # next_page.click()
            try:
                next_page = driver.find_element(By.XPATH, "//img[@class='dxWeb_pNext_SisTheme']")
                next_page.click()
                logging.info("NEXT PAGE INVALITE ------------------------------")
                time.sleep(0.2)
            except exception.NoSuchElementException:
                logging.info("BREAK PAGE ------------------------------")
                break

        driver.quit()