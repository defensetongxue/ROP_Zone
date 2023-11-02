
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import json,os

def visual_mask(image_path, ridge_path, point, text, save_path='./tmp.jpg'):
    # Open the image file.
    image = Image.open(image_path).convert("RGBA")  # Convert image to RGBA
    
    # Create a blue mask.
    mask = Image.open(ridge_path).convert('L')
    mask_np = np.array(mask)
    mask_blue = np.zeros((mask_np.shape[0], mask_np.shape[1], 4), dtype=np.uint8)  # 4 for RGBA
    mask_blue[..., 2] = 255  # Set blue channel to maximum
    mask_blue[..., 3] = (mask_np * 127.5).astype(np.uint8)  # Adjust alpha channel according to the mask value
    
    # Convert mask to an image.
    mask_image = Image.fromarray(mask_blue)
    
    # Overlay the mask onto the original image.
    composite = Image.alpha_composite(image, mask_image)
    
    # Draw on the image.
    draw = ImageDraw.Draw(composite)
    x, y = point
    draw.ellipse((x-10, y-10, x+10, y+10), fill='red')  # Draws a small red circle around the point
    
    # Define font and size.
    font = ImageFont.truetype( 'arial.ttf',size=30)  # 20 is the font size. Adjust as needed.
    
    draw.text((10, 10), text, fill="white", font=font)  # Prints the text in the top-left corner with a specified font and size
    
    # Convert back to RGB mode (no transparency).
    rgb_image = composite.convert("RGB")
    
    # Save the image with mask and points to the specified path.
    rgb_image.save(save_path)
if __name__ =="__main__":
    with open('./tmp.json','r') as f:
        zone_list=json.load(f)['zone']
    with  open('../autodl-tmp/dataset_ROP/annotations.json','r') as f:
        data_dict=json.load(f)
    cnt=0

    for data_list in zone_list:
        cnt+=1
        os.makedirs(f'./experiments/{str(cnt)}',exist_ok=True)
        data_list=sorted(data_list,key= lambda x:x[1])
        for image_name,angle in data_list:
            data=data_dict[image_name]
            if 'optic_disc_gt' in data:
                optic_disc=data['optic_disc_gt']
            else: 
                optic_disc=data['optic_disc_pred']
            
            visual_mask(data['image_path'],
                        data['ridge_diffusion_path'],
                        optic_disc['position'],
                        text=str(angle),
                        save_path=f'./experiments/{str(cnt)}/{str(angle)}_{image_name}'
                        )