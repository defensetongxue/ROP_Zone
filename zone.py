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
    if "ridge_seg" in data and "ridge_seg_path" in data["ridge_seg"]:
        angle=processer._get_angle(data["ridge_seg"]["ridge_seg_path"],optic_disc["position"])
        # zone[data['zone']-1].append((image_name,angle))
        data_dict[image_name]['zone_pred']=angle
with open(os.path.join(data_path,'annotations.json'),'w') as f:
    json.dump(data_dict,f)