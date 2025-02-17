from ultralytics import YOLO
import cv2
import time

CROP_LENGTH = 100

model = YOLO("best.pt")
results = model("images.jpg", conf=0.2)  # Make sure the image path is correct

image_path = "images.jpg"
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    exit()

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break


    height, width, _ = img.shape
    x_center = width // 2
    x_start, x_end = x_center - (CROP_LENGTH // 2), x_center + (CROP_LENGTH // 2)

    cropped_img = img[:, x_start:x_end]

    # Run YOLO on cropped image
    results = model(cropped_img, conf=0.10)

    class_names = model.names

    fire_detected = False
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # Get the class ID of the detected object
            class_name = class_names[class_id]

            if class_name.lower() == "fire":  # Check if 'fire' is detected
                fire_detected = True
                break

    print(fire_detected)

    # Draw detections on the frame
    annotated_frame = results[0].plot()  # This overlays bounding boxes on the image

    # Show the output video with detections
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Press 'q' to exit
    time.sleep(.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()