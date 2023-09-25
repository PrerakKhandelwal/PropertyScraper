# from django_cron import CronJobBase, Schedule
# from scrapy.crawler import CrawlerProcess
# from scraper.scraper.spiders import data_collector

# class RunScrapySpiderMorning(CronJobBase):
#     RUN_AT_TIMES = ['16:19']  # Specify the morning time (in 24-hour format)
#     schedule = Schedule(run_at_times=RUN_AT_TIMES)
#     code = 'properties.cronjobs.run_scrapy_spider'

#     def do(self):
#         process = CrawlerProcess()
#         process.crawl(data_collector)
#         process.start()

# # class RunScrapySpiderEvening(CronJobBase):
# #     RUN_AT_TIMES = ['18:00']  # Specify the evening time (in 24-hour format)
# #     schedule = Schedule(run_at_times=RUN_AT_TIMES)
# #     code = 'properties.run_scrapy_spider_evening'

# #     def do(self):
# #         process = CrawlerProcess()
# #         process.crawl(data_collector)
# #         process.start()