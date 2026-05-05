import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x500")

        # 1. Список предопределённых цитат
        self.quotes = [
            {"text": "Жизнь — это то, что случается с тобой, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Успех — это идти от ошибки к ошибке, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Единственный способ делать великие дела — любить то, что вы делаете.", "author": "Стив Джобс", "theme": "Работа"},
        ]
        self.history = []
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Блок отображения цитаты
        self.quote_label = tk.Label(self.root, text="Нажмите кнопку для получения цитаты", wraplength=500, font=("Arial", 12, "italic"))
        self.quote_label.pack(pady=20)

        self.author_label = tk.Label(self.root, text="", font=("Arial", 10, "bold"))
        self.author_label.pack()

        # Кнопка генерации
        self.gen_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.gen_btn.pack(pady=10)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Фильтр (Автор/Тема):").pack(side=tk.LEFT)
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(filter_frame, text="Применить", command=self.apply_filter).pack(side=tk.LEFT)

        # История
        tk.Label(self.root, text="История цитат:").pack()
        self.history_listbox = tk.Listbox(self.root, width=70, height=10)
        self.history_listbox.pack(pady=5, padx=10)
        
        self.update_history_display()

    def generate_quote(self):
        # 2. Выбор случайной цитаты
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["text"]}"')
        self.author_label.config(text=f"— {quote['author']} ({quote['theme']})")
        
        # 3. Добавление в историю
        self.history.append(quote)
        self.update_history_display()
        self.save_history()

    def update_history_display(self, filtered_list=None):
        self.history_listbox.delete(0, tk.END)
        display_list = filtered_list if filtered_list is not None else self.history
        for q in display_list:
            self.history_listbox.insert(tk.END, f"[{q['theme']}] {q['author']}: {q['text'][:40]}...")

    def apply_filter(self):
        # 4. Реализация фильтрации
        query = self.filter_entry.get().lower()
        if not query:
            self.update_history_display()
            return
        
        filtered = [q for q in self.history if query in q['author'].lower() or query in q['theme'].lower()]
        self.update_history_display(filtered)

    def save_history(self):
        # 5. Сохранение в JSON
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        # 5. Загрузка из JSON
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
