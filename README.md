<p align="center">
  <img src="images/user-agent-dict-logo.png" alt="User Agent Dictionary Logo">
</p>

<div align="center">

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Add3r/UserAgent-Parser)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://github.com/Add3r/UserAgent-Parser/blob/main/LICENSE)
[![Awesome](https://img.shields.io/badge/Awesome-%F0%9F%98%8E-blueviolet.svg)](https://shields.io/)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)
[![Support](https://img.shields.io/static/v1?label=Support&message=Ko-fi&color=ff5e5b&logo=ko-fi)](https://ko-fi.com/add3r)

![Repository Views](https://komarev.com/ghpvc/?username=Add3r&label=Repository+Views)
![Python](https://img.shields.io/badge/Python-3.11.5-blue.svg)
![Total User-Agents Archived](https://img.shields.io/badge/Total%20User--Agents%20Archived-11256-blue.svg)
![Mobile User-Agents](https://img.shields.io/badge/Mobile%20User--Agents-629-orange.svg)
![General User-Agents](https://img.shields.io/badge/General%20User--Agents-10627-green.svg)

</div>

# UserAgent Fuzzing-Library

This repository holds data of all the user agents in the `user_agents.json` file, which can be used directly with any tool that can parse json format.

download the repo to update the user-agent data by running `User-Agent-Dict.py` and edit the file per the fields you would like to add or remove.

Major intention for creating this dictionary of useragents was to feed it to Proxy_Bypass vulnerability research tool(under development in private repo) to use the `user-agents.json` file as input for fuzzing proxies.

As a PoC have provided the `ua-stats.py` script which draw various statistics out of the `user-agents.json` file as input

## Overview

🎯 **Primary:**
- The User Agent Dict python script is designed to scrape from [useragentstring.com](https://www.useragentstring.com/pages/All/)
- To use as Fuzzing library of user-agents used for vulnerability research tools
- Organize the data into dictionaries, for faster access (mimicing hashmaps)

🚀 **Secondary:**
- Identify user agent groups based on specified conditions.
   - High used vs low used user-agents to choose for fuzzing
- Display statistics about general and mobile user agents.
- Provide options for data visualization using pie charts, word clouds, and more.

## How to Use

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
   python3 User-Agent-Dict.py
   ```

## Sample Output
   
   ***If you would like to print on screen***
   ```
   > python3 User-Agent-Dict.py
   Do you want to print the data on the screen? (yes/no): yes
   
   [
    {
        "title": "ABrowse 0.6",
        "group": "ABrowse",
        "id": "ua-1",
        "user-agent": "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
        "Host": "General"
    },
   .
   .
   .
   (output Truncated)
   .
   .
    {
        "title": "WDG_Validator 1.6.2",
        "group": "WDG_Validator",
        "id": "ua-11256",
        "user-agent": "WDG_Validator/1.6.2",
        "Host": "Mobile"
    }
   ]
   ```
   ***If you would like to update the `user_agents.json` file***
   <pre>
   <code>
   Do you want to update the JSON file? (yes/no): yes
   <span style="color: green;">[+]</span> General User Agents: <span style="color: cyan;">10627</span>
   <span style="color: green;">[+]</span> Mobile User Agents: <span style="color: cyan;">629</span>
   <span style="color: green;">[+]</span> Total User Agents: <span style="color: cyan;">11256</span>
   <span style="color: green;">[+]</span> JSON file updated successfully.
   <span style="color: yellow;">[!]</span> No new user-agents found.
   </code>
   </pre>
## Statistics

As a PoC, have added a basic statistics deriving script `ua-stats.py` that uses the `user_agents.json` as input file.

`ua-stats.py` script will prompt you to interactively choose from various options, such as viewing pie charts and generating word clouds from the `user_agents.json` data.

## How to Use `ua-stats.py`

1. **Run the Script:**
   Open a terminal and navigate to the project directory. Run the script using the following command:

   ```bash
   python3 ua-stats.py
   ```

## Sample Output

   ```
   > python3 ua-stats.py
   Select an option:
   1. Pie chart for Mobile User Agents (Count < 10)
   2. Pie chart for Mobile User Agents (10 <= Count < 500)
   3. Pie chart for General User Agents (10 <= Count < 50)
   4. Pie chart for General User Agents (50 <= Count < 500)
   5. Pie chart for General User Agents (Count >= 500)
   6. Word Cloud for Mobile User Agent Group Names
   7. Word Cloud for General User Agent Group Names
   8. Exit
   Enter your choice (1/2/3/4/5/6/7/8): 
   ```

This is only a PoC to use of using the json file data, there could be more analysis you could think of with this data. 😀

**Few Samples Below**

**Mobile**

<p align="center">
  <strong>Highest Mobile User Agents</strong><br>
  <img src="Charts/Highest%20Mobile%20User-agents.png" alt="Highest Mobile User Agents">
</p>

<p align="center">
  <strong>Mobile User Agents &lt; 500</strong><br>
  <img src="Charts/Mobile%20User-agents%20less%20than%20500.png" alt="Mobile User Agents < 500">
</p>

**General**

<p align="center">
  <strong>Highest General User Agents</strong><br>
  <img src="Charts/Highest%20General%20User-agents.png" alt="Highest General User Agents">
</p>

<p align="center">
  <strong>General User Agents &gt; 500</strong><br>
  <img src="Charts/General%20User-agents%20greater%20than%20500.png" alt="General User Agents > 500">
</p>

<p align="center">
  <strong>General User Agents &lt; 500</strong><br>
  <img src="Charts/General%20User-agents%20less%20than%20500.png" alt="General User Agents < 500">
</p>

## Note
The script may require an internet connection to retrieve data from the specified URL.
If you encounter any issues or have questions, feel free to open an issue in this repository.

## License
This project is licensed under the GPL 3.0 License - see the LICENSE file for details.
