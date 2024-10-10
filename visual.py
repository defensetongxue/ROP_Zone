from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import os
import random

def visual_zone(image_path, ridge_path, zone_pred, optic_disc, distance, save_path='./tmp.jpg',ridge_threshold=0.5):
    # Open the image file.
    image = Image.open(image_path).convert("RGBA")

    # Create a blue mask.
    mask = Image.open(ridge_path).convert('L')
    mask_np = np.array(mask)
    mask_np=np.where(mask_np>255*ridge_threshold,1,0)
    mask_blue = np.zeros((mask_np.shape[0], mask_np.shape[1], 4), dtype=np.uint8)
    mask_blue[..., 2] = 255  # Set blue channel to maximum
    mask_blue[..., 3] = (mask_np * 127.5).astype(np.uint8)  # Adjust alpha channel

    # Convert mask to an image.
    mask_image = Image.fromarray(mask_blue)

    # Overlay the mask onto the original image.
    composite = Image.alpha_composite(image, mask_image)

    # Draw on the image.
    draw = ImageDraw.Draw(composite)
    font_path = 'arial.ttf'
    font = ImageFont.truetype(font_path, size=40)  # Adjust font size as needed.

    # Draw circles for optic disc, min_coor, and avg_coor
    optic_x, optic_y = optic_disc
    draw.ellipse((optic_x-30, optic_y-30, optic_x+30, optic_y+30), fill='red')

    # Min coordinates circle and text
    min_x, min_y = zone_pred["min_coor"]
    draw.ellipse((min_x-10, min_y-10, min_x+10, min_y+10), fill='white')
    draw.text((min_x+10, min_y+10), f"{zone_pred['min_angle']}°", fill="white", font=font)

    # Avg coordinates circle and text
    avg_x, avg_y = zone_pred["avg_coor"]
    draw.ellipse((avg_x-10, avg_y-10, avg_x+10, avg_y+10), fill='white')
    draw.text((avg_x+10, avg_y+10), f"{zone_pred['avg_angle']}°", fill="white", font=font)

    # Calculate position for Min_Angle and Avg_Angle text using textbbox
    image_width, _ = image.size
    bbox = draw.textbbox((0, 0), f"Min_Angle: {zone_pred['min_angle']}", font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Print Distance, Min_Angle, and Avg_Angle at the top of the image
    draw.text((10, 10), f"Distance: {distance}", fill="white", font=font)
    draw.text((image_width - text_width - 10, 10), f"Min_Angle: {zone_pred['min_angle']}", fill="white", font=font)
    draw.text((image_width - text_width - 10, 10 + text_height + 5), f"Avg_Angle: {zone_pred['avg_angle']}", fill="white", font=font)
    # Save the image
    rgb_image = composite.convert("RGB")
    rgb_image.save(save_path)

if __name__ == "__main__":
    with open('../autodl-tmp/dataset_ROP/annotations.json', 'r') as f:
        data_dict = json.load(f)
    visual_number = {
        "near": 10,
        "far": 10,
        'visible': 10  
    }
    
    distance_list = ["near", 'far', "visible"]
    for distance_item in distance_list:
        os.makedirs(os.path.join('experiments', distance_item), exist_ok=True)
        os.system(f"rm -rf {os.path.join('experiments', distance_item)}/*")
    # Shuffle the data_dict keys for random iteration
    items = list(data_dict.items())
    for image_name, data in items:
        if 'zone_pred' not in data:
            continue
        optic_disc = data['optic_disc_pred']
        
        visual_zone(data['image_path'],
                    data["ridge_seg"]["ridge_seg_path"],
                    zone_pred=data["zone_pred"],
                    optic_disc=data['optic_disc_pred']["position"],
                    distance=optic_disc['distance'],
                    save_path=f'./experiments/{optic_disc["distance"]}/{image_name}'
                    )
