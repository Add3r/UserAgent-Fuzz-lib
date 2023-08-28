import requests
from bs4 import BeautifulSoup
import json
import os

# Color Codes for Printing
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
RESET = "\033[0m"

url = "https://www.useragentstring.com/pages/useragentstring.php?name=All"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if there's an HTTP error
    soup = BeautifulSoup(response.content, 'html.parser')

    user_agents = []  # List to store user agent dictionaries
    group = None  # Initialize group value
    sequence = 0  # Initialize sequence value
    seen_combinations = set()  # Set to store seen combinations of user-agent and title
    mobile_detected = False  # Flag to indicate if mobile user agent has been detected

    for tag in soup.find_all(True):
        if tag.name == 'h3':
            group_text = tag.get_text(strip=True)  # Get the text from <h3>
            if group_text == "MOBILE BROWSERS":
                host = "Mobile"
            else:
                host = "General"
            group = group_text  # Update group value
            
        elif tag.name == 'h4':
            title = tag.get_text(strip=True)  # Get the text from <h4> as the title
            
            ul_tag = tag.find_next('ul')  # Find the <ul> under <h4>
            a_tags = ul_tag.find_all('a')  # Find all <a> tags within the <ul>
            
            for a_tag in a_tags:
                href = a_tag['href']  # Get the 'href' attribute value
                user_agent = a_tag.text  # Get the text within the <a> tag
                
                user_agent = user_agent.replace("-->>", "")  # Remove "-->>" if present
                
                if "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" in user_agent:
                    continue  # Skip this iteration if the condition is met
                
                host = "Mobile" if mobile_detected else "General"  # Set the "Host" value
                
                # Check if the combination of user-agent and title has been seen before
                if (user_agent, title) in seen_combinations:
                    continue  # Skip this iteration if the combination has been seen
                
                sequence += 1  # Increment the sequence value
                
                ua_dict = {
                    "title": title if title != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                    "group": group if group != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                    "id": f"ua-{sequence}",
                    "user-agent": user_agent if user_agent != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                    "Host": host
                }
                
                # Check if "Xenu Link Sleuth/1.3.7" is in the user agent
                if "Xenu Link Sleuth/1.3.7" in user_agent:
                    mobile_detected = True
    
                user_agents.append(ua_dict)
                seen_combinations.add((user_agent, title))  # Add the combination to the set
    
    # Prompt the user whether to print the data on the screen
    while True:
        print_data = input("Do you want to print the data on the screen? (yes/no): ").lower()
        if print_data in ["yes", "no"]:
            break
        else:
            print(f"{RED}[ERROR]{RESET} Please enter 'yes' or 'no.'")

    if print_data == "yes":
        # Print the user agent dictionaries in a pretty format
        print(json.dumps(user_agents, indent=4))
    else:
        print("Data was not printed on the screen.")
    
    # Count the total number of user-agents before updating
    total_user_agents_before = len(user_agents)
    
    # Prompt the user whether to update the JSON file
    while True:
        update_json = input("Do you want to update the JSON file? (yes/no): ").lower()
        if update_json in ["yes", "no"]:
            break
        else:
            print(f"{RED}[ERROR]{RESET} Please enter 'yes' or 'no.'")
    
    # Calculate statistics for user agents per "Mobile" and "General" host values
    mobile_user_agents = sum(1 for ua in user_agents if ua["Host"] == "Mobile")
    general_user_agents = sum(1 for ua in user_agents if ua["Host"] == "General")

    # Count the total number of user-agents after updating
    total_user_agents_after = len(user_agents)
    
    print(GREEN + "[+]" + RESET + " General User Agents: " + BLUE + str(general_user_agents) + RESET)
    print(GREEN + "[+]" + RESET + " Mobile User Agents: " + BLUE + str(mobile_user_agents) + RESET)
    print(GREEN + "[+]" + RESET + " Total User Agents: " + BLUE + str(total_user_agents_after) + RESET)
    
    if update_json == "yes":
        json_file_path = "user_agents.json"  # Updated to use default working directory
        
        try:
            # Save the user agent dictionaries to the JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(user_agents, json_file, indent=4)
                print(GREEN + "[+]" + RESET +" JSON file updated successfully.")
            
            # Check if new user agents were identified
            if total_user_agents_after > total_user_agents_before:
                new_user_agents = user_agents[total_user_agents_before:]
                print(GREEN + '[+]' + RESET + " New User Agents Identified: " + BLUE + str(len(new_user_agents)) + RESET)
                for ua in new_user_agents:
                    print(json.dumps(ua, indent=4))
                
                input("Press Enter to acknowledge...")
            else:
                print(f"{YELLOW}[!]{RESET} No new user-agents found.")
            
        except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
            print(f"{RED}[ERROR]{RESET} Error while updating JSON file:", e)
    else:
        print(RED + "[x]" + RESET + " JSON file was not updated.")
        
except requests.exceptions.RequestException as e:
    print(f"{RED}[ERROR]{RESET} Unable to retrieve data from the URL.")
except (AttributeError, ValueError, BeautifulSoup.exceptions.BeautifulSoupError) as e:
    print(f"{RED}[ERROR]{RESET} Error while parsing HTML:", e)
except ValueError as e:
    print(f"{RED}[ERROR]{RESET} Invalid input:", e)
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")