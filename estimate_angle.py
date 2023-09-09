import os,json
import numpy as np
import math
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
