<p align="center">
  <img src="images/user-agent-dict-logo.png" alt="User Agent Dictionary Logo">
</p>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Add3r/UserAgent-Parser) [![Awesome](https://img.shields.io/badge/Awesome-%F0%9F%98%8E-blueviolet.svg)](https://shields.io/) ![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg) ![Repository Views](https://komarev.com/ghpvc/?username=Add3r&label=Repository+Views) ![Release Downloads](https://img.shields.io/github/test/Add3r/UserAgent-Parser/releases/tag/V1.0.0/total.svg) ![Python](https://img.shields.io/badge/Python-3.11.5-blue.svg)

![Dictionary Download](https://img.shields.io/github/downloads/Add3r/UserAgent-Parser/blob/main/user_agents.json/total.svg) ![Total User-Agents Archived](https://img.shields.io/badge/Total%20User--Agents%20Archived-11256-blue.svg) ![Mobile User-Agents](https://img.shields.io/badge/Mobile%20User--Agents-629-green.svg) ![General User-Agents](https://img.shields.io/badge/General%20User--Agents-10627-green.svg)


# UserAgent-Dictionary

This repository holds data for the Proxy_Bypass vulnerability research tool with the `user-agents.json` file generated from the `User-Agent-Parser.py` script within this repository. Additionally, the `ua-stats.py` script is used to draw various statistics out of the `user-agents.json` file.

## Overview

The User Agent Data Scraper is designed to:

🎯 **Primary:**
- Scrape user agent data from [useragentstring.com](https://www.useragentstring.com/pages/All/)
- Create a dictionary of user agents to be used by the proxy-bypass vulnerability research tool
- Organize the data into dictionaries.

🚀 **Secondary:**
- Identify user agent groups based on specified conditions.
- Display statistics about general and mobile user agents.
- Provide options for data visualization using pie charts, word clouds, and more.

## Features

🌟 **Scrapes User Agent Data:**
Scrapes user agent data from a URL and stores it in dictionaries.

🔍 **Filters and Organizes:**
Filters and organizes user agents based on conditions.

📊 **Provides Statistics:**
Provides statistics about general and mobile user agents.

📈 **Data Visualization:**
Offers options for data visualization, including:
- Pie charts for user agent groups.
- Word clouds for user agent group names.

💾 **Save Charts and Data:**
Allows users to save generated charts and data to a local directory.

🎈 **Easy-to-Use Interface:**
An easy-to-use command-line interface.

## How to Use

[![Watch the video](video_thumbnail.png)](video_link)

1. **Installation:**
   Clone this repository to your local machine.

2. **Setup:**
   Install the required libraries using the following command:
   
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the Script:**
   Open a terminal and navigate to the project directory. Run the script using the following command:

   ```bash
   python User-Agent-Dict.py
   ```

Follows the Prompts: The script will prompt you to interactively choose from various options, such as viewing pie charts, generating word clouds, and more.

Data Visualization: The script generates various types of charts and visualizations to analyze user agent data.

Saving Charts: Choose to save generated charts and data to a local directory.

## Sample Output

Video Tutorial
Watch the full tutorial on YouTube

## Statistics

**Mobile**

Highest Mobile User Agents
![Highest Mobile User Agents](Charts/Highest%20Mobile%20User-agents.png)

Mobile User Agents < 500
![Mobile User Agents < 500](Charts/Mobile%20User-agents%20less%20than%20500.png)

***General***

Highest General User Agents
![Highest General User Agents](Charts/Highest%20General%20User-agents.png)

General User Agents > 500
![General User Agents > 500](Charts/General%20User-agents%20greater%20than%20500.png)

General User Agents < 500
![General User Agents < 500](Charts/General%20User-agents%20less%20than%20500.png)

## Note
The script may require an internet connection to retrieve data from the specified URL.
If you encounter any issues or have questions, feel free to open an issue in this repository.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
