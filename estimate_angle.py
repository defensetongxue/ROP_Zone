import os,json
import numpy as np
import math
from PIL import Image
class ZoneProcesser():
    def __init__(self,image_size=(1600,1200),
                 camrea_weight=1570,
                 camera_angle=math.pi/2,
                 sample_dense=10,
                 threshold=0.5):
        self.weight,self.height=image_size
        self.camera_angle=camera_angle
        self.radius=camrea_weight/(2*math.sin(camera_angle/2))
        self.sample_dense=sample_dense
        self.threshold=threshold

        self.crop_padded=CropPadding()
    def _get_z(self,x,y):
        tmp=self.radius**2-x**2-y**2
        if tmp>=0:
            return round(math.sqrt(tmp))
        return 0
    def _get_xy(self,coordinate_x,coordinate_y):
        return coordinate_x-(self.weight/2),coordinate_y-(self.height/2)
    
    def _xy2coor(self,x,y):
        return x+(self.weight/2),y+(self.height/2)
    
    def calculate_angle(self,ridge_x,ridge_y,optic_x,optic_y):
        z_ridge = self._get_z(ridge_x, ridge_y)
        z_optic = self._get_z(optic_x, optic_y)
        l = math.sqrt((ridge_x - optic_x)**2 + (ridge_y - optic_y)**2 + (z_ridge - z_optic)**2)
        # in circle l ischord length, cal the angle with l and radius
        try:
            angle=2*math.asin(l/(2*self.radius))
        except:
            print(l)
            raise
        return math.degrees(angle)
    
    def ridge_sample(self,mask):
        """
        For each point in mask 2D numpy array, if coordinates x, y satisfy 
        x % sample_dense == 0 and y % sample_dense == 0 and mask[x][y] > threshold, 
        sample it. Return a list of coordinates (x, y).
        """
        rows, cols = np.where((mask > self.threshold) & 
                              (np.arange(mask.shape[0])[:, None] % self.sample_dense == 0) & 
                              (np.arange(mask.shape[1])[None, :] % self.sample_dense == 0))
        samples_coordinate = list(zip(rows, cols))
        samples=[]
        for i,j in samples_coordinate:
            x,y =self._get_xy(j,i)
            samples.append([x,y])
        return samples
    
    def _get_angle(self, ridge_path, optic_disc_coordinate, distance):
        optic_x, optic_y = self._get_xy(optic_disc_coordinate[0], optic_disc_coordinate[1])
        print(ridge_path)
        ridge = Image.open(ridge_path).convert('L')
        ridge = np.array(ridge)
        ridge[ridge > 0] = 1
        samples = self.ridge_sample(ridge)

        angles = []
        for x, y in samples:
            angle = self.calculate_angle(x, y, optic_x, optic_y)
            angles.append((angle, self._xy2coor(x,y)))

        if not angles:
            return json.dumps({"error": "No samples found."})

        # Calculate min and avg angles
        min_angle, min_coor = min(angles, key=lambda x: x[0])
        avg_angle = sum(angle for angle, _ in angles) / len(angles)
        
        # Find the coordinate closest to the average angle
        avg_coor = min(angles, key=lambda x: abs(x[0] - avg_angle))[1]

        result = {
            "min_angle": int(min_angle),
            "min_coor": min_coor,
            "avg_angle": int(avg_angle),
            "avg_coor": avg_coor
        }
        
        return result
    
class CropPadding:
    def __init__(self,box=(80, 0, 1570, 1200)):
        self.box=box
    def __call__(self,img) :
        return img.crop(self.box)