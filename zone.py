import os,json
from estimate_angle import ZoneProcesser
data_path='../autodl-tmp/dataset_ROP'
with open(os.path.join(data_path,'annotations.json'),'r') as f:
    data_orignal=json.load(f)

# simplify the data 
data_dict={}
for image_name in data_orignal:
    data=data_orignal[image_name]
    if "ridge" in data:
        if data["zone"]<=0:
            print(image_name)
            if data["stage"]<=0:
                print("? ",image_name," ?")
            continue
        
        if 'optic_disc_gt' in data:
            if data['optic_disc_gt']['distance']!='visible':
                continue
        else:
            if data['optic_disc_pred']['distance']!='visible' or\
                data['optic_disc_pred']['value']<=0.25:
                continue
        data_dict[image_name]={
            "ridge_diffusion_path":data_orignal[image_name]["ridge_diffusion_path"],
            "zone":data["zone"],
            'optic_disc_pred':data['optic_disc_pred']
        }
        if 'optic_disc_gt' in data:
            data_dict[image_name]['optic_disc_gt']=data['optic_disc_gt']
zone=[[],[],[]]
processer=ZoneProcesser()
for image_name in data_dict:
    data=data_dict[image_name]
    print(image_name)
    if 'optic_disc_gt' in data:
        optic_disc=data['optic_disc_gt']
    else: 
        optic_disc=data['optic_disc_pred']
    angle=processer._get_angle(data['ridge_diffusion_path'],optic_disc["position"],optic_disc['distance'])
    zone[data['zone']-1].append((image_name,angle))
with open('./tmp.json','w') as f:
    json.dump({'zone':zone},f)