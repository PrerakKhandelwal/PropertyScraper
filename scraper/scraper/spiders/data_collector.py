from selenium.webdriver.support.wait import WebDriverWait 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import scrapy
import time
import sys
from selenium.webdriver.common.keys import Keys
from django.db import connections
from scraper.items import MyModelItem


search_url = 'https://www.99acres.com/search/property/buy/'
google = "https://www.google.com/"



class property_scrappers(scrapy.Spider):
    name = "data_collector"
    start_urls = [google]
    

    def __init__(self, *args, **kwargs):
        super(property_scrappers, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(executable_path='/home/prerak/lyxel/chromedriver')
        wait = WebDriverWait(self.driver, 5)
        self.driver.set_page_load_timeout(15)
        self.driver.set_window_size(1920,1080)
        # self.datalist=[]
        self.cities=['Pune', 'Delhi', 'Mumbai', 'Lucknow', 'Agra', 'Ahmedabad', 'Kolkata', 'Jaipur', 'Chennai', 'Bengaluru']
          

    

    def do_initials(self):
        try:
            self.driver.get(google)
            time.sleep(3)
            self.driver.execute_script("window.location.href = '{}';".format(search_url))
            time.sleep(7)
            

        except TimeoutException:
            exc_type, exc_obj, exc_tb=sys.exc_info()
            message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
            print(message)
       

  
    def parse(self, response):
        try:
            for city in self.cities:
                try:
                    self.do_initials()
                    search_button=self.driver.find_element('xpath','//input[@class="list_header_semiBold "]')
                    search_button.click()
                    time.sleep(2)
                    search_button.send_keys(city)
                    search_button.send_keys(Keys.RETURN)
                    time.sleep(10)
                    for i in range(150):
                        self.driver.execute_script("window.scrollBy(0,500);")
                        time.sleep(2)
                    res = scrapy.Selector(text=self.driver.page_source)
                    print(res)
                    # input()
                    sections = res.xpath('//div[@class="pageComponent undefined"]/section')
                    for section in sections:
                       

                        data = MyModelItem()

                        property_name = property_cost = property_text = property_type = property_area = property_locality = property_city = property_link = ''

                        property_name = section.xpath('.//td[@class="srpTuple__propertyPremiumHeading srpTuple__spacer10 srpTuple__tdClasstwoPremium "]/a[@class="srpTuple__dFlex"]/text() | .//a[@class="projectTuple__projectName  projectTuple__pdWrap20 ellipsis"]/text()').extract_first()
                        
                        property_cost = section.xpath('.//span[@class="list_header_bold configurationCards__srpPriceHeading configurationCards__configurationCardsHeading"]/text()').extract()
                        try: 
                            property_cost=''.join(property_cost)
                            

                            if not property_cost:
                                property_cost = section.xpath('.//td[@id="srp_tuple_price"][1]/text() | .//table[@class="srpTuple__tableFSL"]//td[@id="srp_tuple_price"]/text()').extract()
                                if len(property_cost)>1:
                                    property_cost.pop()
                                property_cost=''.join(property_cost)
                              
                            
                            try:
                                unit_val=''
                                unit_val = section.xpath('.//span[@id="srp_tuple_price_unit"]/text()').extract_first()
                                if unit_val:
                                    property_cost = property_cost+" "+unit_val
                            except Exception as e:
                                exc_type, exc_obj, exc_tb=sys.exc_info()
                                message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
                                print(message)

                        except Exception as e:
                                exc_type, exc_obj, exc_tb=sys.exc_info()
                                message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
                                print(message)


                    
                        property_text = section.xpath('.//h2/text()').extract_first()
                        property_type = property_text.split(' in ')[0].strip()
                        property_area = section.xpath('.//td[@id = "srp_tuple_primary_area"]/text() | .//div[@class="carousel__slidingBox  "]//span[@class="caption_subdued_medium configurationCards__cardAreaSubHeadingOne"]/text()').extract()
                        property_area=''.join(property_area)
                        property_area = str(property_area)
                        if 'sq.ft.' not in property_area:
                            property_area=property_area + "sq.ft."
                        property_locality = property_text.split('in',1)[1].strip()
                        property_city = city
                        property_link = section.xpath('.//table[@class="srpTuple__tableFSL"]//td[@class="srpTuple__tdClassPremium"]/a/@href | .//a[@class="projectTuple__projectName  projectTuple__pdWrap20 ellipsis"]/@href').extract_first()
                        
                        
                        
                        if not property_link:
                            property_link = section.xpath('.//table//td[@class="srpTuple__tdClassPremium"]/a/@href').extract_first()

                        if not property_name:
                            property_name = section.xpath('.//td[@id="srp_tuple_society_heading"]//text()').extract_first()



                        data['property_name']=property_name
                        data['property_cost']=property_cost
                        data['property_type']=property_type
                        data['property_area']=property_area
                        data['property_locality']=property_locality
                        data['property_city']=property_city
                        data['property_link']= property_link
                        # print(data)
                        
                        yield data  

                        
                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb=sys.exc_info()
                    message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
                    print(message)

            
        except Exception as e:
            exc_type, exc_obj, exc_tb=sys.exc_info()
            message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
            print(message)
            
        finally:
            self.driver.quit() 
            

