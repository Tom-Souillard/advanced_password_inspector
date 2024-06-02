import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Any
from advanced_password_inspector.core.password_evaluator import evaluate_password

class PasswordInspectorApp(tk.Tk):
    """
    A simple GUI application using Tkinter to evaluate password strength,
    check for breaches, and estimate crack time for the 'Advanced Password Inspector'.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.title('Advanced Password Inspector')
        self.geometry('500x400')  # Adjust size as needed

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Creates the widgets for the application interface.
        """
        label = tk.Label(self, text="Enter Password:", font=('Helvetica', 12))
        label.pack(pady=10)

        self.entry = tk.Entry(self, show='*', width=30, font=('Helvetica', 12))
        self.entry.pack(pady=10)

        evaluate_button = tk.Button(self, text="Evaluate Password", command=self.evaluate_password)
        evaluate_button.pack(pady=20)

        self.result_text = scrolledtext.ScrolledText(self, height=10, width=50)
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

    def evaluate_password(self) -> None:
        """
        Evaluates the entered password and updates the result text widget with the results.
        """
        password = self.entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password to evaluate.")
            return

        try:
            results = evaluate_password(password)
            message = (
                f"Password Strength: {results['password_strength']['score']}\n"
                f"Breach Status: {'Breached' if results['breach_check'] else 'Safe'}\n"
                f"Crack Time: {results['crack_time']}\n"
                f"Suggestions: {' '.join(results['password_strength']['feedback']['suggestions'])}"
            )
        except Exception as e:
            message = f"Error: {str(e)}"

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = PasswordInspectorApp()
    app.mainloop()
