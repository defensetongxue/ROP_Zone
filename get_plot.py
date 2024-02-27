from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import os
import random
from visual import visual_zone
from shutil import copy


def visual_mask(image_path, mask_path, max_val, save_path='./tmp.jpg'):
    # Open the image file.
    image = Image.open(image_path).convert("RGBA")  # Convert image to RGBA
    # Create a blue mask.
    mask = Image.open(mask_path).convert('L')
    mask_np = np.array(mask)/255
    mask_blue = np.zeros(
        (mask_np.shape[0], mask_np.shape[1], 4), dtype=np.uint8)  # 4 for RGBA
    mask_blue[..., 2] = 255  # Set blue channel to maximum
    # Adjust alpha channel according to the mask value
    mask_blue[..., 3] = (mask_np * 127.5).astype(np.uint8)

    # Convert mask to an image.
    mask_image = Image.fromarray(mask_blue)

    # Overlay the mask onto the original image.
    composite = Image.alpha_composite(image, mask_image)

    # Define font and size.
    draw = ImageDraw.Draw(composite)
    # 20 is the font size. Adjust as needed.
    font = ImageFont.truetype('arial.ttf', size=40)
    # Prints the text in the top-left corner with a
    draw.text((10, 10), f'Confidence: {str(max_val)}', fill="white", font=font)

    # Convert back to RGB mode (no transparency).
    rgb_image = composite.convert("RGB")
    # Save the image with mask to the specified path.
    rgb_image.save(save_path)


def draw_bbox(image_path, points, width,  save_path, values=None, font_size=40, value_font_size=24):
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # Load the font for texts and values
    font_path = './arial.ttf'
    value_font = ImageFont.truetype(font_path, value_font_size)

    # Draw the squares if there are points
    if points:
        if len(points) > 3:
            points = random.sample(points, 3)
            if values is not None:
                values = random.sample(values, 3)

        for i, (x, y) in enumerate(points):
            # Define the position of the squares
            top_left = (x - width // 2, y - width // 2)
            bottom_right = (x + width // 2, y + width // 2)
            # Draw the squares
            draw.rectangle([top_left, bottom_right], outline="green", width=5)

            # Draw the values on the top left of the square
            if values is not None:
                # print(values[i])
                value = round(values[i], 2)
                # print(value)
                val_text = str(value)
                # Calculate position for the text
                val_x, val_y = top_left
                draw.text((val_x, val_y - value_font_size),
                          val_text, fill="yellow", font=value_font)
    # Save the image
    img.save(save_path)


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
    random.shuffle(items)

    for image_name, data in items:
        if 'zone_pred' not in data:
            continue
        optic_disc = data['optic_disc_pred']

        if data['stage']!=3:
            continue
        if visual_number[optic_disc["distance"]] < 0 and image_name !='1708.jpg':
            continue
        
        visual_number[optic_disc["distance"]] -= 1
        if ("ridge_visual_path" not in data) or 'ridge' not in data or "visual_stage_path" not in data or data['stage']<=0 :
            continue
        save_dir = f'./experiments/{optic_disc["distance"]}/{image_name}'
        os.makedirs(save_dir, exist_ok=True)

        # visual zone
        visual_zone(data['image_path'],
                    data["ridge_seg"]["ridge_seg_path"],
                    zone_pred=data["zone_pred"],
                    optic_disc=data['optic_disc_pred']["position"],
                    distance=optic_disc['distance'],
                    save_path=os.path.join(save_dir, 'zone.jpg')
                    )

        # visual ridge
        visual_mask(data['image_path'],
                    data["ridge_seg"]["ridge_seg_path"],
                    max_val=round(data['ridge_seg']['max_val'],2),
                    save_path=os.path.join(save_dir, 'ridge.jpg'))

        # visual stage
        copy(data["visual_stage_path"], os.path.join(save_dir, 'stage.jpg'))

        # orignal image
        copy(data['image_path'], os.path.join(save_dir,str(data['stage'])+'.jpg'))
