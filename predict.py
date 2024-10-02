from ultralytics import YOLO
import sys

def main(path_to_model, image):
    # Load a YOLOv8 model, you can specify yolov8n, yolov8s, yolov8m, yolov8l, yolov8x based on your requirements
    model = YOLO(path_to_model)  # Create a new model from a config file or load a pretrained model

    # Evaluate the model on the validation set
    results = model(image,show=True)

    print(results)

    breakpoint()

if __name__ == '__main__':

    # input is to the data yaml file
    if (len(sys.argv)!=3):
        print("Incorrect Arguments")
        exit(1)
    else:
        path_to_data = sys.argv[1]
        image = sys.argv[2]
        if path_to_data.endswith('.pt') and image.endswith(('.jpg','.png')):
            main(path_to_data,image)
        else:
            print("Not a pt file")
            exit(1)
        

