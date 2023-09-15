from PIL import Image
import numpy as np
import os
import argparse

def extract_spritesheet(spritesheet_path, output_directory, cols, rows, sprite_name):
    # Open the spritesheet image
    spritesheet = Image.open(spritesheet_path)

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

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
            frame_path = os.path.join(output_directory, frame_filename)
            sprite_frame.save(frame_path, "PNG")

def main():
    parser = argparse.ArgumentParser(description="Extract sprite frames from a spritesheet.")
    parser.add_argument("spritesheet_path", type=str, help="Path to the spritesheet image.")
    parser.add_argument("output_directory", type=str, help="Output directory where sprite frames will be saved.")
    parser.add_argument("sprite_width", type=int, help="Width of each sprite frame in pixels.")
    parser.add_argument("sprite_height", type=int, help="Height of each sprite frame in pixels.")
    parser.add_argument("sprite_name", type=str, help="Base name for the extracted sprite frames.")

    args = parser.parse_args()

    extract_spritesheet(args.spritesheet_path, args.output_directory, args.sprite_width, args.sprite_height, args.sprite_name)

if __name__ == "__main__":
    main()