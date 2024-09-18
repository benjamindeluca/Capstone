from ultralytics import YOLO
import sys
import os

def main(path_to_model, path_to_data):
    # Load a YOLOv8 model, you can specify yolov8n, yolov8s, yolov8m, yolov8l, yolov8x based on your requirements
    model = YOLO(path_to_model)  # Create a new model from a config file or load a pretrained model

    for root, dirs, files in os.walk(path_to_data):

        for file in files:
            if file.endswith((".jpg",".png")):
                file_path = os.path.join(root,file)
                model(file_path,show=True,save=False)

    # Export the model to ONNX, TensorRT, CoreML, etc.
    model.export(format='onnx')  # export the trained model to ONNX format

if __name__ == '__main__':

    # input is to the data yaml file
    if (len(sys.argv)!=3):
        print("Incorrect Arguments")
        exit(1)
    else:
        path_to_model = sys.argv[1]
        path_to_data = sys.argv[2]
        if path_to_model.endswith('.pt'):
            main(path_to_model, path_to_data)
        else:
            print("Not a pt file")
            exit(1)
        
