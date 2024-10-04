from ultralytics import YOLO
import sys
import json
import socket
import cv2
import numpy as np
import struct

# updated to recieve images from the web socket

def main(path_to_model):

    # Load a YOLOv8 model, you can specify yolov8n, yolov8s, yolov8m, yolov8l, yolov8x based on your requirements
    model = YOLO(path_to_model)  # Create a new model from a config file or load a pretrained model

    # Setting up the socket

    # Setup socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    print("Waiting for connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    try:
        while True:
            # First, receive the length of the image data
            length_data = client_socket.recv(4)
            if not length_data:
                break

            # Unpack the length (as an integer)
            length = struct.unpack('!I', length_data)[0]

            # Now receive the actual image data based on the length
            data = b''
            while len(data) < length:
                packet = client_socket.recv(length - len(data))
                if not packet:
                    break
                data += packet

            if len(data) == length:
                print(f"Received complete image data of length: {len(data)}")
                # Convert the received bytes to an image
                image_array = np.frombuffer(data, dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                # Evaluate the model on the validation set
                results = model(image,show=True)

                result = results[0]

                print(type(result.boxes))


                with open("results.txt", "w") as fp:
                    for result in results:

                        boxes_list = []
                        for box in result.boxes:  # Assuming 'results' is iterable or contains multiple 'Boxes'
                            boxes_list.append({
                                "box": box.xyxy.tolist(),         # Get the bounding box coordinates (x_min, y_min, x_max, y_max)
                                "confidence": box.conf.tolist(),  # Get the confidence score as a list
                                "class": box.cls.tolist()         # Get the class label(s) as a list
                            })

                        print(f"Box List: {boxes_list}")

                        json.dump(boxes_list, fp, indent=4)  # 'indent=4' makes the JSON output pretty and readable

            else:
                print("Received incomplete image data")

    except KeyboardInterrupt:
        print("Server shutdown.")

    finally:
        # Clean up
        cv2.destroyAllWindows()
        client_socket.close()
        server_socket.close()

    

    # breakpoint()

if __name__ == '__main__':

    # input is to the data yaml file
    if (len(sys.argv)!=2):
        print("Incorrect Arguments")
        exit(1)
    else:
        path_to_data = sys.argv[1]
        if path_to_data.endswith('.pt'):
            main(path_to_data)
        else:
            print("Not a pt file")
            exit(1)
        

