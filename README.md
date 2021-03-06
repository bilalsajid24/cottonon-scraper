## Cottonon SG Data Scraper

A scraper for fetching data from Cottonon SG retailer website `https://cottonon.com/SG/`


## Setup Guidelines

- Create a separate virtualenv 
- Install requirements `pip install -r requirements.txt`
- Set environment variables `LOG_LEVEL -> DEBUG/INFO` and `FILE_PATH -> The path of the file you want to read from and write to`

## Simple crawler
- For running a default crawl run command `scrapy crawl cottonon-crawler`

## Savaing menu items to CSV
- Before running the crawler make sure to include `FILE_PATH` into your enviroment variable including the name of the file you want to save to.
- For saving menu items (categories) to a CSV file run command `scrapy crawl conttonon-crawler -a menu_items=true`. This will create a file to the path you provided in the environment variable

## Read category URLs from file
- Make sure your the FILE_PATH in the evironment is a valid path for the file you want to read
- For reading the URLs from the file run command  `scrapy crawl cottonon-crawler -a read_from_file=true`. This will read the URLs from the file and start the crawling process

