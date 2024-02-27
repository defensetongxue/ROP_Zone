import os,json
data_path='../autodl-tmp/dataset_ROP'
with open(os.path.join(data_path,'annotations.json'),'r') as f:
    data_dict=json.load(f)
cnt=0
for image_name in data_dict:
    data = data_dict[image_name]
    
    # Check if 'zone_pred' exists and is a string
    if 'zone_pred' in data and isinstance(data['zone_pred'], str):
        del data['zone_pred']  # Correct syntax to remove a key from a dictionary
        cnt+=1
    else:
        # Ensure that 'zone_pred', if present, is a dictionary
        if 'zone_pred' in data:
            assert isinstance(data['zone_pred'], dict), f"zone_pred in {image_name} is not a dict"
print(f"rm number {str(cnt)}")
with open(os.path.join(data_path,'annotations.json'),'w') as f:
    json.dump(data_dict,f)