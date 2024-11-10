import tkinter as tk
from tkinter import ttk, scrolledtext
import google.generativeai as genai
from threading import Timer

class AutocorrectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Autocorrect")
        self.root.geometry("800x600")
        
        # Configure Gemini
        genai.configure(api_key="")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Variables
        self.typing_timer = None
        self.correction_delay = 2000  # 2 seconds
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=('Arial', 12),
            height=20
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            main_frame, 
            text="Type to begin...", 
            font=('Arial', 10)
        )
        self.status_label.pack(fill=tk.X)
        
        # Bind events
        self.text_area.bind('<Key>', self.on_type)
        
    def on_type(self, event):
        # Reset the timer on each keystroke
        if self.typing_timer:
            self.typing_timer.cancel()
            
        # Start a new timer
        self.typing_timer = Timer(2.0, self.check_text)
        self.typing_timer.start()
        self.status_label.config(text="Waiting for you to finish typing...")
        
    def check_text(self):
        try:
            # Get current text
            text = self.text_area.get("1.0", tk.END).strip()
            if not text:
                return
                
            self.status_label.config(text="Checking text...")
            
            # First, check if the text is gibberish
            gibberish_prompt = f"""Determine if this text is gibberish or meaningful text. 
            Only respond with either 'GIBBERISH' or 'MEANINGFUL':
            Text: {text}"""
            
            gibberish_check = self.model.generate_content(gibberish_prompt)
            
            if 'GIBBERISH' in gibberish_check.text.upper():
                self.status_label.config(text="Can't understand")
                return
            
            # If text is meaningful, proceed with correction
            prompt = f"Correct this text, fixing any spelling or grammar errors. If it's already correct, return it unchanged: {text}"
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                corrected_text = response.text.strip()
                
                # Only update if there are actual changes
                if corrected_text.lower() != text.lower():
                    # Save cursor position
                    cursor_pos = self.text_area.index(tk.INSERT)
                    
                    # Update text
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", corrected_text)
                    
                    # Restore cursor position
                    try:
                        self.text_area.mark_set(tk.INSERT, cursor_pos)
                    except:
                        pass
                        
                    self.status_label.config(text="Text corrected!")
                else:
                    self.status_label.config(text="No corrections needed.")
                    
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = AutocorrectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()