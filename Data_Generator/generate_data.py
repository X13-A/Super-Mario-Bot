from PIL import Image, ImageOps, ImageDraw
import numpy as np
import os
import argparse
import random
import json
import configparser
import glob

class DataGenerator:
    def __init__(self, sprites_path, backgrounds_path, res_path, res_width, res_height, classes):
        self.sprites_path = sprites_path
        self.backgrounds_path = backgrounds_path
        self.res_path = res_path
        self.res_width = res_width
        self.res_height = res_height
        self.classes = classes
    
    def generate_data(self):
        # Load backgrounds
        backgrounds = [Image.open(os.path.join(self.backgrounds_path, bg)) for bg in os.listdir(self.backgrounds_path)]

        # Utiliser la fonction max avec un lambda pour trouver les dimensions maximales
        all_sprites = [Image.open(sprite) for sprite in glob.glob(f"{self.sprites_path}/**/*.png", recursive=True)]
        width_max = max(all_sprites, key=lambda img: img.size[0]).size[0]
        height_max = max(all_sprites, key=lambda img: img.size[1]).size[1]

        indexes=[]
        for w in range(0,int(self.res_width/width_max)) :
            for h in range(0,int(self.res_height/height_max)):
                indexes.append((w*width_max,h*height_max))

        # Ensure the output directory exists
        images_path = f"{self.res_path}/images/train"
        labels_path = f"{self.res_path}/labels/train"

        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
            
        i = 0
        # Iterate and create images
        for background in backgrounds:
            for _ in range(10):  # Repeat 10 times
                indexes2 = indexes.copy()
                resized_background = background.resize((self.res_width, self.res_height))
                result_image = Image.new("RGBA", (self.res_width,self. res_height), (255, 255, 255, 0))
                result_image.paste(resized_background, (0, 0))
                
                annotations = []

                for class_index, class_label in enumerate(self.classes):
                    sprites = [Image.open(sprite) for sprite in glob.glob(f"{self.sprites_path}/{class_label}/**/*.png", recursive=True)]

                    for sprite in sprites:    
                        # Calculate a random position to place the sprite
                        rand_ind = random.randint(0,len(indexes2)-1)
                        x_offset = indexes2[rand_ind][0]
                        y_offset = indexes2[rand_ind][1]
                        print(str((x_offset,y_offset)))
                        
                        indexes2.remove(indexes2[rand_ind])

                        # Paste the sprite onto the background
                        result_image.paste(sprite, (x_offset, y_offset), sprite)

                        # Save the annotation data
                        annotations.append(f"{class_index} {(x_offset + sprite.width/2) / self.res_width} {(y_offset + sprite.height/2) / self.res_height} {sprite.width / self.res_width} {sprite.height / self.res_height}")

                # Save the resulting image
                result_image.save(os.path.join(images_path, f"result_{i}.png"), "PNG")

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
    class_config = config['class_config']

    return (
        sprite_config['sprites_path'],
        background_config['backgrounds_path'],
        res_config['res_path'],
        int(res_config['res_width']),
        int(res_config['res_height']),
        class_config['classes'].split(', '),
    )


def main():
    generator = DataGenerator(*load_config())
    generator.generate_data()

if __name__ == "__main__":
    main()


'''
# Randomly scale the sprite
scale_factor = random.uniform(1, 3.0)
scaled_sprite = ImageOps.scale(sprite, scale_factor)

# Randomly rotate the sprite
rotation_angle = random.randint(0, 360)
rotated_sprite = ImageOps.exif_transpose(scaled_sprite.rotate(rotation_angle, expand=True))
'''
