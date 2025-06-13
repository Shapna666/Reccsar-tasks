# chatbot.py
import tkinter as tk
from assets.style_utils import *

def open_chatbot(user_role):
    def respond():
        user_input = entry.get().lower()
        entry.delete(0, tk.END)

        if "course" in user_input:
            response = "There are 20 exciting courses available. Check them out on your dashboard!"
        elif "enroll" in user_input:
            response = "To enroll, just click the 'Enroll' button next to a course."
        elif "hello" in user_input or "hi" in user_input:
            response = f"Hello {user_role}! How can I assist you today?"
        else:
            response = "I'm still learning. Try asking about 'courses' or 'enroll'."

        chat_log.config(state='normal')
        chat_log.insert(tk.END, f"You: {user_input}\nBot: {response}\n\n")
        chat_log.config(state='disabled')
        chat_log.see(tk.END)

    bot = tk.Toplevel()
    bot.title(f"{user_role} Chatbot")
    bot.geometry("400x400")
    bot.configure(bg=BG_LIGHT)

    tk.Label(bot, text="LMS Chatbot 🤖", font=FONT_HEADER, bg=BG_LIGHT).pack(pady=10)

    chat_log = tk.Text(bot, height=15, width=45, font=FONT_NORMAL, state='disabled', wrap='word')
    chat_log.pack(pady=5)

    entry = tk.Entry(bot, font=FONT_NORMAL, width=30)
    entry.pack(pady=5)

    tk.Button(bot, text="Send", font=FONT_SMALL, bg=BUTTON_BLUE, fg=BUTTON_WHITE, command=respond).pack()

    bot.mainloop()
