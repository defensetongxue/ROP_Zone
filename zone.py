import os,json
from estimate_angle import ZoneProcesser
data_path='../autodl-tmp/dataset_ROP'
with open(os.path.join(data_path,'annotations.json'),'r') as f:
    data_dict=json.load(f)

# simplify the data 
processer=ZoneProcesser()
for image_name in data_dict:
# for image_name in test_list:
    data=data_dict[image_name]
    optic_disc=data['optic_disc_pred']
    # if optic_disc['distance']!='visible':
    #     continue
    if "ridge_visual_path" in data:
        angle=processer._get_angle(data["ridge_visual_path"],optic_disc["position"],optic_disc['distance'])
        # zone[data['zone']-1].append((image_name,angle))
        data_dict[image_name]['zone_pred']=angle
with open(os.path.join(data_path,'annotations.json'),'w') as f:
    json.dump(data_dict,f)