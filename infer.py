import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

model = YOLO("models/fsd10e.pt")

"""
while True:
	results = model.predict(source=img, show=True, stream=True, verbose=False)

	for r in results:
		if len(r.boxes.cls) > 0:
			# Loop through all detected objects
			for i in range(len(r.boxes.cls)):
				pred_idx = r.boxes.cls[i].item()
				confidence = r.boxes.conf[i].item()
					print(f"{i} => Class: {model.names.get(pred_idx)}, Confidence: {confidence:.2f}")

	sleep(0.5)
	"""
	
while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Run YOLO11 inference on the frame
    results = model(frame)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()
