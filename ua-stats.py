import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#import os

# Color Codes for Printing
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
RESET = "\033[0m"

# Load user agents from the JSON file
json_file_path = "user_agents.json"  # Update the file path to the correct one
try:
    with open(json_file_path, "r") as json_file:
        user_agents = json.load(json_file)
except FileNotFoundError:
    print(f"{RED}[ERROR]{RESET}JSON file '{json_file_path}' not found.")
    exit()

# Count the number of different groups in the JSON file for mobile and general user agents
mobile_group_counts = {}
general_group_counts = {}
for ua in user_agents:
    if ua["Platform"] == "Mobile":
        if ua["group"]:
            mobile_group_counts[ua["group"]] = mobile_group_counts.get(ua["group"], 0) + 1
    else:
        if ua["group"]:
            general_group_counts[ua["group"]] = general_group_counts.get(ua["group"], 0) + 1

def create_labeled_pie_chart(groups, title):
    plt.figure()
    labels = [f"{group} ({count})" for group, count in groups.items()]
    sizes = groups.values()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    
    # Create the legend in the upper left corner with a defined box position
    plt.legend(labels, loc="upper left", bbox_to_anchor=(1, 1))
    
    plt.tight_layout()

# User input for pie charts
while True:
    print("Select an option:")
    print("1. Pie chart for Mobile User Agents (Count < 10)")
    print("2. Pie chart for Mobile User Agents (10 <= Count < 500)")
    print("3. Pie chart for General User Agents (10 <= Count < 50)")
    print("4. Pie chart for General User Agents (50 <= Count < 500)")
    print("5. Pie chart for General User Agents (Count >= 500)")
    print("6. Word Cloud for Mobile User Agent Group Names")
    print("7. Word Cloud for General User Agent Group Names")
    print("8. Exit")
    choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")

    if choice == "1":
        create_labeled_pie_chart({group: count for group, count in mobile_group_counts.items() if count < 10}, "Mobile User Agents (Count < 10)")
        plt.subplots_adjust(bottom=0.1, top=1.0)  # Adjust the layout        
        #plt.savefig(os.path.join(charts_dir, "mobile_pie_chart.png"))
    elif choice == "2":
        create_labeled_pie_chart({group: count for group, count in mobile_group_counts.items() if 10 <= count < 500}, "Mobile User Agents (10 <= Count < 500)")
        #plt.savefig(os.path.join(charts_dir, "mobile_pie_chart_10_to_500.png"))
    elif choice == "3":
        create_labeled_pie_chart({group: count for group, count in general_group_counts.items() if 10 <= count < 50}, "General User Agents (10 <= Count < 50)")
        plt.subplots_adjust(bottom=0.1, top=1.0)  # Adjust the layout
        #plt.savefig(os.path.join(charts_dir, "general_pie_chart_10_to_50.png"))
    elif choice == "4":
        create_labeled_pie_chart({group: count for group, count in general_group_counts.items() if 50 <= count < 500}, "General User Agents (50 <= Count < 500)")
        #plt.savefig(os.path.join(charts_dir, "general_pie_chart_50_to_500.png"))
    elif choice == "5":
        create_labeled_pie_chart({group: count for group, count in general_group_counts.items() if count >= 500}, "General User Agents (Count >= 500)")
        #plt.savefig(os.path.join(charts_dir, "general_pie_chart_500_and_above.png"))
    elif choice == "6":
        # Create a word cloud for mobile user agent group names
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(mobile_group_counts)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Highest Mobile User Agents")
        #plt.savefig(os.path.join(charts_dir, "mobile_wordcloud.png"))
    elif choice == "7":
        # Create a word cloud for general user agent group names
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(general_group_counts)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Highest General User Agents")
        #plt.savefig(os.path.join(charts_dir, "general_wordcloud.png"))
    elif choice == "8":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a valid choice.")
# Display the selected pie chart
    plt.show()