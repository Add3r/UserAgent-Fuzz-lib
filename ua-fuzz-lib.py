import requests
from bs4 import BeautifulSoup
import json

# Color Codes for Printing
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
RESET = "\033[0m"

class UserAgentFuzzLib:
    def __init__(self):
        self.url = "https://www.useragentstring.com/pages/useragentstring.php?name=All"
        self.user_agents = []
        self.sequence = 0
        self.seen_combinations = set()
        self.mobile_detected = False

    def parse_user_agents(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception if there's an HTTP error
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in soup.find_all(True):
                if tag.name == 'h3':
                    group_text = tag.get_text(strip=True)
                    if group_text == "MOBILE BROWSERS":
                        host = "Mobile"
                    else:
                        host = "General"
                    group = group_text
            
                elif tag.name == 'h4':
                    title = tag.get_text(strip=True)
            
                    ul_tag = tag.find_next('ul')
                    a_tags = ul_tag.find_all('a')
            
                    for a_tag in a_tags:
                        href = a_tag['href']
                        user_agent = a_tag.text
                        user_agent = user_agent.replace("-->>", "")

                        if user_agent.startswith("More"):
                            continue

                        if "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" in user_agent:
                            continue
                
                        host = "Mobile" if self.mobile_detected else "General"
                
                        if (user_agent, title) in self.seen_combinations:
                            continue
                
                        self.sequence += 1
                        ua_dict = {
                            "title": title if title != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                            "group": group if group != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                            "id": f"ua-{self.sequence}",
                            "user-agent": user_agent if user_agent != "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" else "",
                            "platform": host
                        }
                
                        if "Xenu Link Sleuth/1.3.7" in user_agent:
                            self.mobile_detected = True
            
                        self.user_agents.append(ua_dict)
                        self.seen_combinations.add((user_agent, title))
        
        except requests.exceptions.RequestException as e:
            print(f"{RED}[ERROR]{RESET} Unable to retrieve data from the URL.")
        except (AttributeError, ValueError, BeautifulSoup.exceptions.BeautifulSoupError) as e:
            print(f"{RED}[ERROR]{RESET} Error while parsing HTML:", e)
        except KeyboardInterrupt:
            print(f"\n{RED}[ERROR]{RESET} Program interrupted by user.")
            exit(1)

    def print_user_agents(self):
        try:
            while True:
                print_data = input("Do you want to print the data on the screen? (yes/no): ").lower()
                if print_data in ["yes", "no"]:
                    break
                else:
                    print(f"{RED}[ERROR]{RESET} Please enter 'yes' or 'no.'")

            if print_data == "yes":
                print(json.dumps(self.user_agents, indent=4))
            else:
                print(f"{YELLOW}[!]{RESET} Data was not printed on the screen.")
        except KeyboardInterrupt:
            print(f"\n{RED}[ERROR]{RESET} Program interrupted by user.")
            exit(1)

    def update_json_file(self):
        try:
            while True:
                update_json = input("Do you want to update the JSON file? (yes/no): ").lower()
                if update_json in ["yes", "no"]:
                    break
                else:
                    print(f"{RED}[ERROR]{RESET} Please enter 'yes' or 'no.'")

            if update_json == "yes":
                json_file_path = "user_agents.json"
            
                try:
                    with open(json_file_path, "w") as json_file:
                        json.dump(self.user_agents, json_file, indent=4)
                        print(GREEN + "[+]" + RESET + " JSON file updated successfully.")
                
                    self.print_new_user_agents()  
                
                except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
                    print(f"{RED}[ERROR]{RESET} Error while updating JSON file:", e)
            else:  
                print(RED + "[x]" + RESET + " JSON file was not updated.")
                self.print_new_user_agents()

        except KeyboardInterrupt:
            print(f"\n{RED}[ERROR]{RESET} Program interrupted by user.")
            exit(1)
    
    # Method to check if new user agents found
    def print_new_user_agents(self):
        total_user_agents_before = len(self.user_agents)
                
        if len(self.user_agents) > total_user_agents_before:
            new_user_agents = self.user_agents[total_user_agents_before:]
            print(GREEN + '[+]' + RESET + " New User Agents Identified: " + BLUE + str(len(new_user_agents)) + RESET)
            for ua in new_user_agents:
                ua_dict = {
                    "title": ua[0],
                    "group": ua[1],
                    "id": ua[2],
                    "user-agent": ua[3],
                    "platform": ua[4]
                }
                print(json.dumps(ua_dict, indent=4))
                    
            input("Press Enter to acknowledge...")
        else:
            print(f"{YELLOW}[!]{RESET} No new user-agents found.")

    def print_updates(self):
        try:
            mobile_user_agents = sum(1 for ua in self.user_agents if ua["platform"] == "Mobile")
            general_user_agents = sum(1 for ua in self.user_agents if ua["platform"] == "General")
            total_user_agents_after = len(self.user_agents)

            print(GREEN + "[+]" + RESET + " General User Agents: " + BLUE + str(general_user_agents) + RESET)
            print(GREEN + "[+]" + RESET + " Mobile User Agents: " + BLUE + str(mobile_user_agents) + RESET)
            print(GREEN + "[+]" + RESET + " Total User Agents: " + BLUE + str(total_user_agents_after) + RESET)
        except KeyboardInterrupt:
            print(f"\n{RED}[ERROR]{RESET} Program interrupted by user.")
            exit(1)
    
if __name__ == "__main__":
    fuzzlib = UserAgentFuzzLib()
    fuzzlib.parse_user_agents()
    fuzzlib.print_user_agents()
    fuzzlib.update_json_file()
    fuzzlib.print_updates()
