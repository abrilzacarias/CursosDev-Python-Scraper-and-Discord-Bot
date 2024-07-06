# CoursesDev Scraper and Discord Bot

This repository contains a web scraper for [CursosDev](https://www.cursosdev.com) and a Discord bot that can filter and display courses based on user-specified keywords. The scraper extracts course data from the website and stores it in a JSON file, which the Discord bot then uses to respond to user commands.

![image](https://github.com/abrilzacarias/CursosDev-Python-Scraper-and-Discord-Bot/assets/83786610/beb2e902-b561-4559-bbfc-2de9ee29c31c)

## Features

- Scrapes course data from CursosDev.com
- Stores course data in a JSON file
- Automatically runs the scraper twice a day
- Discord bot that filters and displays courses based on keywords

## Scraper

The scraper is built using Scrapy and runs twice a day to ensure that the course data is up-to-date.

## Discord Bot

The Discord bot is built using `discord.py` and responds to commands to filter and display course data.

## Improvements to Implement

- **Cloud Deployment**: Deploy the scraper to the cloud to ensure it runs twice a day without needing to keep the local machine on.
- **Database Connection**: Connect the scraper to a database for more efficient data storage and retrieval.
- **Additional Command**: Implement another command to list all the courses available in the JSON file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Scrapy](https://scrapy.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [Schedule](https://schedule.readthedocs.io/)

