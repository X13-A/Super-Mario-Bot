from PIL import Image, ImageOps, ImageDraw
import numpy as np
import os
import argparse
import random
import json
import configparser
import glob

def generate_data(sprites_path, backgrounds_path, res_path, res_width, res_height):
    # Load sprites and backgrounds
    sprites = [Image.open(sprite) for sprite in glob.glob(f"{sprites_path}/**/*.png", recursive=True)]
    backgrounds = [Image.open(os.path.join(backgrounds_path, bg)) for bg in os.listdir(backgrounds_path)]

    # Ensure the output directory exists
    images_path = f"{res_path}/images/train"
    labels_path = f"{res_path}/labels/train"
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(labels_path, exist_ok=True)
    i = 0
    # Iterate and create images
    for background in backgrounds:
        for _ in range(10):  # Repeat 10 times
            result_image = Image.new("RGBA", (res_width, res_height), (255, 255, 255, 0))
            result_image.paste(background, (0, 0), background)
            
            annotations = []

            for sprite in sprites:
                # Randomly scale the sprite
                scale_factor = random.uniform(1, 3.0)
                scaled_sprite = ImageOps.scale(sprite, scale_factor)

                # Randomly rotate the sprite
                rotation_angle = random.randint(0, 360)
                rotated_sprite = ImageOps.exif_transpose(scaled_sprite.rotate(rotation_angle, expand=True))

                # Calculate a random position to place the sprite
                x_offset = random.randint(0, res_width - rotated_sprite.width)
                y_offset = random.randint(0, res_height - rotated_sprite.height)

                # Paste the sprite onto the background
                result_image.paste(rotated_sprite, (x_offset, y_offset), rotated_sprite)
                
                # Save the annotation data
                annotations.append(f"0 {(x_offset + rotated_sprite.width/2) / res_width} {(y_offset + rotated_sprite.height/2) / res_height} {rotated_sprite.width / res_width} {rotated_sprite.height / res_height}")

            # Save the resulting image
            result_image_filename = f"result_{i}.png"
            result_image_path = os.path.join(images_path, result_image_filename)
            result_image.save(result_image_path, "PNG")

            # Save the annotation data
            result_label_filename = f"result_{i}.txt"
            result_label_path = os.path.join(labels_path, result_label_filename)
            
            with open(result_label_path, 'w') as file:
                file.write("\n".join(annotations))
            i += 1


def load_config():
    config = configparser.ConfigParser()
    config.read('config.properties')

    sprite_config = config['sprite_config']
    background_config = config['background_config']
    res_config = config['res_config']

    return (
        sprite_config['sprites_path'],
        background_config['backgrounds_path'],
        res_config['res_path'],
        int(res_config['res_width']),
        int(res_config['res_height']),
    )


def main():
    parser = argparse.ArgumentParser(description="Generate training data from sprites and backgrounds.")
    parser.add_argument("--config", action="store_true", help="Use this flag to load configuration from a config file.")
    args = parser.parse_args()
    print("sdsd")

    if args.config:
        sprites_path, backgrounds_path, res_path, res_width, res_height = load_config()
    else:
        parser = argparse.ArgumentParser(description="Generate images with sprites placed on backgrounds.")
        parser.add_argument("--sprites_path", type=str, help="Path to the directory containing sprite images.")
        parser.add_argument("--backgrounds_path", type=str, help="Path to the directory containing background images.")
        parser.add_argument("--res_path", type=str, help="Output directory where resulting images will be saved.")
        parser.add_argument("--res_width", type=int, help="Width of the resulting images in pixels.")
        parser.add_argument("--res_height", type=int, help="Height of the resulting images in pixels.")
    
        args = parser.parse_args()
        sprites_path = args.sprites_path
        backgrounds_path = args.backgrounds_path
        res_path = args.res_path
        res_width = args.res_width
        res_height = args.res_height

    generate_data(sprites_path, backgrounds_path, res_path, res_width, res_height)

if __name__ == "__main__":
    main()
