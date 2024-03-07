import os,json
foshan_path='../autodl-tmp/dataset_ROP'
shenzhen_path='../autodl-tmp/ROP_shen'
path_list=[foshan_path,shenzhen_path]
zone_list={
    1:[],2:[],3:[]
}
for data_path in path_list:
    with open(os.path.join(data_path,'annotations.json'),'r') as f:
        data_dict=json.load(f)
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
        
with open('./experiments/zone_list.json','w') as f:
    json.dump(zone_list,f)