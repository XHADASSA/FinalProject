# import cv2
#
# def camera():
#     # Initialize the camera
#     cap = cv2.VideoCapture(0)  # 0 represents the camera index (usually the built-in camera)
#
#     # Check if the camera is opened successfully
#     if not cap.isOpened():
#         raise Exception("Could not open the camera")
#
#     # Capture a single frame (image)
#     ret, frame = cap.read()
#
#     # Define the path where the image will be saved
#     image_path = 'captured_image.jpg'
#
#     # Save the captured image
#     cv2.imwrite(image_path, frame)
#
#     # Release the camera
#     cap.release()
#     return image_path
# image_path=camera()
import cv2

def camera():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 represents the camera index (usually the built-in camera)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        raise Exception("Could not open the camera")

    # Capture a single frame (image)
    ret, frame = cap.read()

    # Define the path where the image will be saved
    image_path = 'captured_image.jpg'

    # Save the captured image
    cv2.imwrite(image_path, frame)

    # Release the camera
    cap.release()

    # Print the path where the image is saved
    print("Image saved at:", image_path)
