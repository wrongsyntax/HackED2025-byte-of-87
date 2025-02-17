import subprocess

def speak(text, speed=130, pitch=15, voice="en"):
    """
    Uses espeak to convert text to speech.

    Parameters:
    - text (str): The text to speak.
    - speed (int): Speed of speech (default 150, lower is slower, higher is faster).
    - pitch (int): Pitch of speech (default 50, lower is deeper, higher is higher).
    - voice (str): Language/voice selection (default "en" for English).
    """
    subprocess.run(["espeak", f"-s{speed}", f"-p{pitch}", f"-v{voice}", text])


def fire_safety_advice(fire_type):
    """
    Provides safety advice based on fire type.
    
    Fire Types:
    - "electrical" -> Warns against using water.
    - "solid" -> Advises using water.
    - "chemical" -> Suggests using a fire extinguisher.
    - "oil" -> Warns against using water, suggests using a fire blanket.
    """
    advice = {
        "electrical": "Electrical fire detected. Do not put water on an electrical fire. Use a Class C fire extinguisher.",
        "solid": "Solid fire detected. Use water to extinguish it.",
        "chemical": "Chemical fire detected. Use a fire extinguisher labeled Class B or Class D.",
        "oil": "Oil fire detected Do not use water on an oil fire. Cover it with a fire blanket or use a Class K extinguisher."
    }
    
    message = advice.get(fire_type.lower(), "Unknown fire type detected. Follow safety protocols.")
    speak(message)



def main():
    """
    Main function to let the user choose the fire type and receive safety advice.
    """
    print("\nFire Safety Advisor")
    print("=====================")
    print("Choose the type of fire:")
    print("1. Electrical Fire")
    print("2. Solid Fire (Wood, Paper, etc.)")
    print("3. Chemical Fire")
    print("4. Oil Fire")
    print("5. Exit")

    while True:
        choice = input("\nEnter your choice (1-5): ").strip()

        fire_types = {
            "1": "electrical",
            "2": "solid",
            "3": "chemical",
            "4": "oil"
        }

        if choice == "5":
            print("\nStay safe! Exiting program.")
            speak("Stay safe! Exiting program.")
            break
        elif choice in fire_types:
            fire_safety_advice(fire_types[choice])
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            speak("Invalid choice. Please enter a valid number.")
            
        speak("Please procede to your nearest exit if you cannot safely fight it.")


if __name__ == "__main__":
    main()