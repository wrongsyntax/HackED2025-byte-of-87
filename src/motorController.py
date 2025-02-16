import threading
import time

fireDetected = threading.Event()  # Thread-safe event for fire detection
stopEvent = threading.Event()  # Event to stop the program manually

def spinCamera():
    """Camera keeps spinning until fire is detected or stop is triggered."""
    while not fireDetected.is_set() and not stopEvent.is_set():
        #print("Camera is spinning...")
        time.sleep(1)
    print("Camera stopped.")

def detectFire():
    """Detects fire or stops the program based on user input."""
    while not stopEvent.is_set():
        user_input = input("Enter 'yes' for fire or 'stop' to exit: ").strip().lower()
        if user_input == "yes":
            fireDetected.set()  # Stop camera due to fire
            print("🔥 Fire detected! Stopping the camera.")
            break
        elif user_input == "stop":
            stopEvent.set()  # Stop the entire program
            print("🛑 Stopping program.")
            break

def main():
    camera_thread = threading.Thread(target=spinCamera)
    fire_thread = threading.Thread(target=detectFire)
'''
    camera_thread.start()
    fire_thread.start()

    # Wait for fire detection or stop input
    fire_thread.join()

    # Ensure camera thread stops when the program is exiting
    camera_thread.join()
'''

if __name__ == "__main__":
    main()
