"""Refresh the combined browser and AI user-agent library."""

import json
import os
import tempfile
from collections import Counter
from pathlib import Path

import requests
from bs4 import BeautifulSoup


GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
RESET = "\033[0m"

JSON_FILE_PATH = Path("user_agents.json")
BROWSER_URL = "https://www.useragentstring.com/pages/useragentstring.php?name=All"
RADAR_BOTS_URL = "https://api.cloudflare.com/client/v4/radar/bots"
AI_CATEGORIES = ("AI_CRAWLER", "AI_ASSISTANT", "AI_SEARCH")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "no"):
            return answer == "yes"
        print(f"{RED}[ERROR]{RESET} Please enter 'yes' or 'no.'")


def fetch_browser_user_agents():
    response = requests.get(BROWSER_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    records = []
    seen = set()
    group = ""
    mobile_detected = False

    for tag in soup.find_all(["h3", "h4"]):
        if tag.name == "h3":
            group = tag.get_text(strip=True)
            continue

        title = tag.get_text(strip=True)
        listing = tag.find_next("ul")
        if listing is None:
            continue
        for anchor in listing.find_all("a"):
            user_agent = anchor.get_text(strip=True).replace("-->>", "")
            if not user_agent or user_agent.startswith("More"):
                continue
            if "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.14912Mod.By.www.9jamusic.cz.cc/22.387; U; en)" in user_agent:
                continue
            key = (user_agent, title)
            if key in seen:
                continue
            seen.add(key)
            platform = "Mobile" if mobile_detected else "General"
            records.append({
                "title": title,
                "group": group,
                "id": f"ua-{len(records) + 1}",
                "user-agent": user_agent,
                "platform": platform,
            })
            if "Xenu Link Sleuth/1.3.7" in user_agent:
                mobile_detected = True

    if not records:
        raise ValueError("The browser source returned no user-agent records.")
    return records


def radar_get(path, token, params=None):
    response = requests.get(
        f"{RADAR_BOTS_URL}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success"):
        raise ValueError("Cloudflare Radar returned an unsuccessful response.")
    return payload.get("result", {})


def list_ai_bots(token):
    bots_by_slug = {}
    for category in AI_CATEGORIES:
        offset = 0
        while True:
            result = radar_get("", token, {
                "botCategory": category,
                "limit": 1000,
                "offset": offset,
                "format": "JSON",
            })
            bots = result.get("bots")
            if not isinstance(bots, list):
                raise ValueError("Cloudflare Radar response is missing its bot list.")
            for bot in bots:
                if not isinstance(bot, dict) or not bot.get("slug"):
                    raise ValueError("Cloudflare Radar returned a bot without a slug.")
                bots_by_slug[bot["slug"]] = bot
            if len(bots) < 1000:
                break
            offset += len(bots)
    if not bots_by_slug:
        raise ValueError("Cloudflare Radar returned no AI bots.")
    return list(bots_by_slug.values())


def is_concrete_user_agent(user_agent):
    """Ignore patterns and placeholders rather than recorded header values."""
    markers = ("*", "[", "]", "W.X.Y.Z", "...")
    return not any(marker in user_agent for marker in markers) and not user_agent.endswith("/")


def fetch_ai_user_agents(token, id_offset):
    records = []
    missing_headers = []
    template_headers = []
    for listed_bot in list_ai_bots(token):
        bot = radar_get(f"/{listed_bot['slug']}", token).get("bot")
        if not isinstance(bot, dict):
            raise ValueError(f"Cloudflare Radar returned no detail for {listed_bot['slug']}.")
        name = bot.get("name", listed_bot.get("name", listed_bot["slug"]))
        user_agents = bot.get("userAgents")
        if not isinstance(user_agents, list) or not user_agents:
            missing_headers.append(name)
            continue
        for user_agent in dict.fromkeys(user_agents):
            if not isinstance(user_agent, str) or not user_agent.strip() or user_agent != user_agent.strip():
                raise ValueError(f"Cloudflare Radar returned an invalid HTTP User-Agent for {name}.")
            if not is_concrete_user_agent(user_agent):
                template_headers.append(name)
                continue
            records.append({
                "title": name,
                "group": "AI-Agents",
                "id": f"ua-{id_offset + len(records) + 1}",
                "user-agent": user_agent,
                "platform": "AI",
            })
    if not records:
        raise ValueError("Cloudflare Radar returned no concrete AI HTTP User-Agent values.")
    return records, missing_headers, template_headers


def load_existing_records():
    try:
        with JSON_FILE_PATH.open(encoding="utf-8") as source:
            records = json.load(source)
        if not isinstance(records, list):
            raise ValueError("user_agents.json must contain a JSON array.")
        return records
    except FileNotFoundError:
        return []


def save_records(records):
    JSON_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=JSON_FILE_PATH.parent,
                                         delete=False) as target:
            temp_path = Path(target.name)
            json.dump(records, target, indent=4, ensure_ascii=False)
            target.write("\n")
        os.replace(temp_path, JSON_FILE_PATH)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


def print_statistics(records):
    counts = Counter(record["platform"] for record in records)
    for platform in ("General", "Mobile", "AI"):
        print(f"{GREEN}[+]{RESET} {platform} User Agents: {BLUE}{counts[platform]}{RESET}")
    print(f"{GREEN}[+]{RESET} Total User Agents: {BLUE}{len(records)}{RESET}")


def main():
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        print(f"{RED}[ERROR]{RESET} Set CLOUDFLARE_API_TOKEN to refresh the combined library.")
        return 1

    try:
        browser_records = fetch_browser_user_agents()
        ai_records, missing, templates = fetch_ai_user_agents(token, len(browser_records))
        records = browser_records + ai_records
        for name in missing:
            print(f"{YELLOW}[!]{RESET} Skipping {name}: Radar has no HTTP User-Agent value.")
        for name in templates:
            print(f"{YELLOW}[!]{RESET} Skipping template User-Agent listed for {name}.")

        if ask_yes_no("Do you want to print the data on the screen? (yes/no): "):
            print(json.dumps(records, indent=4, ensure_ascii=False))
        else:
            print(f"{YELLOW}[!]{RESET} Data was not printed on the screen.")

        previous = load_existing_records()
        old_pairs = {(item.get("platform"), item.get("title"), item.get("user-agent"))
                     for item in previous if isinstance(item, dict)}
        new_records = [item for item in records
                       if (item["platform"], item["title"], item["user-agent"]) not in old_pairs]
        if ask_yes_no("Do you want to update the combined JSON file? (yes/no): "):
            save_records(records)
            print(f"{GREEN}[+]{RESET} user_agents.json updated successfully.")
        else:
            print(f"{RED}[x]{RESET} JSON file was not updated.")
        print(f"{GREEN}[+]{RESET} New User-Agent records: {BLUE}{len(new_records)}{RESET}")
        print_statistics(records)
    except (requests.exceptions.RequestException, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"{RED}[ERROR]{RESET} Unable to update user-agents: {error}")
        return 1
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}[ERROR]{RESET} Program interrupted.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
