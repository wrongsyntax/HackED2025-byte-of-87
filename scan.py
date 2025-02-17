import RPi.GPIO as GPIO
import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
import time
import speak

# Setup
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM object with 50Hz frequency
# 50Hz is standard for most servos
pwm = GPIO.PWM(SERVO_PIN, 50)

# Define servo angle limits (in degrees)
MIN_ANGLE = 0
MAX_ANGLE = 180

current = 0

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

model = YOLO("models/fsd10e.pt")

# Keep track of the current duty cycle
current_dc = 0

def angle_to_duty_cycle(angle):
    # 2.5 is duty cycle for 0 degrees
    # 12.5 is duty cycle for 180 degrees
    return 2.5 + (angle / 180) * 10

def move_smooth(target_angle, step_delay=0.05):
    global current_dc
    
    # Calculate current angle from the current duty cycle
    current_angle = (current_dc - 2.5) * 180 / 10
    
    # Move in small steps
    step = 2  # degrees per step (smaller = smoother)
    if current_angle < target_angle:
        for angle in range(int(current_angle), int(target_angle), step):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            current_dc = dc  # Update current duty cycle
            time.sleep(step_delay)
    else:
        for angle in range(int(current_angle), int(target_angle), -step):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            current_dc = dc  # Update current duty cycle
            time.sleep(step_delay)
    
    # Final position
    pwm.ChangeDutyCycle(angle_to_duty_cycle(target_angle))
    current_dc = angle_to_duty_cycle(target_angle)  # Final update

try:
    # Start PWM
    pwm.start(0)
    
    while True:
        time.sleep(0.5)
        
        # Capture frame-by-frame
        frame = picam2.capture_array()

        # Run YOLO11 inference on the frame
        results = model.predict(source=frame, show=True, stream=True, verbose=False)

        for r in results:
            if len(r.boxes.cls) > 0:
                # Loop through all detected objects
                for i in range(len(r.boxes.cls)):
                    pred_idx = r.boxes.cls[i].item()
                    confidence = r.boxes.conf[i].item()
                    print(f"{i} => Class: {model.names.get(pred_idx)}, Confidence: {confidence:.2f}")
                    speak.fire_safety_advice(model.names.get(pred_idx))

            # Visualize the results on the frame
            annotated_frame = r.plot()

            # Display the resulting frame
            cv2.imshow("Camera", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break
        
        if current < MAX_ANGLE:
            current += 10
            move_smooth(current)
        else:
            move_smooth(MIN_ANGLE)
            current = 0
        
        time.sleep(2)

except KeyboardInterrupt:
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()
