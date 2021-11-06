'''
This is a tool to scrape the data of courses from the website sis.hust.edu.vn.
The information includes:
    - Course code
    - Course name
    - Time
    - Number of credits
    - Tuition credits
    - Conditional course
    - English name
    - Abbreviation
    - Institute of Management

'''

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exception
import logging
import time

class CoursesList(scrapy.Spider):
    '''
    A class used to represent an Spider

    Variable:
         name (str): Name of Spider
         allowed_domains (arr): An optional list of strings containing domains that this spider is allowed to crawl
    '''

    name = "course"
    allowed_domains = ['sis.hust.edu.vn']

    def start_requests(self):
        '''
        The function makes a request which the spider will collect data from.

        Parameter:
            self: Reference to the current instance of the class

        variable:
            url: The web address will crawl the data

        Return:
            A request to a web page whose address is stored in the url variable and executes a callback function parse_source
        '''

        url = "http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx"
        yield scrapy.Request(url=url, callback=self.parse_sourse)

    def parse_sourse(self, response):
        '''
        Extract data, get necessary information, simulate operations

        Parameter:
            self: Reference to the current instance of the class
            response: The site's response to the request

        Variable:
            option: Manage ChromeDriver specific options
            desired_capabilities: Store 1 option of ChromeDriver
            driver: The instance of Chrome WebDriver is created with option
        '''

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe", desired_capabilities=desired_capabilities)

        driver.get("http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx")
        driver.implicitly_wait(2)

        while True:
            '''
            Execute it again and again before reaching the last page:
                - Using Selector to get page_source and save it in variable sel
                - Extract the required row information
                - For each row, use a for loop to get the entire subject data
            '''

            sel = Selector(text=driver.page_source)
            courses = sel.xpath("//table[@class='dxgvTable_SisTheme']//tr[@class='dxgvDataRow_SisTheme']")

            cnt = len(courses)

            for i in range(0, cnt, 1):
                '''
                Simulate the action of pressing the "+" button to see the expanded information of the subjects
                Extract the necessary data and save it in variables
                Return: information of required data fields
                '''

                btn_detail = driver.find_elements(By.XPATH, "//img[@class='dxGridView_gvDetailCollapsedButton_SisTheme']")
                if i == 0 or i == 1:
                    btn_detail[0].click()
                else:
                    btn_detail[i-1].click()
                time.sleep(1)

                detail = Selector(text=driver.page_source).xpath("//td[@class='dxgv dxgvDetailCell_SisTheme']//b/text()").getall()
                if len(detail) == 2:
                    HP_DK = None
                    Ten_tieng_anh = None
                    Ten_viet_tat = detail[0]
                    Vien_quan_ly = detail[1]
                elif len(detail) == 3:
                    HP_DK = None
                    Ten_tieng_anh = detail[0]
                    Ten_viet_tat = detail[1]
                    Vien_quan_ly = detail[2]
                else:
                    HP_DK = detail[0]
                    Ten_tieng_anh = detail[1]
                    Ten_viet_tat = detail[2]
                    Vien_quan_ly = detail[3]

                data = courses[i].xpath("td[@class='dxgv']/text()").getall()
                yield {
                    "Mã HP": data[0],
                    "Tên HP": data[1],
                    "Thời lượng": data[2],
                    "Số tín chỉ": data[3],
                    "TC học phí": data[4],
                    "Trọng số": data[5],
                    "Học phần điều kiện": HP_DK,
                    "Tên tiếng anh": Ten_tieng_anh,
                    "Tên viết tắt": Ten_viet_tat,
                    "Viện quản lý": Vien_quan_ly
                }
            try:
                '''Simulate the action of pressing the page switch to continue collecting data'''
                next_page = driver.find_element(By.XPATH, "//img[@class='dxWeb_pNext_SisTheme']")
                next_page.click()
                logging.info("NEXT PAGE INVALITE ------------------------------")
                time.sleep(1)
            except exception.NoSuchElementException:
                '''End the crawl when the next page is no longer available'''
                logging.info("BREAK PAGE ------------------------------")
                break
        '''Exit the browser window when the crawl is complete'''
        driver.quit()