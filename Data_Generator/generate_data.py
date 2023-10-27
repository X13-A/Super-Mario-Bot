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
        
        # Load sprites
        count = {"mario":6,"koopa":12,"ground":120,"pipe":90,"spike_turtle":60,
                "turtle":60,"goomba":60,"bullet":60,"question_block":60}
        
        # Ensure the output directory exists
        images_path = f"{self.res_path}/images/train"
        labels_path = f"{self.res_path}/labels/train"

        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
            
        i = 0
        # Iterate and create images
        for background in backgrounds:
            for _ in range(20):  # Repeat 10 times
                
                width_max = 0
                height_max = 0
                all_sprites = {}
                for k,v in count.items():
                    sprite_paths = glob.glob(f"{self.sprites_path}/{k}/**/*.png", recursive=True)
                    all_sprites[k] = []
                    for sprite in sprite_paths * v:
                        
                        # Randomly rotate the sprite 
                        rotation_angle = random.randint(0, 360)
                        rotated_sprite = ImageOps.exif_transpose(Image.open(sprite).rotate(rotation_angle, expand=True)) 
                        if width_max<rotated_sprite.width : 
                            width_max = rotated_sprite.width
                        if height_max<rotated_sprite.height: 
                            height_max = rotated_sprite.height
                            
                        all_sprites[k].append(rotated_sprite)
                        
                indexes=[]
                for w in range(0,int(self.res_width/width_max)) :
                    for h in range(0,int(self.res_height/height_max)):
                        indexes.append((w*width_max,h*height_max))
                        
                resized_background = background.resize((254,176))
                result_image = Image.new("RGBA", (self.res_width,self. res_height), (255, 255, 255, 0))
                for x in range(0,10) :
                    for y in range (0,10) :
                        pos_x = int(x*254)
                        pos_y = int(y*176)
                        #print(str(pos_x)+ " : "+str(pos_y))
                        result_image.paste(resized_background,(pos_x, pos_y ))
                
                annotations = []

                for class_index, class_label in enumerate(self.classes):
                    for sprite in all_sprites[class_label]:    
                        # Calculate a random position to place the sprite
                        rand_ind = random.randint(0,len(indexes)-1)
                        x_offset = indexes[rand_ind][0]
                        y_offset = indexes[rand_ind][1]
                           
                        indexes.remove(indexes[rand_ind])

                        # Paste the sprite onto the background
                        result_image.paste(sprite, (x_offset, y_offset), sprite)

                        # Save the annotation data
                        annotations.append(f"{class_index} {(x_offset + sprite.width/2) / self.res_width} {(y_offset + sprite.height/2) / self.res_height} {sprite.width / self.res_width} {sprite.height / self.res_height}")

                # Save the resulting image
                print(i)
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
