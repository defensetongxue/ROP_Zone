import json,os
import numpy as np
def remove_outliers(angle_list):
    q1, q3 = np.percentile(angle_list, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return [angle for angle in angle_list if lower_bound <= angle <= upper_bound]


def get_dividing(lower_list, upper_list):
    # Combine and sort the unique values from both lists
    combined = np.unique(lower_list + upper_list)
    combined.sort()
    
    # Initialize variables to store the optimal dividing value and minimum error
    min_error = float('inf')
    dividing_value = combined[0]
    
    # Try every value as a potential threshold and compute errors
    for i in range(len(combined) - 1):
        threshold = (combined[i] + combined[i + 1]) / 2
        lower_errors = sum([1 for x in lower_list if x >= threshold])
        upper_errors = sum([1 for x in upper_list if x < threshold])
        total_error = lower_errors + upper_errors
        
        # Update the dividing value if this threshold results in fewer errors
        if total_error < min_error:
            min_error = total_error
            dividing_value = threshold
            
    return dividing_value

data_path='../autodl-tmp/dataset_ROP'
with open(os.path.join(data_path,'annotations.json'),'r') as f:
    data_dict=json.load(f)
with open(os.path.join(data_path,'split','1.json'),'r') as f:
    split_list=json.load(f)

access_data=split_list['train']+split_list['val']
data_angle_list={
    'visible':{1:[],2:[],3:[]},'near':{1:[],2:[],3:[]},'far':{1:[],2:[],3:[]}
}
for image_name in access_data:
    data=data_dict[image_name]
    if data['zone']==0:
        continue
    distance=data['optic_disc_pred']["distance"]
    angle=data['zone_pred']["min_angle"]
    data_angle_list[distance][data['zone']].append(angle)


for distance in data_angle_list:
    for zone in data_angle_list[distance]:
        if len(data_angle_list[distance][zone])<=10:
            continue
        data_angle_list[distance][zone] = remove_outliers(data_angle_list[distance][zone])

dividing={
    'visible':0,'near':11.5,'far':30
}
# Assuming data_angle_list is populated as before

    # Calculate dividing values between zones
a = get_dividing(data_angle_list['visible'][1], data_angle_list['visible'][2])
b = get_dividing(data_angle_list['visible'][2], data_angle_list['visible'][3])
    

for image_name in data_dict:
    data = data_dict[image_name]
    if 'zone_pred' in data:
        distance = data['optic_disc_pred']["distance"]
        # Classify into zones based on dividing values
        angle=data['zone_pred']['min_angle']+dividing[distance]
        if angle < a:
            data['zone_pred']['zone'] = 1
        elif angle >= a and angle < b:
            data['zone_pred']['zone'] = 2
        else:
            data['zone_pred']['zone'] = 3
print(a,b)
# with open(os.path.join(data_path,'annotations.json'),'w') as f:
#     json.dump(data_dict,f)