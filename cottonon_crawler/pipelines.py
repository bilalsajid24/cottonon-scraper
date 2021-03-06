import os
import csv


class CottononCrawlerPipeline:
    def open_spider(self, spider):
        if spider.get_menu_items and not os.environ.get('FILE_PATH'):
            raise Exception('Define menu items file path in environment for read and write')

        return

    def process_item(self, item, spider):
        # removing extra meta field for storing requests pipeline
        del item['meta']

        return item

    def close_spider(self, spider):
        if not spider.get_menu_items:
            return

        csv_file = open(os.environ['FILE_PATH'], 'w', newline='')

        fieldnames = ['Category', 'Url']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for item in spider.menu_items:
            csv_writer.writerow(item)

        csv_file.close()
