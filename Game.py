import tkinter as tk
from tkinter import messagebox
import random, csv, os

# This sets the number of seconds for each round.
TIME_LIMIT = 15
# This sets how many rounds are played each game.
ROUNDS = 5
# This stores usernames.
USERS_FILE = "users.csv"
# This stores leaderboard scores.
SCORES_FILE = "leaderboard.csv"
# This sets the main background color.
BG = "#8b0000"
# This sets the clue card color.
CARD = "#a61c1c"
# This sets the button color.
BTN = "#cc2b2b"
# This sets the text color.
TXT = "white"

# This list stores the songs, clue lines, and genres.
SONGS = [
    {"title": "No Scrubs", "clue": "Hanging out the passenger side", "genre": "R&B"},
    {"title": "Say My Name", "clue": "If no one is around you", "genre": "R&B"},
    {"title": "Foolish", "clue": "See my days are cold without you", "genre": "R&B"},
    {"title": "Me & U", "clue": "Tell me if you want me to", "genre": "R&B"},
    {"title": "You", "clue": "Is it the shoes", "genre": "R&B"},
    {"title": "1, 2 Step", "clue": "Automatic supersonic hypnotic funky fresh", "genre": "R&B"},
    {"title": "We Belong Together", "clue": "When you left I lost a part of me", "genre": "R&B"},
    {"title": "Confessions Part II", "clue": "Man I'm throwing and I don't know what to do", "genre": "R&B"},
    {"title": "Adorn", "clue": "Baby these fists will always protect ya", "genre": "R&B"},
    {"title": "Best Part", "clue": "You don't know babe", "genre": "R&B"},
    {"title": "Can We Talk", "clue": "For a minute girl I want to know your name", "genre": "R&B"},
    {"title": "Irreplaceable", "clue": "Standing in the front yard telling me", "genre": "R&B"},
    {"title": "Ms. Officer", "clue": "I know taste like candy", "genre": "Rap"},
    {"title": "California Love", "clue": "Out on bail fresh out of jail", "genre": "Rap"},
    {"title": "Mind Playing Tricks on Me", "clue": "At night I can't sleep", "genre": "Rap"},
    {"title": "Rather Be Ya Nigga", "clue": "For the rest of your life", "genre": "Rap"},
    {"title": "Will I See You Again", "clue": "Memories running through my brain", "genre": "Rap"},
    {"title": "Norte Sidin'", "clue": "Still posted with the homies", "genre": "West Coast"},
    {"title": "Bay Luv", "clue": "All I know is that bay love", "genre": "West Coast"},
    {"title": "Lost", "clue": "Trying to find my way through the dark", "genre": "West Coast"},
    {"title": "Hey There Delilah", "clue": "What's it like in New York City", "genre": "Pop"},
    {"title": "Under the Bridge", "clue": "Sometimes I feel like I don't have a partner", "genre": "Rock"},
    {"title": "I Want You Back", "clue": "When I had you to myself", "genre": "Oldies"},
    {"title": "I Like the Way You Love Me", "clue": "You got me running", "genre": "Oldies"},
    {"title": "I Love You for All Seasons", "clue": "Winter spring summer fall", "genre": "Oldies"}
]

# This cleans text before comparing answers.
def clean(text):
    # This removes extra spaces and ignores capital letters.
    return " ".join(text.lower().strip().split())

# This creates the needed CSV files.
def ensure_files():
    # This creates the username file if it does not exist.
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["username"])
    # This creates the leaderboard file if it does not exist.
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["username", "score", "genre", "mode"])

