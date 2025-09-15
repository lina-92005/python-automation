import pyttsx3
import speech_recognition as sr
import threading
import os

def save_audio_thread(text, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()

def text_to_speech():
    while True:
        print("\nChoose text input method:")
        print("1. Type text")
        print("2. Read from a text file")
        text_choice = input("Enter 1 or 2: ").strip()

        if text_choice == "1":
            text = input("Enter the text to convert to speech: ").strip()
            if text:
                break
            else:
                print("❌ No text entered. Please try again.")
        elif text_choice == "2":
            filename = input("Enter the path to your text file: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                if text:
                    break
                else:
                    print("❌ Text file is empty. Please try again.")
            except FileNotFoundError:
                print("❌ File not found. Please try again.")
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

    # Speak live audio
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

    # Save audio
    save_choice = input("Do you want to save this audio? (y/n): ").strip().lower()
    if save_choice == "y":
        output_name = input("Enter filename (without extension, will be .wav): ").strip()
        if not output_name:
            output_name = "output"
        output_path = os.path.abspath(f"{output_name}.wav")

        # Run saving in a separate thread to prevent freeze
        thread = threading.Thread(target=save_audio_thread, args=(text, output_path))
        thread.start()
        
        print(f"✅ Audio successfully saved as '{output_path}'")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"✅ You said: {text}")

        # Save text
        save_choice = input("Do you want to save this text? (y/n): ").strip().lower()
        if save_choice == "y":
            output_name = input("Enter filename (without extension, will be .txt): ").strip()
            if not output_name:
                output_name = "recognized_text"
            output_path = os.path.abspath(f"{output_name}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Text successfully saved as '{output_path}'")

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ Error from Google API: {e}")

def main():
    while True:
        print("\nChoose mode:")
        print("1. Text-to-Speech (TTS / DTS)")
        print("2. Speech-to-Text (STT / SCT)")
        print("3. Exit")
        mode = input("Enter 1, 2, or 3: ").strip()

        if mode == "1":
            text_to_speech()
        elif mode == "2":
            speech_to_text()
        elif mode == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
