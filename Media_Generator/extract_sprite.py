from PIL import Image
import numpy as np
import os
import argparse
import configparser

def extract_spritesheet(input_path, output_path, cols, rows, sprite_name):    
    # Open the spritesheet image
    spritesheet = Image.open(input_path)

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Get the dimensions of the spritesheet
    sheet_width, sheet_height = spritesheet.size

    # Calculate the sprite width and height based on cols and rows
    sprite_width = sheet_width // cols
    sprite_height = sheet_height // rows

    # Loop through the rows and columns to extract each sprite frame
    
    for row in range(rows):
        for col in range(cols):
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height

            # Crop the sprite frame from the spritesheet
            sprite_frame = spritesheet.crop((left, upper, right, lower))
            print(row, col)
            # Save the sprite frame as a PNG file
            frame_filename = f"{sprite_name}_{row}_{col}.png"
            frame_path = os.path.join(output_path, frame_filename)
            sprite_frame.save(frame_path, "PNG")

def load_config():
    config = configparser.ConfigParser()
    config.read('config.properties')

    input_config = config['input_config']
    output_config = config['output_config']
    spritesheet_config = config['spritesheet_config']

    return (
        input_config['input_path'],
        output_config['output_path'],
        int(spritesheet_config['cols']),
        int(spritesheet_config['rows']),
        spritesheet_config['sprite_name'],
    )


def main():
    parser = argparse.ArgumentParser(description="Extracts sprites from spritesheets.")
    parser.add_argument("--config", action="store_true", help="Use this flag to load configuration from a config file.")
    args = parser.parse_args()

    if args.config: 
        input_path, output_path, cols, rows, sprite_name = load_config()
        extract_spritesheet(input_path, output_path, cols, rows, sprite_name)

if __name__ == "__main__":
    main()