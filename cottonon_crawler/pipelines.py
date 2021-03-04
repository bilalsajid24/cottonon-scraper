class CottononCrawlerPipeline:
    def process_item(self, item, spider):
        # removing extra meta field for storing requests pipeline
        del item['meta']

        return item