# This class runs the whole game.
class SongGame:
    # This starts the window and variables.
    def __init__(self, root):
        # This stores the main window.
        self.root = root
        # This sets the title bar text.
        root.title("Song Challenge Game")
        # This sets the window size.
        root.geometry("920x650")
        # This sets the background color.
        root.configure(bg=BG)
        # This makes sure the CSV files exist.
        ensure_files()

        # This stores the username.
        self.username = ""
        # This stores the selected game mode.
        self.mode = tk.StringVar(value="Typed")
        # This stores the selected genre.
        self.genre = tk.StringVar(value="All")
        # This stores the score.
        self.score = 0
        # This stores the round number.
        self.round_num = 0
        # This stores the timer value.
        self.time_left = TIME_LIMIT
        # This stores the timer id.
        self.timer_id = None
        # This stores the current song.
        self.current = None
        # This stores the songs remaining in the game.
        self.pool = []
        # This stores how many rounds will be played.
        self.max_rounds = 0

        # This creates the main frame.
        self.frame = tk.Frame(root, bg=BG)
        # This places the main frame.
        self.frame.pack(fill="both", expand=True)
        # This shows the login screen first.
        self.login_screen()

    # This clears the current screen.
    def clear(self):
        # This removes every widget from the frame.
        for w in self.frame.winfo_children():
            w.destroy()
        # This stops the timer when changing screens.
        self.stop_timer()

    # This creates a centered container.
    def box(self):
        # This makes a centered frame.
        b = tk.Frame(self.frame, bg=BG)
        # This places the centered frame.
        b.pack(expand=True)
        # This returns the centered frame.
        return b

    # This makes a styled button.
    def button(self, parent, text, command, width=20):
        # This returns one red button.
        return tk.Button(parent, text=text, command=command, width=width, bg=BTN, fg=TXT, activebackground="#b91c1c", activeforeground=TXT, font=("Arial", 12, "bold"))

    # This shows the login screen.
    def login_screen(self):
        # This clears the screen.
        self.clear()
        # This creates a centered box.
        b = self.box()
        # This shows the title.
        tk.Label(b, text="Song Challenge Game", font=("Arial", 28, "bold"), bg=BG, fg=TXT).pack(pady=20)
        # This asks for a username.
        tk.Label(b, text="Enter Username", font=("Arial", 13), bg=BG, fg=TXT).pack(pady=8)
        # This creates the username entry.
        self.name_entry = tk.Entry(b, font=("Arial", 14), width=24, justify="center")
        # This places the username entry.
        self.name_entry.pack(pady=10)
        # This places the cursor in the entry.
        self.name_entry.focus()
        # This adds the continue button.
        self.button(b, "Continue", self.login_user).pack(pady=8)
        # This adds the leaderboard button.
        self.button(b, "Leaderboard", self.show_leaderboard).pack(pady=8)

    # This saves a username if it is new.
    def save_user(self, name):
        # This stores all saved usernames.
        seen = set()
        # This opens the users file.
        with open(USERS_FILE, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seen.add(row.get("username", "").lower())
        # This adds the username if it was not saved before.
        if name.lower() not in seen:
            with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([name])

    # This handles the login button.
    def login_user(self):
        # This gets the entered username.
        name = self.name_entry.get().strip()
        # This checks for an empty username.
        if not name:
            messagebox.showerror("Error", "Please enter a username.")
            return
        # This stores the username.
        self.username = name
        # This saves the username.
        self.save_user(name)
        # This opens the menu screen.
        self.menu_screen()

    # This shows the menu screen.
    def menu_screen(self):
        # This clears the screen.
        self.clear()
        # This creates a centered box.
        b = self.box()
        # This shows the welcome message.
        tk.Label(b, text=f"Welcome, {self.username}", font=("Arial", 24, "bold"), bg=BG, fg=TXT).pack(pady=20)
        # This shows the mode label.
        tk.Label(b, text="Mode", bg=BG, fg=TXT).pack()
        # This lets the user choose typed or multiple choice mode.
        tk.OptionMenu(b, self.mode, "Typed", "Multiple Choice").pack(pady=6)
        # This shows the genre label.
        tk.Label(b, text="Genre", bg=BG, fg=TXT).pack()
        # This lets the user choose a genre.
        tk.OptionMenu(b, self.genre, "All", "R&B", "Rap", "West Coast", "Pop", "Rock", "Oldies").pack(pady=6)
        # This adds the start button.
        self.button(b, "Start Game", self.start_game).pack(pady=8)
        # This adds the leaderboard button.
        self.button(b, "Leaderboard", self.show_leaderboard).pack(pady=8)
        # This adds the logout button.
        self.button(b, "Logout", self.login_screen).pack(pady=8)

    # This starts a new game.
    def start_game(self):
        # This filters songs by the chosen genre.
        self.pool = [s for s in SONGS if self.genre.get() == "All" or s["genre"] == self.genre.get()]
        # This shows an error if no songs match.
        if not self.pool:
            messagebox.showerror("No Songs", "No songs match that genre.")
            return
        # This shuffles the song order.
        random.shuffle(self.pool)
        # This resets the score.
        self.score = 0
        # This resets the round number.
        self.round_num = 0
        # This sets the round limit.
        self.max_rounds = min(ROUNDS, len(self.pool))
        # This begins the first round.
        self.next_round()

    # This moves to the next round.
    def next_round(self):
        # This ends the game if there are no rounds left.
        if self.round_num >= self.max_rounds or not self.pool:
            self.end_game()
            return
        # This gets the next song without repeating it.
        self.current = self.pool.pop(0)
        # This increases the round number.
        self.round_num += 1
        # This resets the timer.
        self.time_left = TIME_LIMIT
        # This shows the game screen.
        self.game_screen()
        # This starts the timer.
        self.run_timer()

    # This shows the game screen.
    def game_screen(self):
        # This clears the screen.
        self.clear()
        # This creates a centered box.
        b = self.box()
        # This shows the username, round, and score.
        tk.Label(b, text=f"{self.username}  |  Round {self.round_num}/{self.max_rounds}  |  Score {self.score}", font=("Arial", 14, "bold"), bg=BG, fg=TXT).pack(pady=10)
        # This creates the timer label.
        self.timer_label = tk.Label(b, text=f"Time Left: {self.time_left}", font=("Arial", 15, "bold"), bg=BG, fg="#ffd54f")
        # This places the timer label.
        self.timer_label.pack(pady=8)
        # This shows the clue card.
        tk.Label(b, text=f'"{self.current["clue"]}"', font=("Arial", 20, "italic"), wraplength=650, justify="center", bg=CARD, fg=TXT, padx=20, pady=20).pack(pady=20)

        # This checks if typed mode is selected.
        if self.mode.get() == "Typed":
            # This creates the answer entry.
            self.answer_entry = tk.Entry(b, font=("Arial", 14), width=28, justify="center")
            # This places the answer entry.
            self.answer_entry.pack(pady=10)
            # This places the cursor in the answer entry.
            self.answer_entry.focus()
            # This adds the submit button.
            self.button(b, "Submit", self.check_typed).pack(pady=8)
        else:
            # This shows the multiple choice answers.
            self.show_choices(b)

    # This shows the multiple choice buttons.
    def show_choices(self, parent):
        # This gets all wrong answer titles.
        wrong = [s["title"] for s in SONGS if s["title"] != self.current["title"]]
        # This picks up to three wrong answers.
        picks = random.sample(wrong, min(3, len(wrong)))
        # This combines the wrong answers with the correct answer.
        choices = picks + [self.current["title"]]
        # This shuffles the answer order.
        random.shuffle(choices)
        # This creates one button for each answer choice.
        for title in choices:
            self.button(parent, title, lambda value=title: self.check_choice(value), width=28).pack(pady=5)

    # This checks the typed answer.
    def check_typed(self):
        # This stops the timer.
        self.stop_timer()
        # This compares the typed answer with the real title.
        if clean(self.answer_entry.get()) == clean(self.current["title"]):
            # This adds points for a correct answer.
            self.score += 100
            messagebox.showinfo("Correct", "Correct!")
        else:
            # This shows the correct answer.
            messagebox.showinfo("Wrong", f"Answer: {self.current['title']}")
        # This goes to the next round.
        self.next_round()

    # This checks the multiple choice answer.
    def check_choice(self, choice):
        # This stops the timer.
        self.stop_timer()
        # This compares the chosen answer with the real title.
        if clean(choice) == clean(self.current["title"]):
            # This adds points for a correct answer.
            self.score += 100
            messagebox.showinfo("Correct", "Correct!")
        else:
            # This shows the correct answer.
            messagebox.showinfo("Wrong", f"Answer: {self.current['title']}")
        # This goes to the next round.
        self.next_round()

    # This updates the timer every second.
    def run_timer(self):
        # This updates the timer text.
        self.timer_label.config(text=f"Time Left: {self.time_left}")
        # This checks whether time ran out.
        if self.time_left <= 0:
            # This shows the correct answer when time ends.
            messagebox.showinfo("Time Up", f"Answer: {self.current['title']}")
            # This goes to the next round.
            self.next_round()
            return
        # This lowers the timer by one.
        self.time_left -= 1
        # This schedules the timer again.
        self.timer_id = self.root.after(1000, self.run_timer)

    # This stops the timer safely.
    def stop_timer(self):
        # This cancels the timer if one exists.
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    # This saves the final score.
    def save_score(self):
        # This writes the score row to the leaderboard file.
        with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([self.username, self.score, self.genre.get(), self.mode.get()])

    # This shows the leaderboard screen.
    def show_leaderboard(self):
        # This clears the screen.
        self.clear()
        # This creates a centered box.
        b = self.box()
        # This shows the leaderboard title.
        tk.Label(b, text="Leaderboard", font=("Arial", 26, "bold"), bg=BG, fg=TXT).pack(pady=20)
        # This reads all saved score rows.
        with open(SCORES_FILE, "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        # This sorts the rows by score from highest to lowest.
        rows.sort(key=lambda row: int(row.get("score", 0) or 0), reverse=True)
        # This shows the scores if any exist.
        if rows:
            for i, row in enumerate(rows[:10], 1):
                username = row.get("username", "Unknown")
                score = row.get("score", "0")
                genre = row.get("genre", "N/A")
                mode = row.get("mode", "N/A")
                tk.Label(b, text=f"{i}. {username} - {score} pts - {genre} - {mode}", font=("Arial", 12), bg=BG, fg=TXT).pack(pady=3)
        else:
            # This shows a message if there are no scores yet.
            tk.Label(b, text="No scores yet.", font=("Arial", 13), bg=BG, fg=TXT).pack(pady=5)
        # This chooses where the back button goes.
        back = self.menu_screen if self.username else self.login_screen
        # This adds the back button.
        self.button(b, "Back", back).pack(pady=20)

    # This shows the game over screen.
    def end_game(self):
        # This clears the screen.
        self.clear()
        # This saves the score.
        self.save_score()
        # This creates a centered box.
        b = self.box()
        # This shows the game over title.
        tk.Label(b, text="Game Over", font=("Arial", 28, "bold"), bg=BG, fg=TXT).pack(pady=25)
        # This shows the final score.
        tk.Label(b, text=f"{self.username}, your final score is {self.score}", font=("Arial", 16), bg=BG, fg=TXT).pack(pady=10)
        # This adds the play again button.
        self.button(b, "Play Again", self.menu_screen).pack(pady=8)
        # This adds the leaderboard button.
        self.button(b, "Leaderboard", self.show_leaderboard).pack(pady=8)

# This starts the program.
if __name__ == "__main__":
    # This creates the main window.
    root = tk.Tk()
    # This starts the app.
    SongGame(root)
    # This keeps the window running.
    root.mainloop()
