import socket
import numpy as np
import cv2
import struct
import pickle

def receive_images():
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

                # Display the image
                if image is not None:
                    cv2.imshow('Received Image', image)
                    cv2.waitKey(1)  # 1 ms delay to keep the window responsive
                else:
                    print("Failed to decode the image data")
            else:
                print("Received incomplete image data")

    except KeyboardInterrupt:
        print("Server shutdown.")

    finally:
        # Clean up
        cv2.destroyAllWindows()
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    receive_images()