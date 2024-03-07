import os,json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from matplotlib.font_manager import FontManager, FontProperties

with open('./experiments/zone_list.json') as f:
    zone_list=json.load(f)
class judge:
    def __init__(self,a,b) -> None:
        self.a=a
        self.b=b
    def set(self,a,b):
        self.a=a 
        self.b=b 
    def __call__(self, angle):
        if angle < self.a:
            pred = 1
        elif self.a <= angle < self.b:
            pred = 2
        else:
            pred = 3
        return pred
handler=judge(47,79)
label_list=[]
pred_list=[]
for zone in zone_list:
    for angle in zone_list[zone]:
        pred_list.append(int(handler(angle)))
        label_list.append(int(zone))
        
        
# Calculate Accuracy
accuracy = accuracy_score(label_list, pred_list)
print(f'Accuracy: {accuracy}')

# Calculate Precision, Recall, and F1-score for each class
precision = precision_score(label_list, pred_list, average=None)
recall = recall_score(label_list, pred_list, average=None)
f1 = f1_score(label_list, pred_list, average=None)

# Print the results
print(f'Precision for each class: {precision}') # class number is 3
print(f'Recall for each class: {recall}')
print(f'F1-score for each class: {f1}')