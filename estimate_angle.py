import os,json
import numpy as np
import math
from PIL import Image
def get_z(x,y,radius):
    return round(math.sqrt(radius**2-x**2-y**2))
def ridge_sample(mask, threshold, sample_dense):
    """
    For each point in mask 2D numpy array, if coordinates x, y satisfy 
    x % sample_dense == 0 and y % sample_dense == 0 and mask[x][y] > threshold, 
    sample it. Return a list of coordinates (x, y).
    """
    rows, cols = np.where((mask > threshold) & 
                          (np.arange(mask.shape[0])[:, None] % sample_dense == 0) & 
                          (np.arange(mask.shape[1])[None, :] % sample_dense == 0))
    samples = list(zip(rows, cols))
    
    return samples

def calculate_angle(ridge_x,ridge_y,optic_x,optic_dic_y,radius):
    z_ridge = get_z(ridge_x, ridge_y, radius)
    z_optic = get_z(optic_x, optic_dic_y, radius)
    
    l = math.sqrt((ridge_x - optic_x)**2 + (ridge_y - optic_dic_y)**2 + (z_ridge - z_optic)**2)
    
    # in circle l ischord length, cal the angle with l and radius
    angle=round(2*math.acos(l/(2*radius)))
    return angle

def coodinate2xy(coordinate_x,coordinate_y):
    pass

class Zone():
    def __init__(self,image_size=(1600,1200),
                 camrea_weight=1570,
                 camera_angle=2*math.pi/3,
                 sample_dense=10,
                 threshold=0.5):
        self.weight,self.height=image_size
        self.camera_angle=camera_angle
        self.radius=camrea_weight/(2*math.cos(camera_angle/2))
        self.sample_dense=sample_dense
        self.threshold=threshold

        self.crop_padded=CropPadding()
    def _get_z(self,x,y):
        return round(math.sqrt(self.radius**2-x**2-y**2))
    def _get_xy(self,coordinate_x,coordinate_y):
        return coordinate_x-(self.weight/2),self.height-coordinate_y
    def calculate_angle(self,ridge_x,ridge_y,optic_x,optic_y):
        z_ridge = get_z(ridge_x, ridge_y)
        z_optic = get_z(optic_x, optic_y)

        l = math.sqrt((ridge_x - optic_x)**2 + (ridge_y - optic_y)**2 + (z_ridge - z_optic)**2)

        # in circle l ischord length, cal the angle with l and radius
        angle=round(2*math.acos(l/(2*self.radius)))
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
            x,y =self._get_xy(i,j)
            samples.append([x,y])
        return samples
    def _get_angle(self,ridge_path,optic_disc_coordinate,distance):
        optic_x,optic_y=self._get_xy(optic_disc_coordinate[0],optic_disc_coordinate[1])

        ridge=Image.open(ridge_path).convert('L')
        ridge=np.array(ridge)
        ridge[ridge>0]=1
        samples=self.ridge_sample(ridge)
        print("there is {} points sampled".format(len(samples)))
        min_angle=99999
        for x,y in samples:
            min_angle=min(min_angle,
                          self.calculate_angle(x,y,optic_x,optic_y))
        return min_angle
class CropPadding:
    def __init__(self,box=(80, 0, 1570, 1200)):
        self.box=box
    def __call__(self,img) :
        return img.crop(self.box)