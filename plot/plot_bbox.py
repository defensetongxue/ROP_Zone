import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import json,os
# Example data
with open('../autodl-tmp/dataset_ROP/annotations.json', 'r') as f:
    data_dict = json.load(f)
    
# Bin width
zone_list={
    1:[],
    2:[],
    3:[]
}
angle_add={
    'visible':0,
    'near':19,
    'far':39
}
for image_name in data_dict:
    data=data_dict[image_name]
    if isinstance(data,int):
        print(image_name,data)
        continue
    if 'zone_pred' not in data or data['zone'] <= 0:
                continue
    if 'ridge_seg' not in data or "ridge_seg_path" not in data['ridge_seg']:
        continue
    distance = data['optic_disc_pred']["distance"]
    angle=data['zone_pred']["min_angle"]+angle_add[distance]
    zone_list[data['zone']].append(angle)
def remove_outliers(data):
    q25, q75 = np.percentile(data, [25, 75])
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]
    return filtered_data

# Apply the outlier removal function to each zone list
for zone in zone_list:
    zone_list[zone] = remove_outliers(zone_list[zone])

bin_width = 2.5
bins = np.arange(30, 100, bin_width)  # Extend to 125 to ensure the last bin is included

def normalize_hist(hist, bins):
    bin_width = np.diff(bins)
    normalized_hist = hist / sum(hist * bin_width)  # Normalize by the area under the histogram
    return normalized_hist

# Histogram data
hist1, _ = np.histogram(zone_list[1], bins)
hist2, _ = np.histogram(zone_list[2], bins)
hist3, _ = np.histogram(zone_list[3], bins)

# Normalize histograms
hist1 = normalize_hist(hist1, bins)
hist2 = normalize_hist(hist2, bins)
hist3 = normalize_hist(hist3, bins)

# Midpoints of bins for plotting
bin_midpoints = bins[:-1] + bin_width / 2

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(bin_midpoints - bin_width/3, hist1, width=bin_width/3, color='red', label='Zone 1')
ax.bar(bin_midpoints, hist2, width=bin_width/3, color='yellow', label='Zone 2')
ax.bar(bin_midpoints + bin_width/3, hist3, width=bin_width/3, color='green', label='Zone 3')

font_path = './arial.ttf'
font_prop = FontProperties(fname=font_path, size=24)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontproperties(font_prop)

ax.set_xlabel('Angle', fontproperties=font_prop)
ax.set_ylabel('Frequency', fontproperties=font_prop)
ax.legend(prop=font_prop)

plt.savefig('./experiments/bar_plot.png')
plt.close(fig)

# Function to filter out zero-height bins and their midpoints
def filter_zeros(hist, midpoints):
    non_zero_indices = np.where(hist > 0)  # Find indices where histogram is non-zero
    filtered_midpoints = midpoints[non_zero_indices]
    filtered_hist = hist[non_zero_indices]
    return filtered_midpoints, filtered_hist

# Filtered data for plotting
filtered_midpoints1, filtered_hist1 = filter_zeros(hist1, bin_midpoints)
filtered_midpoints2, filtered_hist2 = filter_zeros(hist2, bin_midpoints)
filtered_midpoints3, filtered_hist3 = filter_zeros(hist3, bin_midpoints)

# Plotting setup
font_path = './arial.ttf'  # Ensure this path is correct for your environment
font_prop = FontProperties(fname=font_path, size=24)

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting only non-zero bins as line chart
ax.plot(filtered_midpoints1, filtered_hist1, color='red', label='Zone 1')
ax.plot(filtered_midpoints2, filtered_hist2, color='yellow', label='Zone 2')
ax.plot(filtered_midpoints3, filtered_hist3, color='green', label='Zone 3')

# Fill the area under the line with color
ax.fill_between(filtered_midpoints1, 0, filtered_hist1, color='red', alpha=0.3)
ax.fill_between(filtered_midpoints2, 0, filtered_hist2, color='yellow', alpha=0.3)
ax.fill_between(filtered_midpoints3, 0, filtered_hist3, color='green', alpha=0.3)

# Customize the plot with labels, title, and legend
ax.set_xlabel('Angle', fontproperties=font_prop)
ax.set_ylabel('Normalized Frequency', fontproperties=font_prop)
ax.legend(prop=font_prop)

# Save the plot
plt.savefig('./experiments/line_chart_filtered.png')
plt.close(fig)