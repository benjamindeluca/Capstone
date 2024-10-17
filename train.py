from ultralytics import YOLO
import sys

def main(path_to_data):
    # Load a YOLOv8 model, you can specify yolov8n, yolov8s, yolov8m, yolov8l, yolov8x based on your requirements
    model = YOLO(r'C:\Users\Ben\Desktop\Uni\Capstone\Code\NonUnity\Capstone\runs\detect\Tuesday15th_LARGE-20241015T064752Z-001\Tuesday15th_LARGE\weights\DNF.pt')  # Create a new model from a config file or load a pretrained model

    # Train the model
    model.train(
        data=path_to_data,  # path to the data.yaml file
        epochs=1,  # number of training epochs
        patience=15,
        imgsz=640,  # image size
        batch=16,  # batch size
        name='resultsdata',  # experiment name
        verbose=True,
        plots=True,
        mosaic=0
    )

    # Evaluate the model on the validation set
    metrics = model.val()

    # Export the model to ONNX, TensorRT, CoreML, etc.
    # model.export(format='onnx')  # export the trained model to ONNX format

if __name__ == '__main__':

    # input is to the data yaml file
    if (len(sys.argv)!=2):
        print("Incorrect Arguments")
        exit(1)
    else:
        path_to_data = sys.argv[1]
        if path_to_data.endswith('.yaml'):
            main(path_to_data)
        else:
            print("Not a yaml file")
            exit(1)
        

