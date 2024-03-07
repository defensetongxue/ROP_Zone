import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from matplotlib.font_manager import FontManager, FontProperties

# Path to your Arial.ttf font file
arial_font_path = './arial.ttf'  # Update this to the path where Arial.ttf is located on your system

# Load your custom font
custom_font = FontProperties(fname=arial_font_path)

# Set the font globally for all text elements where possible
plt.rcParams['font.family'] = custom_font.get_name()
plt.rcParams['font.size'] = 12

# Load data
with open('./experiments/zone_list.json', 'r') as f:
    zone_list = json.load(f)

# Prepare data for plotting
data = {'Zone': [], 'Angle': []}
for zone, angles in zone_list.items():
    data['Zone'].extend([f"Zone {zone}"] * len(angles))
    data['Angle'].extend(angles)

df = pd.DataFrame(data)

# Define colors, normalized to [0, 1]
colors = [
    (51/255, 57/255, 91/255),  # RGB for Zone 1
    (93/255, 116/255, 162/255),  # RGB for Zone 2
    (196/255, 216/255, 242/255)  # RGB for Zone 3
]

# Set the color palette in seaborn
palette = sns.color_palette(colors)

# Violin Plot
plt.figure(figsize=(8, 6))
ax = sns.violinplot(x='Zone', y='Angle', data=df, palette=palette)

# After creating the plot, set font properties for plot elements
ax.set_xlabel(ax.get_xlabel(), fontsize=12, fontproperties=custom_font)
ax.set_ylabel(ax.get_ylabel(), fontsize=12, fontproperties=custom_font)

# Set the font size for the tick labels
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontproperties(custom_font)

plt.savefig('./experiments/violin.png', dpi=300)
plt.close()
