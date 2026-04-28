import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Файл для хранения данных
        self.data_file = "movies.json"
        self.movies = []
        
        # Загрузка данных
        self.load_movies()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.update_table()
    
    def create_widgets(self):
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов для строк и столбцов
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавление фильма", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Поля ввода
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.genre_entry = ttk.Entry(input_frame, width=40)
        self.genre_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.year_entry = ttk.Entry(input_frame, width=40)
        self.year_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.rating_entry = ttk.Entry(input_frame, width=40)
        self.rating_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.filter_genre = ttk.Entry(filter_frame, width=20)
        self.filter_genre.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.filter_year = ttk.Entry(filter_frame, width=20)
        self.filter_year.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        self.filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, padx=5)
        
        self.clear_filter_button = ttk.Button(filter_frame, text="Сбросить", command=self.clear_filter)
        self.clear_filter_button.grid(row=0, column=5, padx=5)
        
        # Фрейм для таблицы
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Таблица
        columns = ('Название', 'Жанр', 'Год', 'Рейтинг')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настройка заголовков
        self.tree.heading('Название', text='Название')
        self.tree.heading('Жанр', text='Жанр')
        self.tree.heading('Год', text='Год выпуска')
        self.tree.heading('Рейтинг', text='Рейтинг')
        
        # Настройка ширины колонок
        self.tree.column('Название', width=300)
        self.tree.column('Жанр', width=200)
        self.tree.column('Год', width=100)
        self.tree.column('Рейтинг', width=100)
        
        # Добавление скроллбаров
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Размещение элементов
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.delete_button = ttk.Button(button_frame, text="Удалить выбранный", command=self.delete_movie)
        self.delete_button.grid(row=0, column=0, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Сохранить", command=self.save_movies)
        self.save_button.grid(row=0, column=1, padx=5)
        
        self.load_button = ttk.Button(button_frame, text="Загрузить", command=self.load_movies)
        self.load_button.grid(row=0, column=2, padx=5)
        
        # Статус бар
        self.status_label = ttk.Label(main_frame, text=f"Всего фильмов: {len(self.movies)}", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def validate_input(self, year, rating):
        """Проверка корректности ввода"""
        errors = []
        
        # Проверка года
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1888 or year_int > current_year:
                errors.append(f"Год должен быть между 1888 и {current_year}")
        except ValueError:
            errors.append("Год должен быть числом")
        
        # Проверка рейтинга
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                errors.append("Рейтинг должен быть от 0 до 10")
        except ValueError:
            errors.append("Рейтинг должен быть числом")
        
        return errors
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        # Проверка на пустые поля
        if not all([title, genre, year, rating]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        # Валидация
        errors = self.validate_input(year, rating)
        if errors:
            messagebox.showerror("Ошибка валидации", "\n".join(errors))
            return
        
        # Добавление фильма
        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }
        
        self.movies.append(movie)
        self.save_movies()
        self.update_table()
        self.clear_inputs()
        messagebox.showinfo("Успех", "Фильм успешно добавлен!")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранный фильм?"):
            # Получение индекса выбранного элемента
            item = self.tree.item(selected_item[0])
            values = item['values']
            
            # Поиск и удаление фильма
            for i, movie in enumerate(self.movies):
                if (movie['title'] == values[0] and 
                    movie['genre'] == values[1] and 
                    movie['year'] == int(values[2]) and 
                    movie['rating'] == float(values[3])):
                    del self.movies[i]
                    break
            
            self.save_movies()
            self.update_table()
    
    def apply_filter(self):
        """Применение фильтрации"""
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        
        filtered_movies = self.movies.copy()
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m['genre'].lower()]
        
        if year_filter:
            try:
                year = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m['year'] == year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год в фильтре должен быть числом!")
                return
        
        self.update_table(filtered_movies)
        self.status_label.config(text=f"Найдено фильмов: {len(filtered_movies)}")
    
    def clear_filter(self):
        """Сброс фильтрации"""
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table()
    
    def update_table(self, movies=None):
        """Обновление таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Выбор фильмов для отображения
        display_movies = movies if movies is not None else self.movies
        
        # Заполнение таблицы
        for movie in display_movies:
            self.tree.insert('', tk.END, values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                movie['rating']
            ))
        
        # Обновление статуса
        if movies is None:
            self.status_label.config(text=f"Всего фильмов: {len(self.movies)}")
    
    def clear_inputs(self):
        """Очистка полей ввода"""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
    
    def save_movies(self):
        """Сохранение данных в JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {str(e)}")
    
    def load_movies(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {str(e)}")
                self.movies = []
        else:
            self.movies = []

def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()

if __name__ == "__main__":
    main()