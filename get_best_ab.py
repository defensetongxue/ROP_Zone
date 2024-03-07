import os
import json
import itertools

class Handler:
    def __init__(self, data_path):
        with open(os.path.join(data_path, 'annotations.json')) as f:
            self.data_dict = json.load(f)
        self.split_list = []
        for image_name in self.data_dict:
            data = self.data_dict[image_name]
            if isinstance(data, int):
                print(image_name, data)
                continue
            if 'zone_pred' not in data or data['zone'] <= 0:
                continue
            if 'ridge_seg' not in data or "ridge_seg_path" not in data['ridge_seg']:
                continue
            self.split_list.append(image_name)
        self.p={
            1:0,2:0,3:0
        }
        cnt=0
        for image_name in self.split_list:
            self.p[self.data_dict[image_name]['zone']]+=1
            cnt+=1
        print(self.p)
        for z in self.p:
            self.p[z]=int(cnt/self.p[z])
    def get_acc(self, a, b, threshold_1, threshold_2):
        appendix = {
            'visible': 0,
            'near': a,
            'far': b
        }
        error_number = 0
        for image_name in self.split_list:
            data = self.data_dict[image_name]
            distance = data['optic_disc_pred']["distance"]
            angle = data['zone_pred']["min_angle"] + appendix[distance]
            if angle < threshold_1:
                pred = 1
            elif threshold_1 <= angle < threshold_2:
                pred = 2
            else:
                pred = 3
            if pred != data['zone']:
                error_number += self.p[data['zone']]
        return error_number

if __name__ == '__main__':
    a_l = range(10, 25)
    b_l = range(30, 45)
    t1_l = range(40, 50)
    t2_l = range(70, 80)
    handler = Handler('../autodl-tmp/dataset_ROP')

    best_error_number = float('inf')
    record_best = ()

    for a, b, c, d in itertools.product(a_l, b_l, t1_l, t2_l):
        error_number = handler.get_acc(a, b, c, d)
        if error_number < best_error_number:
            best_error_number = error_number
            record_best = (a, b, c, d)
    
    print(f"Best parameters: a={record_best[0]}, b={record_best[1]}, threshold_1={record_best[2]}, threshold_2={record_best[3]} with error_number={best_error_number}")
