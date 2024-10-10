import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.font_manager import FontProperties
import os

# Your metrics and class names (zones)
Precision= [0.65306122, 0.97697842, 0.84605757]
Recall = [0.98461538, 0.8210399, 0.96571429]
f1= [0.78527607, 0.89224704, 0.90193462]
metrics = [Precision, Recall, f1]
metric_names = ['Precision', 'Recall', 'F1-score']
class_names = ['Zone 1', 'Zone 2', 'Zone 3']
colors = [
    (51/255, 57/255, 91/255),
    (93/255, 116/255, 162/255),
    (196/255, 216/255, 242/255)
]

font_prop = FontProperties(fname='./arial.ttf')  # Ensure the path is correct

experiments_dir = './experiments/bar_plot/'

# Ensure the output directory exists
os.makedirs(experiments_dir, exist_ok=True)

# Iterate over each metric to plot
for metric, metric_name in zip(metrics, metric_names):
    fig, ax = plt.subplots(figsize=(4, 5))  # Adjust figure size as needed
    positions = np.arange(len(class_names))
    bar_width = 0.6  # Adjust bar width here

    for i, class_name in enumerate(class_names):
        # Plot metric value for each class
        ax.bar(positions[i], metric[i], bar_width, label=class_name, color=colors[i], align='center')
        ax.text(positions[i], metric[i] + 0.01, f"{metric[i]:.3f}", ha='center', fontproperties=font_prop, fontsize=12)

    ax.set_yticks(np.linspace(0, 1, 5))
    ax.set_yticklabels([f"{tick:.2f}" for tick in np.linspace(0, 1, 5)], fontproperties=font_prop, fontsize=16)

    ax.set_xticks([])  # No x-tick labels
    ax.set_title(f'{metric_name}', fontproperties=font_prop, fontsize=16)  # Adjust fontsize as needed

    plt.tight_layout()
    plt.savefig(os.path.join(experiments_dir, f'{metric_name}_bar_plot.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creating a figure for the legend
fig_legend = plt.figure(figsize=(3, 2))
ax_legend = fig_legend.add_subplot(111)
legend_elements = [Patch(facecolor=colors[i], label=class_names[i]) for i in range(len(class_names))]
legend = ax_legend.legend(handles=legend_elements, loc='center', prop=font_prop)
ax_legend.axis('off')
fig_legend.savefig(os.path.join(experiments_dir, 'legend.png'), dpi=300, bbox_inches='tight')
plt.close(fig_legend)
