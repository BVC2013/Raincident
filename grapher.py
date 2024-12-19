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

# Helper function to calculate sums
def calculate_sum(region_counties):
    sums = {}
    for year in range(2001, 2023):
        total = sum([dict(county_data[county])[year] for county in region_counties if year in dict(county_data[county])])
        sums[year] = total
    return sums

# Calculate crash totals for regions
north_sum = calculate_sum(north_counties)
south_sum = calculate_sum(south_counties)
coast_sum = calculate_sum(coast_counties)

# Extract years and totals for plotting
north_crash_totals = list(north_sum.values())
south_crash_totals = list(south_sum.values())
coast_crash_totals = list(coast_sum.values())
statewide_crash_totals = [
    sum(x) for x in zip(north_crash_totals, south_crash_totals, coast_crash_totals)
]

# Calculate total rainfall for the state
statewide_rainfall = [
    sum(x) for x in zip(north_rainfall, south_rainfall, coast_rainfall)
]

# Function to add interactive checkboxes
def plot_with_checkboxes():
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(left=0.3)

    # Plot data
    lines = {}
    labels = [
        "North Rainfall", "South Rainfall", "Coast Rainfall", "Statewide Rainfall",
        "North Crashes", "South Crashes", "Coast Crashes", "Statewide Crashes"
    ]
    datasets = [
        north_rainfall, south_rainfall, coast_rainfall, statewide_rainfall,
        north_crash_totals, south_crash_totals, coast_crash_totals, statewide_crash_totals
    ]
    colors = ["red", "green", "orange", "blue", "red", "green", "orange", "blue"]
    linestyles = ["--", "--", "--", "-", "-", "-", "-", "-"]

    for label, data, color, linestyle in zip(labels, datasets, colors, linestyles):
        line, = ax.plot(years, data, label=label, color=color, linestyle=linestyle)
        lines[label] = line

    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title("Rainfall and Crashes Over Years")
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

# Correlation between North, South, Coast crashes and annual rainfall
def plot_crash_rainfall_correlation():
    plt.figure(figsize=(14, 8))
    regions = {
        "North": (north_crash_totals, north_rainfall, "red"),
        "South": (south_crash_totals, south_rainfall, "green"),
        "Coast": (coast_crash_totals, coast_rainfall, "orange"),
    }

    for region, (crash_data, rainfall_data, color) in regions.items():
        # Scatter points
        plt.scatter(rainfall_data, crash_data, label=f"{region} Crashes vs Rainfall", color=color, alpha=0.7)
        # Regression line
        slope, intercept, _, _, _ = linregress(rainfall_data, crash_data)
        regression_line = [slope * x + intercept for x in rainfall_data]
        plt.plot(rainfall_data, regression_line, linestyle="--", color=color, label=f"{region} Regression Line")

    plt.xlabel("Rainfall (inches)")
    plt.ylabel("Crash Totals")
    plt.title("Correlation Between Rainfall and Crashes by Region")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Generate graphs
plot_with_checkboxes()
plot_crash_rainfall_correlation()
