# Rainfall Project
# Bhav, Devan, Dhruva, Sid
# CMP131
# 12/18/2024
# Mrs. Arakelian







import csv
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import pandas as pd
import numpy as np
from scipy.stats import linregress

# Paths to the CSV files
crash_file_path = "countycrashes.csv"
south_rain_file = "southrain.csv"
north_rain_file = "northrain.csv"
coast_rain_file = "coastrain.csv"

# Load rainfall data
def load_rainfall_data(file_path, start_year=2001, end_year=2022):
    data = pd.read_csv(file_path)
    data = data[['Year', 'Annual']].copy()
    data['Annual'] = pd.to_numeric(data['Annual'], errors='coerce')
    filtered_data = data[data['Year'].between(start_year, end_year)].reset_index(drop=True)
    return filtered_data['Year'].tolist(), filtered_data['Annual'].tolist()

# Load rainfall data for all regions
years, south_rainfall = load_rainfall_data(south_rain_file)
_, north_rainfall = load_rainfall_data(north_rain_file)
_, coast_rainfall = load_rainfall_data(coast_rain_file)

# Initialize the dictionary for crashes
county_data = {}

# Read the crash CSV file and populate the dictionary
with open(crash_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        year = int(row["Year"])
        for county, deaths in row.items():
            if county != "Year":  # Skip the Year column
                if county not in county_data:
                    county_data[county] = []
                county_data[county].append((year, int(deaths)))

# Define regions
north_counties = [
    "Bergen", "Essex", "Hudson", "Hunterdon", "Morris",
    "Passaic", "Somerset", "Sussex", "Union", "Warren"
]
south_counties = [
    "Burlington", "Camden", "Cape May", "Cumberland",
    "Gloucester", "Mercer", "Middlesex", "Salem"
]
coast_counties = ["Atlantic", "Ocean", "Monmouth"]

# Helper functions to calculate totals and averages
def calculate_totals(region_counties):
    totals = {}
    for year in range(2001, 2023):
        total = sum([dict(county_data[county])[year] for county in region_counties if year in dict(county_data[county])])
        totals[year] = total
    return totals

def calculate_averages(region_counties):
    averages = {}
    for year in range(2001, 2023):
        valid_data = [dict(county_data[county])[year] for county in region_counties if year in dict(county_data[county])]
        averages[year] = sum(valid_data) / len(valid_data) if valid_data else 0
    return averages

# Calculate totals and averages for crashes and rainfall
north_crash_totals = calculate_totals(north_counties)
south_crash_totals = calculate_totals(south_counties)
coast_crash_totals = calculate_totals(coast_counties)

north_crash_averages = calculate_averages(north_counties)
south_crash_averages = calculate_averages(south_counties)
coast_crash_averages = calculate_averages(coast_counties)

north_rain_totals = sum(north_rainfall)
south_rain_totals = sum(south_rainfall)
coast_rain_totals = sum(coast_rainfall)

north_rain_averages = np.mean(north_rainfall)
south_rain_averages = np.mean(south_rainfall)
coast_rain_averages = np.mean(coast_rainfall)

# Function to create interactive plots
def plot_with_checkboxes(data, title):
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(left=0.3)

    # Plot data
    lines = {}
    labels = list(data.keys())
    for label in labels:
        line, = ax.plot(years, data[label], label=label)
        lines[label] = line

    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(title)
    ax.legend()
    plt.grid(True)

    # Add checkboxes
    rax = plt.axes([0.05, 0.4, 0.2, 0.5])
    check = CheckButtons(rax, labels, [True] * len(labels))

    def toggle_visibility(label):
        lines[label].set_visible(not lines[label].get_visible())
        plt.draw()

    check.on_clicked(toggle_visibility)
    plt.show()

# Correlation plots
def plot_correlation(data_1, data_2, labels, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(left=0.3)

    lines = {}
    for label, (x_data, y_data) in zip(labels, zip(data_1, data_2)):
        scatter, = ax.plot(x_data, y_data, 'o', label=f"{label} Data")
        slope, intercept, _, _, _ = linregress(x_data, y_data)
        regression_line, = ax.plot(x_data, [slope * x + intercept for x in x_data], linestyle="--", label=f"{label} Regression Line")
        lines[f"{label} Data"] = scatter
        lines[f"{label} Regression Line"] = regression_line

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.grid(True)

    # Add checkboxes
    rax = plt.axes([0.05, 0.4, 0.2, 0.5])
    check = CheckButtons(rax, list(lines.keys()), [True] * len(lines))

    def toggle_visibility(label):
        lines[label].set_visible(not lines[label].get_visible())
        plt.draw()

    check.on_clicked(toggle_visibility)
    plt.show()

# Prepare data for totals and averages
totals_data = {
    "North Crash Totals": list(north_crash_totals.values()),
    "South Crash Totals": list(south_crash_totals.values()),
    "Coast Crash Totals": list(coast_crash_totals.values())
}

averages_data = {
    "North Crash Averages": list(north_crash_averages.values()),
    "South Crash Averages": list(south_crash_averages.values()),
    "Coast Crash Averages": list(coast_crash_averages.values())
}

# Generate plots
plot_with_checkboxes(totals_data, "Crash Totals by Region with Rainfall")
plot_with_checkboxes(averages_data, "Crash Averages by Region with Rainfall")

# Correlation plots for totals and averages
plot_correlation(
    [list(north_rainfall), list(south_rainfall), list(coast_rainfall)],
    [list(north_crash_totals.values()), list(south_crash_totals.values()), list(coast_crash_totals.values())],
    ["North", "South", "Coast"],
    "Correlation Between Rainfall Totals and Crash Totals",
    "Rainfall (inches)", "Crash Totals"
)

plot_correlation(
    [list(north_rainfall), list(south_rainfall), list(coast_rainfall)],
    [list(north_crash_averages.values()), list(south_crash_averages.values()), list(coast_crash_averages.values())],
    ["North", "South", "Coast"],
    "Correlation Between Rainfall Averages and Crash Averages",
    "Rainfall (inches)", "Crash Averages"
)
