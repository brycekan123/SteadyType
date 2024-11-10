from pynput import keyboard
import google.generativeai as genai
import time

class GlobalAutocorrect:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key="")
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Variables for text tracking
        self.current_text = ""
        self.last_typing_time = time.time()
        self.pause_duration = 2.0  # 2 seconds pause detection
        self.is_correcting = False
        self.has_typed = False  # New flag to track if user has typed anything
        
        # Create keyboard controller for simulating keystrokes
        self.keyboard_controller = keyboard.Controller()
        
    def start(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()
    
    def on_press(self, key):
        try:
            # Skip if currently performing a correction
            if self.is_correcting:
                return
            
            # Update last typing time
            self.last_typing_time = time.time()
            
            # Handle different key types
            if hasattr(key, 'char') and key.char:
                self.current_text += key.char
                self.has_typed = True  # Set flag when user types
            elif key == keyboard.Key.space:
                if self.has_typed:  # Only add space if user has typed something
                    self.current_text += " "
            elif key == keyboard.Key.enter:
                if self.has_typed:  # Only add newline if user has typed something
                    self.current_text += "\n"
            elif key == keyboard.Key.backspace:
                if self.current_text:
                    self.current_text = self.current_text[:-1]
                    if not self.current_text:  # Reset has_typed if all text is deleted
                        self.has_typed = False
            
            # Start checking for pause only if user has typed something
            if self.has_typed:
                self.start_pause_check()
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def on_release(self, key):
        pass
    
    def start_pause_check(self):
        # Start a background thread to continuously check for pause
        import threading
        if hasattr(self, 'pause_thread') and self.pause_thread.is_alive():
            return
            
        self.pause_thread = threading.Thread(target=self.check_pause)
        self.pause_thread.daemon = True
        self.pause_thread.start()
    
    def check_pause(self):
        while True:
            current_time = time.time()
            if (current_time - self.last_typing_time >= self.pause_duration and 
                self.current_text.strip() and not self.is_correcting and self.has_typed):
                self.correct_text()
                break
            elif not self.has_typed or not self.current_text.strip():
                break
            time.sleep(0.1)  # Check every 100ms
    
    def correct_text(self):
        try:
            self.is_correcting = True
            text = self.current_text.strip()
            if not text:
                self.is_correcting = False
                self.has_typed = False  # Reset typing flag
                return
            
            # Quick correction prompt
            prompt = f"Quick spelling and grammar correction only: {text}"
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                corrected_text = response.text.strip()
                
                # Only apply correction if there are changes
                if corrected_text.lower() != text.lower():
                    # Calculate number of backspaces needed
                    backspaces_needed = len(text)
                    
                    # Delete current text
                    for _ in range(backspaces_needed):
                        self.keyboard_controller.press(keyboard.Key.backspace)
                        self.keyboard_controller.release(keyboard.Key.backspace)
                        time.sleep(0.01)  # Small delay to ensure proper deletion
                    
                    # Type corrected text
                    self.keyboard_controller.type(corrected_text)
                    
                    print(f"Corrected: {corrected_text}")
                
            # Reset current text and typing flag
            self.current_text = ""
            self.has_typed = False
            
        except Exception as e:
            print(f"Error: {str(e)}")
            self.current_text = ""
            self.has_typed = False
        finally:
            self.is_correcting = False

def main():
    print("Global Autocorrect started. Press Ctrl+C to stop.")
    try:
        autocorrect = GlobalAutocorrect()
        autocorrect.start()
    except KeyboardInterrupt:
        print("\nGlobal Autocorrect stopped.")

if __name__ == "__main__":
    main()