import RPi.GPIO as GPIO
import time

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

# Convert angle to duty cycle
def angle_to_duty_cycle(angle):
    # 2.5 is duty cycle for 0 degrees
    # 12.5 is duty cycle for 180 degrees
    return 2.5 + (angle/180) * 10

def move_smooth(target_angle, step_delay=0.05):
    # Get current angle (approximate)
    current_dc = pwm.ChangeDutyCycle(0)  # Get current duty cycle
    current_angle = (current_dc - 2.5) * 180/10 if current_dc else 0
    
    # Move in small steps
    step = 2  # degrees per step (smaller = smoother)
    if current_angle < target_angle:
        for angle in range(int(current_angle), int(target_angle), step):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(step_delay)
    else:
        for angle in range(int(current_angle), int(target_angle), -step):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(step_delay)
    
    # Final position
    pwm.ChangeDutyCycle(angle_to_duty_cycle(target_angle))

try:
    # Start PWM
    pwm.start(0)
    
    while True:
        move_smooth(MAX_ANGLE)
        time.sleep(1)
        move_smooth(MIN_ANGLE)
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
