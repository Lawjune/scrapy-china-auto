import scrapy

class ChinaAutoSales(scrapy.Spider):
    name = "china_auto_sales"
    start_urls = ["https://xl.16888.com/style-202204-202204-1.html"]

    def parse(self, response):
        data = response.css('div.xl-table-data')
        table = data.css('table.xl-table-def.xl-table-a')
        table_rows = table.css('tr')
        header_row = table_rows[0]
        for i in range(1, len(table_rows)):
            yield {
                
                header_row.css('th::text').extract()[0]: # 排名
                    table_rows[i].css('td::text').extract()[0],
                
                header_row.css('th::text').extract()[1]: # 车型
                    table_rows[i].css("a::text").get(), 

                header_row.css('th::text').extract()[2]: # 销量
                    table_rows[i].css('td::text').extract()[0], 

                header_row.css('th::text').extract()[3]: # 厂商
                    table_rows[i].css("a::text").getall()[1], 
                
                header_row.css('th::text').extract()[4]: # 售价（万元）
                    table_rows[i].css("a::text").getall()[2], 
            }
            
        next_page = response.css('a.lineBlock.next').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse)
