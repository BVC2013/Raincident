import matplotlib.pyplot as plt
import numpy as np

# Example data arrays
# Array 1: New Jersey Statewide Monthly Total Precipitation in Inches
rainfall = [3.4, 3.2, 3.1, 4.0, 4.2, 3.6, 4.0, 3.9, 3.5, 3.0, 3.1, 3.4]  # Example monthly rainfall

# Array 2: Fatal Car Crashes Per Year in New Jersey Counties
crashes = [75, 65, 80, 90, 85, 95, 100, 110, 120, 130, 105, 110]  # Example crash data for each month

# Creating x-axis positions
months = np.arange(12)

# Plotting the bar graph
fig, ax1 = plt.subplots(figsize=(10, 6))

# Creating the bar plot for rainfall data (left y-axis)
ax1.bar(months - 0.2, rainfall, width=0.4, color='b', label='Rainfall (inches)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Rainfall (inches)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xticks(months)
ax1.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

# Creating the second y-axis for fatal car crashes
ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis
ax2.bar(months + 0.2, crashes, width=0.4, color='r', label='Fatal Car Crashes')
ax2.set_ylabel('Fatal Car Crashes', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Title and show the plot
plt.title('Monthly Rainfall vs Fatal Car Crashes in New Jersey')
fig.tight_layout()
plt.show()