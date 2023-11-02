import os,json
import numpy as np
import math
from PIL import Image
class ZoneProcesser():
    def __init__(self,image_size=(1600,1200),
                 camrea_weight=1570,
                #  camera_angle=2*math.pi/3,
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
        if self.radius**2-x**2-y**2>=0:
            return round(math.sqrt(self.radius**2-x**2-y**2))
        print(self.radius,x,y)
        raise
    def _get_xy(self,coordinate_x,coordinate_y):
        return coordinate_x-(self.weight/2),coordinate_y-(self.height/2)
    def calculate_angle(self,ridge_x,ridge_y,optic_x,optic_y):
        z_ridge = self._get_z(ridge_x, ridge_y)
        z_optic = self._get_z(optic_x, optic_y)
        l = math.sqrt((ridge_x - optic_x)**2 + (ridge_y - optic_y)**2 + (z_ridge - z_optic)**2)
        # in circle l ischord length, cal the angle with l and radius
        angle=2*math.asin(l/(2*self.radius))
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
    def _get_angle(self,ridge_path,optic_disc_coordinate,distance):
        optic_x,optic_y=self._get_xy(optic_disc_coordinate[0],optic_disc_coordinate[1])
        # print(optic_x,optic_y)
        ridge=Image.open(ridge_path).convert('L')
        ridge=np.array(ridge)
        ridge[ridge>0]=1
        samples=self.ridge_sample(ridge)
        print("there is {} points sampled".format(len(samples)))
        min_angle=99999
        for x,y in samples:
            min_angle=min(min_angle,
                          self.calculate_angle(x,y,optic_x,optic_y))
        return int(min_angle)
class CropPadding:
    def __init__(self,box=(80, 0, 1570, 1200)):
        self.box=box
    def __call__(self,img) :
        return img.crop(self.box)