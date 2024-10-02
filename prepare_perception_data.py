# A script to prepare the unity perception camera data generation to be ready
# for the ultralytics training
# Assumes a certain folder structure
# Class mapping is currently hardcoded

import sys
import os
import shutil
import random
import json


# Program Constants
SPLIT_RATIO = 0.2

def main(perception_path, dataset_path):

    # emptying the path of all pngs and txts
    clean_folder(dataset_path)

    image_path = os.path.join(dataset_path,'train/images')

    move_images(perception_path, image_path)

    create_annotations_txt(perception_path, dataset_path)

    train_test_split(dataset_path)

def clean_folder(folder_path):

    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file ends with .png or .txt
            if file.endswith('.png') or file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    print("Folder cleaned")


def create_annotations_txt(perception_path, dataset_path):
    """
    Parses a Unity camera output JSON file with bounding boxes and creates YOLO .txt annotations.

    :param json_path: Path to the Unity perception JSON file.
    :param output_dir: Directory to save YOLO .txt annotation files.
    :param class_mapping: Dictionary mapping class names to YOLO class IDs.
    """
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(dataset_path,'train/labels')
    os.makedirs(output_dir, exist_ok=True)

    class_mapping = {
    'Shark': 0,
    'RIP': 1,
    'Human': 2
    }

    # for each JSON in the perception data
    for file in os.listdir(perception_path):
        if file.endswith('.json'):

            json_file = os.path.join(perception_path, file)

            # Load the JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Parse each bounding box in the JSON
            for capture in data['captures']:
                image_filename = capture['filename']
                image_width, image_height = capture['dimension']

                # Output file path with the same name as the image but with .txt extension
                output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(image_filename))[0] + '.txt')

                with open(output_file, 'w') as txt_file:
                    empty_flag = 1
                    for annotation in capture['annotations']:
                        if annotation['id'] == 'bounding box':  # Check annotation type if multiple types exist
                            if 'values' not in annotation: continue # Check if this annotation has any detection
                            for bbox in annotation['values']:
                                class_name = bbox['labelName']
                                class_id = class_mapping.get(class_name, -1)  # Get class ID or -1 if not found
                                if class_id == -1:
                                    print(f"Warning: Class '{class_name}' not found in class mapping.")
                                    continue

                                # Bounding box coordinates
                                x_center, y_center = bbox['origin']
                                width, height = bbox['dimension']

                                # Convert to YOLO format (normalized)
                                x_center = x_center / image_width
                                y_center = y_center / image_height
                                norm_width = width / image_width
                                norm_height = height / image_height

                                # Write to .txt file in YOLO format
                                txt_file.write(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}\n")
                                empty_flag = 0
                # after opening the write, if still empty delete
                if empty_flag: del output_file

def move_images(perception_path, dest_dir):

    os.makedirs(dest_dir, exist_ok=True)

    # Iterate over files in the source directory
    for file_name in os.listdir(perception_path):
        # Check if the file has a .png extension
        if file_name.lower().endswith('.png'):
            # Construct the full file paths
            src_file_path = os.path.join(perception_path, file_name)
            dst_file_path = os.path.join(dest_dir, file_name)

            # Move the file
            shutil.copy(src_file_path, dst_file_path)
            # print(f"Moved: {file_name}")

    print(f"All .png files have been moved from {perception_path} to {dest_dir}.")


def train_test_split(dataset_path):

    train_images_dir = 'train/images'
    train_annotations_dir = 'train/labels'
    val_images_dir = 'val/images'
    val_annotations_dir = 'val/labels'

    train_images_dir = os.path.join(dataset_path,train_images_dir)
    train_annotations_dir = os.path.join(dataset_path,train_annotations_dir)
    val_images_dir = os.path.join(dataset_path,val_images_dir)
    val_annotations_dir = os.path.join(dataset_path,val_annotations_dir)

    # Create val directories if they don't exist
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(val_annotations_dir, exist_ok=True)

    # Get the list of all images in the training directory
    images = os.listdir(train_images_dir)

    # Shuffle the images randomly
    random.shuffle(images)

    # Calculate the number of images to move
    num_val_images = int(len(images) * SPLIT_RATIO)

    # Split the images into train and val sets
    val_images = images[:num_val_images]

    for image_name in val_images:
        # Paths for image and annotation
        image_src = os.path.join(train_images_dir, image_name)
        annotation_src = os.path.join(train_annotations_dir, os.path.splitext(image_name)[0] + '.txt') # or adjust based on annotation format

        # Paths to move to
        image_dst = os.path.join(val_images_dir, image_name)
        annotation_dst = os.path.join(val_annotations_dir, os.path.splitext(image_name)[0] + '.txt')

        # Move image
        if os.path.exists(image_src):
            shutil.move(image_src, image_dst)

        # Move annotation if it exists
        if os.path.exists(annotation_src):
            shutil.move(annotation_src, annotation_dst)



if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print("Incorrect Args")
        print(sys.argv)
        exit(1)

    # first argument is the path to the perception output
    perception_path = sys.argv[1]

    # second argument is the path to the new dataset folder
    dataset_path = sys.argv[2]

    main(perception_path,dataset_path)