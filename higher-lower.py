import tkinter as tk
from tkinter import font
import random
from game_data import data

# --- Constants for Styling ---
BG_COLOR = "#f7f7f7"  # Lighter gray for a modern look
FRAME_BG = "#ffffff"
CORRECT_COLOR = "#e0f2f1"  # Soft teal
WRONG_COLOR = "#ffebee"   # Soft red
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#007bff"
FONT_NAME = "Segoe UI"  # A clean, modern font

# --- Dynamic Font Sizing ---
TITLE_FONT = (FONT_NAME, 26, "bold")
SCORE_FONT = (FONT_NAME, 16)
NAME_FONT = (FONT_NAME, 20, "bold")
DESC_FONT = (FONT_NAME, 14)
COUNTRY_FONT = (FONT_NAME, 13, "italic")
VS_FONT = (FONT_NAME, 32, "bold")
BUTTON_FONT = (FONT_NAME, 18, "bold")


class HigherLowerGUI:
    """A GUI for the Higher-Lower guessing game."""

    def __init__(self, root):
        """Initialize the game UI and variables."""
        self.root = root
        self.root.title("Higher or Lower")
        self.root.config(padx=50, pady=30, bg=BG_COLOR)
        self.root.minsize(800, 600)  # Set a minimum size

        # --- Game Variables ---
        self.score = 0
        self.account_a = None
        self.account_b = None

        # --- UI Widget Creation ---
        self.create_widgets()
        self.next_round()

    def create_widgets(self):
        """Creates and lays out all the graphical elements."""
        # --- Main Title ---
        title_label = tk.Label(
            self.root, text="Higher or Lower", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # --- Score Label ---
        self.score_label = tk.Label(
            self.root, text=f"Score: {self.score}", font=SCORE_FONT, bg=BG_COLOR, fg=ACCENT_COLOR
        )
        self.score_label.grid(row=1, column=1, pady=(0, 10))

        # --- Option A Frame ---
        self.frame_a = tk.Frame(self.root, bg=FRAME_BG, padx=30, pady=30, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", highlightthickness=1)
        self.label_a_name = tk.Label(self.frame_a, font=NAME_FONT, bg=FRAME_BG, fg=TEXT_COLOR)
        self.label_a_desc = tk.Label(self.frame_a, font=DESC_FONT, bg=FRAME_BG, fg=TEXT_COLOR, wraplength=280, justify="center")
        self.label_a_country = tk.Label(self.frame_a, font=COUNTRY_FONT, bg=FRAME_BG, fg=TEXT_COLOR)

        # --- Option B Frame ---
        self.frame_b = tk.Frame(self.root, bg=FRAME_BG, padx=30, pady=30, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", highlightthickness=1)
        self.label_b_name = tk.Label(self.frame_b, font=NAME_FONT, bg=FRAME_BG, fg=TEXT_COLOR)
        self.label_b_desc = tk.Label(self.frame_b, font=DESC_FONT, bg=FRAME_BG, fg=TEXT_COLOR, wraplength=280, justify="center")
        self.label_b_country = tk.Label(self.frame_b, font=COUNTRY_FONT, bg=FRAME_BG, fg=TEXT_COLOR)

        # --- 'VS' Label ---
        self.vs_label = tk.Label(text="VS", font=VS_FONT, bg=BG_COLOR, fg=TEXT_COLOR)

        # Pack items within frames
        for widget in (self.label_a_name, self.label_a_desc, self.label_a_country):
            widget.pack(pady=10)
        for widget in (self.label_b_name, self.label_b_desc, self.label_b_country):
            widget.pack(pady=10)

        # Grid layout for main elements
        self.frame_a.grid(row=2, column=0, sticky="nsew", padx=20)
        self.vs_label.grid(row=2, column=1, padx=20)
        self.frame_b.grid(row=2, column=2, sticky="nsew", padx=20)

        # Configure grid resizing behavior
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0) # VS label column doesn't stretch
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # --- Feedback Label ---
        self.feedback_label = tk.Label(
            self.root, text="Who has more followers?", font=SCORE_FONT, bg=BG_COLOR, pady=20, justify="center"
        )
        self.feedback_label.grid(row=3, column=0, columnspan=3)

        # --- Choice Buttons (Styled) ---
        # UPDATED: Button style changed for better text visibility.
        button_style = {
            "font": BUTTON_FONT,
            "bg": "white",                 # Light background
            "fg": ACCENT_COLOR,            # Dark text (blue)
            "activebackground": ACCENT_COLOR,  # Inverts on click
            "activeforeground": "white",       # Inverts on click
            "relief": "solid",
            "borderwidth": 2,
            "pady": 10,
            "cursor": "hand2"
        }
        self.button_a = tk.Button(self.root, text="A", **button_style, command=lambda: self.check_answer("a"))
        self.button_b = tk.Button(self.root, text="B", **button_style, command=lambda: self.check_answer("b"))
        self.button_a.grid(row=4, column=0, pady=20, sticky="ew", padx=20)
        self.button_b.grid(row=4, column=2, pady=20, sticky="ew", padx=20)

        # --- Play Again Button (hidden initially) ---
        self.play_again_button = tk.Button(
            self.root, text="Play Again", **button_style, command=self.reset_game
        )

    def format_data_for_display(self, account):
        """Extracts data from the account dictionary."""
        return (
            account["name"],
            f'A {account["description"]}',
            f'From {account["country"]}'
        )

    def next_round(self):
        """Sets up the next comparison for the user."""
        self.root.config(bg=BG_COLOR)
        # Simplified color reset logic
        for widget in (self.feedback_label, self.score_label, self.vs_label):
            widget.config(bg=BG_COLOR)
        
        for frame in (self.frame_a, self.frame_b):
            frame.config(bg=FRAME_BG)
            for widget in frame.winfo_children():
                widget.config(bg=FRAME_BG)

        self.feedback_label.config(text="Who has more followers?")
        self.button_a.config(state="normal")
        self.button_b.config(state="normal")
        self.play_again_button.grid_forget()

        self.account_a = self.account_b if self.account_b else random.choice(data)
        self.account_b = random.choice(data)
        while self.account_a == self.account_b:
            self.account_b = random.choice(data)

        name_a, desc_a, country_a = self.format_data_for_display(self.account_a)
        self.label_a_name.config(text=name_a)
        self.label_a_desc.config(text=desc_a)
        self.label_a_country.config(text=country_a)

        name_b, desc_b, country_b = self.format_data_for_display(self.account_b)
        self.label_b_name.config(text=name_b)
        self.label_b_desc.config(text=desc_b)
        self.label_b_country.config(text=country_b)

        self.score_label.config(text=f"Score: {self.score}")

    def check_answer(self, user_guess):
        """Checks if the user's guess is correct."""
        self.button_a.config(state="disabled")
        self.button_b.config(state="disabled")

        a_followers = self.account_a["follower_count"]
        b_followers = self.account_b["follower_count"]
        
        is_correct = (a_followers > b_followers and user_guess == "a") or (b_followers > a_followers and user_guess == "b")

        if is_correct:
            self.score += 1
            self.update_colors(CORRECT_COLOR)
            self.feedback_label.config(text="✅ Correct!")
            self.root.after(1500, self.next_round)
        else:
            self.update_colors(WRONG_COLOR)
            final_text = (
                f"❌ Sorry, that's wrong.\n"
                f"{self.account_a['name']}: {a_followers:,}M vs "
                f"{self.account_b['name']}: {b_followers:,}M\n"
                f"Final Score: {self.score}"
            )
            self.feedback_label.config(text=final_text)
            self.play_again_button.grid(row=5, column=0, columnspan=3, pady=20)
    
    def update_colors(self, color):
        """Updates the background color of relevant widgets."""
        self.root.config(bg=color)
        for widget in (self.feedback_label, self.score_label, self.vs_label):
            widget.config(bg=color)
        for frame in (self.frame_a, self.frame_b):
            frame.config(bg=color)
            for child in frame.winfo_children():
                child.config(bg=color)

    def reset_game(self):
        """Resets the game to its initial state."""
        self.score = 0
        self.account_b = None
        self.next_round()


# --- Main Execution ---
if __name__ == "__main__":
    window = tk.Tk()
    app = HigherLowerGUI(window)
    window.mainloop()

