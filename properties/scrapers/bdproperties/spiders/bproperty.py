import scrapy
from scrapy import signals
from properties.models import *
from ..items import BpPropertyItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BpPropertySpider(scrapy.Spider):
    platform=""
    name = "bproperty_spider"
    start_urls = [
        "https://www.bproperty.com/en/bangladesh/properties-for-sale/",
        "https://www.bproperty.com/en/bangladesh/properties-for-rent/",
        "https://www.bproperty.com/en/bangladesh/commercial-for-sale/",
        "https://www.bproperty.com/en/bangladesh/commercial-for-rent/"
        ]


    website_main_url = "https://www.bproperty.com/"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This function generates an interrupt when the spider execution has completed and calls the function
        spider_closed. This is scrapy's built-in functionality.
        """
        spider = super(BpPropertySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self):
        self.logger.info('Spider opend')
        self.platform=Platfroms.objects.create(name="bproperty")

    def spider_closed(self):
        self.logger.info('Spider closed')
    #     """
    #     This function is called when the spider has finished execution and creates a single object against each run.
    #     """

    #     print("Updating Cars Data Objects to be updated in the database")
    #     # for idx, car_data in enumerate(self.update_cars_data):
    #     #     self.update_listing(car_data.get("url"), car_data.get("price"))
    #     # print("Objects Updated!")

    #     # # Updating last seen and other attributes in the db using bulk update
    #     # print("Updating DB Data using Bulk Update")
    #     # SeezDenmarkCarData.objects.bulk_update(self.bulk_update_list,
    #     #                                        ["schedule", "price_info", "last_seen_at"],
    #     #                                        batch_size=500)
    #     # print("Successfully updated")

    #     total_item=BpPropertyItem()
    #     total_item.save_to_database()
    #     print("Successfully Saved!")

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css("li article div a._287661cb::attr(href)").getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        commercial_type = "commercial" in response.url
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page,meta={"commercial_type":commercial_type}, errback=self.errback_httpbin)

        next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()

        # if next_page is not None:

        #     new_url = self.website_main_url+next_page
        #     yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):

        item = BpPropertyItem()
        item['commercial_type'] = response.request.meta['commercial_type']
        item['property_url'] = response.request.url
        item['property_description'] = response.css("div.daabbebb div div._208d68ae h1.fcca24e0::text").get()
        item['property_overview'] = response.xpath('string(//span[@class="_2a806e1e"])').get()
        item['price'] = response.css("span._105b8a67::text").get()
        item['location'] = response.css("div._1f0f1758::text").get()
        item['num_bed_rooms'] = response.css("span.fc2d1086::text").get()
        item['num_bath_rooms'] = response.css("span.fc2d1086::text").get()
        item['area'] = response.css("span.fc2d1086 span::text").get()
        item['building_type'] = response.css("ul._033281ab li span._812aa185::text").get()
        item['purpose'] = response.xpath('//span[contains(@aria-label, "Purpose")]/text()').get()
        amenities = '##'.join(response.css('div._40544a2f span._005a682a::text').getall())

        if amenities is None or len(amenities.strip()) == 0:
            item['amenities'] = ""

        else:
            amenities_list = amenities.replace("##:", ":").split("##")
            amenities_dict = {}
            for amenity in amenities_list:
                if ':' in amenity:
                    current_amenity = amenity.split(":")
                    amenities_dict[current_amenity[0]] = current_amenity[1]
                else:
                    amenities_dict[amenity] = "yes"

            item['amenities'] = amenities_dict
        print(self.platform)
        property=Property(
                platform=self.platform,
                commercial_type=item['commercial_type'],
                property_url=item['property_url'],
                property_description=item['property_description'],
                property_overview=item['property_overview'],
                price=item['price'],
                location=item['location'],
                num_bed_rooms=item['num_bed_rooms'],
                num_bath_rooms=item['num_bath_rooms'],
                area=item['area'],
                building_type=item['building_type'],
                purpose=item['purpose'],
                amenities=item['amenities']

            )
        property.save()
    def errback_httpbin(self, failure):
        # logs failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)

    
        