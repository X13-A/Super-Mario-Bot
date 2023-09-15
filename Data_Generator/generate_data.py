from PIL import Image, ImageOps
import numpy as np
import os
import argparse
import random
import json

def generate_data(sprites_path, backgrounds_path, res_path, res_width, res_height, json_output_file):
    data = []

    # Load sprites and backgrounds
    sprites = [Image.open(os.path.join(sprites_path, sprite)) for sprite in os.listdir(sprites_path)]
    backgrounds = [Image.open(os.path.join(backgrounds_path, bg)) for bg in os.listdir(backgrounds_path)]

    # Ensure the output directory exists
    os.makedirs(res_path, exist_ok=True)

    i = 0
    # Iterate and create images
    for sprite in sprites:
        for background in backgrounds:
            # Randomly scale the sprite
            scale_factor = random.uniform(0.5, 3.0)
            scaled_sprite = ImageOps.scale(sprite, scale_factor)

            # Randomly rotate the sprite
            rotation_angle = random.randint(0, 360)
            rotated_sprite = ImageOps.exif_transpose(scaled_sprite.rotate(rotation_angle, expand=True))

            # Calculate a random position to place the sprite
            x_offset = random.randint(0, res_width - rotated_sprite.width)
            y_offset = random.randint(0, res_height - rotated_sprite.height)

            # Create a new image with the specified dimensions
            result_image = Image.new("RGBA", (res_width, res_height), (255, 255, 255, 0))

            # Paste the sprite onto the background
            result_image.paste(background, (0, 0), background)
            result_image.paste(rotated_sprite, (x_offset, y_offset), rotated_sprite)

            # Save the resulting image
            result_filename = f"result_{i}.png"
            result_path = os.path.join(res_path, result_filename)
            result_image.save(result_path, "PNG")

            # Store annotation data
            annotation = {
                "image_path": result_filename,
                "bounding_boxes": [
                    {
                        "class": "player",
                        "x": x_offset,
                        "y": y_offset,
                        "width": rotated_sprite.width,
                        "height": rotated_sprite.height
                    }
                ]
            }
            data.append(annotation)
            i += 1

    # Write annotation data to JSON file
    with open(json_output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Generate images with sprites placed on backgrounds.")
    parser.add_argument("--sprites_path", type=str, help="Path to the directory containing sprite images.")
    parser.add_argument("--backgrounds_path", type=str, help="Path to the directory containing background images.")
    parser.add_argument("--res_path", type=str, help="Output directory where resulting images will be saved.")
    parser.add_argument("--res_width", type=int, help="Width of the resulting images in pixels.")
    parser.add_argument("--res_height", type=int, help="Height of the resulting images in pixels.")
    parser.add_argument("--json_output_file", type=str, help="Number of images to generate.")
    
    args = parser.parse_args()
    print(args)
    generate_data(args.sprites_path, args.backgrounds_path, args.res_path, args.res_width, args.res_height, args.json_output_file)

if __name__ == "__main__":
    main()
