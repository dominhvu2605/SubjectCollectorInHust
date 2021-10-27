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
        driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe", desired_capabilities=desired_capabilities)

        driver.get("http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx")
        driver.implicitly_wait(2)

        while True:
            # lay du lieu chung cua cac mon hoc
            sel = Selector(text=driver.page_source)
            courses = sel.xpath("//table[@class='dxgvTable_SisTheme']//tr[@class='dxgvDataRow_SisTheme']")

            cnt = len(courses)

            for i in range(0, cnt, 1):
                # an nut xem chi tiet mon hoc
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
                # yield items
            # next_page = driver.find_element(By.XPATH, "//img[@alt='Next']")
            # next_page.click()
            try:
                next_page = driver.find_element(By.XPATH, "//img[@class='dxWeb_pNext_SisTheme']")
                next_page.click()
                logging.info("NEXT PAGE INVALITE ------------------------------")
                time.sleep(1)
            except exception.NoSuchElementException:
                logging.info("BREAK PAGE ------------------------------")
                break

        driver.quit()
