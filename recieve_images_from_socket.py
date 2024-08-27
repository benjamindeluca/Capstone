import socket
import numpy as np
import cv2

def receive_image():
    # Setup socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    print("Waiting for connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Receive the data
    data = b''
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    # Convert the received bytes to an image
    image_array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Received Image', image)
    cv2.waitKey(0)

    # Clean up
    cv2.destroyAllWindows()
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    receive_image()