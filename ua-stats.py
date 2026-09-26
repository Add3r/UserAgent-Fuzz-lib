"""Interactive summaries and charts for the combined user_agents.json library."""

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from wordcloud import WordCloud


DATA_FILE = Path("user_agents.json")

try:
    with DATA_FILE.open(encoding="utf-8") as source:
        user_agents = json.load(source)
except (OSError, json.JSONDecodeError) as error:
    raise SystemExit(f"[ERROR] Could not read {DATA_FILE}: {error}")

if not isinstance(user_agents, list):
    raise SystemExit(f"[ERROR] {DATA_FILE} must contain a JSON array.")


def counts_for(platform):
    return Counter(
        record.get("group") or record.get("title") or "Unknown"
        for record in user_agents
        if isinstance(record, dict) and record.get("platform") == platform
    )


mobile_counts = counts_for("Mobile")
general_counts = counts_for("General")
ai_title_counts = Counter(
    record.get("title") or "Unknown"
    for record in user_agents
    if isinstance(record, dict) and record.get("platform") == "AI"
)
ai_variants_per_bot = Counter(ai_title_counts.values())
platform_counts = Counter(
    record.get("platform", "Unknown")
    for record in user_agents
    if isinstance(record, dict)
)


def create_pie_chart(counts, title):
    if not counts:
        print("No data matches this chart.")
        return
    labels = [f"{name} ({count})" for name, count in counts.items()]
    plt.figure(figsize=(11, 7))
    plt.pie(counts.values(), labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.legend(labels, loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()


def create_word_cloud(counts, title):
    if not counts:
        print("No data matches this word cloud.")
        return
    cloud = WordCloud(width=1000, height=500, background_color="white")
    cloud.generate_from_frequencies(counts)
    plt.figure(figsize=(12, 6))
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def create_ai_bot_chart():
    if not ai_title_counts:
        print("No AI records are available.")
        return
    top_bots = ai_title_counts.most_common(20)
    names, counts = zip(*reversed(top_bots))
    plt.figure(figsize=(11, 8))
    plt.barh(names, counts, color="#4c956c")
    plt.xlabel("HTTP User-Agent values listed by Radar")
    plt.title("AI Bots with the Most Radar Header Variants")
    plt.tight_layout()
    plt.show()


def create_ai_title_chart():
    if not ai_title_counts:
        print("No AI records are available.")
        return
    rows = sorted(ai_title_counts.items(), key=lambda item: (item[1], item[0]))
    titles, counts = zip(*rows)
    figure, axis = plt.subplots(figsize=(12, max(12, len(titles) * 0.25)))
    colors = ["#4c956c" if count == 1 else "#e09f3e" if count == 2 else "#c44536"
              for count in counts]
    bars = axis.barh(titles, counts, color=colors, height=0.72)
    axis.set_xlabel("Number of AI User-Agent records", labelpad=10)
    axis.set_title("All AI User-Agent Records by Title", loc="left", fontsize=17,
                   fontweight="bold", pad=18)
    axis.text(0, 1.005, f"{sum(counts)} records across {len(titles)} titles",
              transform=axis.transAxes, fontsize=10, color="#555", va="bottom")
    axis.set_xticks(range(max(counts) + 1))
    axis.set_xlim(0, max(counts) + 0.8)
    axis.tick_params(axis="y", labelsize=8.5, length=0)
    axis.grid(axis="x", alpha=0.22)
    axis.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        axis.spines[spine].set_visible(False)
    axis.bar_label(bars, padding=4, fontsize=8, fontweight="bold")
    figure.tight_layout()
    plt.show()


def create_platform_chart():
    labels = [f"{platform} ({count})" for platform, count in platform_counts.items()]
    plt.figure(figsize=(8, 6))
    plt.pie(platform_counts.values(), labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("User-Agent Records by Platform")
    plt.tight_layout()
    plt.show()


def main():
    menu = {
        "1": ("Mobile groups (count < 10)", lambda: create_pie_chart(
            {key: value for key, value in mobile_counts.items() if value < 10}, "Mobile User Agents (Count < 10)")),
        "2": ("Mobile groups (10 <= count < 500)", lambda: create_pie_chart(
            {key: value for key, value in mobile_counts.items() if 10 <= value < 500}, "Mobile User Agents (10 to 499)")),
        "3": ("General groups (10 <= count < 50)", lambda: create_pie_chart(
            {key: value for key, value in general_counts.items() if 10 <= value < 50}, "General User Agents (10 to 49)")),
        "4": ("General groups (50 <= count < 500)", lambda: create_pie_chart(
            {key: value for key, value in general_counts.items() if 50 <= value < 500}, "General User Agents (50 to 499)")),
        "5": ("General groups (count >= 500)", lambda: create_pie_chart(
            {key: value for key, value in general_counts.items() if value >= 500}, "General User Agents (500+)")),
        "6": ("Mobile group word cloud", lambda: create_word_cloud(mobile_counts, "Highest Mobile User Agents")),
        "7": ("General group word cloud", lambda: create_word_cloud(general_counts, "Highest General User Agents")),
        "8": ("AI bots with most header variants", create_ai_bot_chart),
        "9": ("AI bot name word cloud", lambda: create_word_cloud(ai_title_counts, "AI Agents by User-Agent Variants")),
        "10": ("All platforms", create_platform_chart),
        "11": ("AI bots by number of header variants", lambda: create_pie_chart(
            {f"{number} header value{'s' if number != 1 else ''} per bot": count
             for number, count in sorted(ai_variants_per_bot.items())},
            "AI Bots by Number of Radar Header Variants")),
        "12": ("All AI User-Agent titles by record count", create_ai_title_chart),
        "13": ("Exit", None),
    }
    while True:
        print("\nSelect an option:")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        choice = input("Enter your choice (1-13): ").strip()
        if choice == "13":
            print("Exiting the program.")
            return
        if choice not in menu:
            print("Invalid choice. Please enter a number from 1 to 13.")
            continue
        menu[choice][1]()


if __name__ == "__main__":
    main()
