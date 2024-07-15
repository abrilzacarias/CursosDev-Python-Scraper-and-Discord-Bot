# CoursesDev Scraper and Discord Bot

This repository contains a web scraper for [CursosDev](https://www.cursosdev.com) and a Discord bot that can filter and display free Udemy courses based on user-specified keywords. The scraper extracts course data from the website and stores it in a database, which the Discord bot then uses to respond to user commands.

![image](https://github.com/abrilzacarias/CursosDev-Python-Scraper-and-Discord-Bot/assets/83786610/beb2e902-b561-4559-bbfc-2de9ee29c31c)

## Features

- Scrapes course data from CursosDev.com
- Stores course data in a MySQL database
- Automatically runs the scraper once a day at a predetermined time
- Discord bot that filters and displays courses based on keywords or the creator's name
- Automatically deletes courses older than one week from the database, since those no longer have coupons associated with them

## Scraper

The scraper is built using Scrapy and runs once a day to ensure that the course data is up-to-date. It stores the scraped data in a MySQL database.

## Discord Bot

The Discord bot is built using discord.py and responds to commands to filter and display course data. Commands include:

- !search <term>: Filters courses based on the specified keyword.
- !today: Lists all courses available today.
- !search_creator <creator_name>: Filters courses based on the creator's name.

## Acknowledgments

- [Scrapy](https://scrapy.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [Schedule](https://schedule.readthedocs.io/)

