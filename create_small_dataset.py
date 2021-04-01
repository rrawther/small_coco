import json,os
import pdb, time
from pycocotools.coco import COCO
import shutil

####################################################################################################
source_root = "/dockerx/coco2017"
datadir = os.path.join(source_root, 'annotations')
json_file = "bbox_only_instances_train2017.json"
datadir_val = os.path.join(source_root, 'annotations')
json_file_val = "bbox_only_instances_val2017.json"

dest_root = "/dockerx/small_coco2017"
new_json_file = "bbox_only_instances_train2017.json"
new_json_file_val = "bbox_only_instances_val2017.json"
new_imgs_name = "train2017" 
new_imgs_name_val = "val2017" 

regenerate = True 
#regenerate = False 
num = 2048 
num_val = 2048 
images_list = [391895, 522418, 184613, 318219, 554625, 574769, 60623, 309022, 5802, 222564, 118113, 193271, 224736, 483108, 403013, 374628]
#images_list = [391895]
####################################################################################################


def generate_annotations(img_list, src_file, dest_file):
    with open(os.path.join(datadir, src_file), 'r') as f:  
        coco = json.load(f)

    new_images = []
    new_annotations = []

    # look for images
    for img in coco['images']:
        if img['id'] in img_list:
            new_images.append(img)

    # look for annotations
    for ann in coco['annotations']:
        if ann['image_id'] in img_list:
            new_annotations.append(ann)

    # update and save
    coco['images'] = new_images
    coco['annotations'] = new_annotations

    new_dir_path = os.path.join(dest_root, "annotations", dest_file)  
#    if os.path.exists(new_dir_path):
#        shutil.rmtree(new_dir_path)
#    os.mkdir(new_dir_path) 
    print("begin to save to %s " %(new_dir_path))
    with open( os.path.join(new_dir_path), 'w') as ff:
        print("dumping json")
        json.dump(coco, ff)


def generate_images(img_list, new_name, new_dir):
    new_dir_path = os.path.join(dest_root, new_name)  

    if os.path.exists(new_dir_path):
        shutil.rmtree(new_dir_path)
    os.mkdir(new_dir_path) 

    print("copy from %s to %s"  %(source_root+new_dir, new_dir_path))
    for img in img_list:
        img_name = format(img, "012") + ".jpg"
        src_file  = os.path.join(source_root, new_dir, img_name)
        dest_file = os.path.join(new_dir_path, img_name)
        shutil.copyfile(src_file, dest_file) 
    


if regenerate:
    with open(os.path.join(datadir, json_file), 'r') as f:  
        coco = json.load(f)
    images_list = [item['id'] for item in coco['images'][:num]]
    #print(images_list)
    with open(os.path.join(datadir, json_file_val), 'r') as f:  
        cocoval = json.load(f)
    images_list_val = [item['id'] for item in cocoval['images'][:num_val]]

if os.path.exists(dest_root):
    shutil.rmtree(dest_root)
os.mkdir(dest_root)

new_dir_path = os.path.join(dest_root, "annotations")  
if os.path.exists(new_dir_path):
    shutil.rmtree(new_dir_path)
os.mkdir(new_dir_path) 

generate_annotations(images_list, json_file, new_json_file)
generate_images(images_list, new_imgs_name, "train2017")
generate_annotations(images_list_val, json_file_val, new_json_file_val)
generate_images(images_list_val, new_imgs_name_val, "val2017")


