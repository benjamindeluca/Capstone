from ultralytics import YOLO
import sys

def main(path_to_data):
    # Load a YOLOv8 model, you can specify yolov8n, yolov8s, yolov8m, yolov8l, yolov8x based on your requirements
    model = YOLO('yolov8n.yaml')  # Create a new model from a config file or load a pretrained model

    # Train the model
    model.train(
        data=path_to_data,  # path to the data.yaml file
        epochs=100,  # number of training epochs
        patience=15,
        imgsz=640,  # image size
        batch=16,  # batch size
        name='yolov8_newsharks_newpeeps',  # experiment name
        verbose=True,
        plots=True,
        mosaic=0
    )

    # Evaluate the model on the validation set
    metrics = model.val()

    # Export the model to ONNX, TensorRT, CoreML, etc.
    model.export(format='onnx')  # export the trained model to ONNX format

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
        

