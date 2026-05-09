import json
import os
import tkinter as tk

# Глобальные переменные
data_file = "movies.json"
movies = []
current_filter_genre = ""
current_filter_year = ""

name_author = "Журтубаев Станислав"


#Тест
def load_data():
    """Загрузка данных из JSON файла"""
    global movies
    try:
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        else:
            movies = []
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        movies = []

def save_data():
    """Сохранение данных в JSON файл"""
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def validate_year(year):
    """Проверка корректности года"""
    try:
        year_num = int(year)
        return 1900 <= year_num <= 2026
    except ValueError:
        return False

def validate_rating(rating):
    """Проверка корректности рейтинга (0-10)"""
    try:
        rating_num = float(rating)
        return 0 <= rating_num <= 10
    except ValueError:
        return False

def clear_table(table_frame):
    """Очистка таблицы"""
    for widget in table_frame.winfo_children():
        widget.destroy()

def display_movies(table_frame, movie_list):
    """Отображение фильмов в таблице"""
    clear_table(table_frame)
    
    # Заголовки
    headers = ["Название", "Жанр", "Год", "Рейтинг"]
    for col, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 10, "bold"), 
                        borderwidth=1, relief="solid", padx=10, pady=5, bg="lightgray")
        label.grid(row=0, column=col, sticky="nsew")
    
    # Данные
    for row, movie in enumerate(movie_list, start=1):
        tk.Label(table_frame, text=movie["title"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=0, sticky="nsew")
        tk.Label(table_frame, text=movie["genre"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=1, sticky="nsew")
        tk.Label(table_frame, text=movie["year"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=2, sticky="nsew")
        tk.Label(table_frame, text=movie["rating"], borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=3, sticky="nsew")
    
    # Настройка веса столбцов
    for col in range(4):
        table_frame.columnconfigure(col, weight=1)

def refresh_table(table_frame):
    """Обновление таблицы с учетом фильтрации"""
    filtered = filter_movies()
    display_movies(table_frame, filtered)

def filter_movies():
    """Фильтрация фильмов по жанру и году"""
    global current_filter_genre, current_filter_year
    
    filtered = movies.copy()
    
    # Фильтр по жанру
    if current_filter_genre:
        filtered = [m for m in filtered if current_filter_genre.lower() in m["genre"].lower()]
    
    # Фильтр по году
    if current_filter_year:
        try:
            year_int = int(current_filter_year)
            filtered = [m for m in filtered if m["year"] == year_int]
        except ValueError:
            pass
    
    return filtered

def add_movie(title_entry, genre_entry, year_entry, rating_entry, table_frame):
    """Добавление нового фильма"""
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()
    
    # Проверка полей
    if not title:
        status_label.config(text="Ошибка: Введите название!", fg="red")
        return
    if not genre:
        status_label.config(text="Ошибка: Введите жанр!", fg="red")
        return
    if not validate_year(year):
        status_label.config(text="Ошибка: Год должен быть числом от 1900 до 2026!", fg="red")
        return
    if not validate_rating(rating):
        status_label.config(text="Ошибка: Рейтинг должен быть числом от 0 до 10!", fg="red")
        return
    
    # Добавление фильма
    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    movies.append(movie)
    save_data()
    
    # Очистка полей
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    
    status_label.config(text=f"Фильм '{title}' добавлен!", fg="green")
    refresh_table(table_frame)

def filter_by_genre(genre_entry, table_frame):
    """Фильтрация по жанру"""
    global current_filter_genre
    current_filter_genre = genre_entry.get().strip()
    refresh_table(table_frame)
    
    if current_filter_genre:
        status_label.config(text=f"Фильтр по жанру: {current_filter_genre}", fg="blue")
    else:
        status_label.config(text="Фильтр сброшен", fg="blue")

def filter_by_year(year_entry, table_frame):
    """Фильтрация по году"""
    global current_filter_year
    current_filter_year = year_entry.get().strip()
    refresh_table(table_frame)
    
    if current_filter_year:
        status_label.config(text=f"Фильтр по году: {current_filter_year}", fg="blue")
    else:
        status_label.config(text="Фильтр сброшен", fg="blue")

def reset_filters(genre_entry, year_entry, table_frame):
    """Сброс фильтров"""
    global current_filter_genre, current_filter_year
    current_filter_genre = ""
    current_filter_year = ""
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    refresh_table(table_frame)
    status_label.config(text="Фильтры сброшены", fg="blue")

def delete_movie(table_frame):
    """Удаление выбранного фильма"""
    selection_window = tk.Toplevel()
    selection_window.title("Удаление фильма")
    selection_window.geometry("400x300")
    
    tk.Label(selection_window, text="Выберите фильм для удаления:", font=("Arial", 10, "bold")).pack(pady=10)
    
    listbox = tk.Listbox(selection_window, width=50)
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    # Заполнение списка
    for i, movie in enumerate(movies):
        listbox.insert(tk.END, f"{i+1}. {movie['title']} ({movie['year']}) - {movie['genre']} - Рейтинг: {movie['rating']}")
    
    def delete_selected():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            deleted_movie = movies.pop(index)
            save_data()
            refresh_table(table_frame)
            selection_window.destroy()
            status_label.config(text=f"Фильм '{deleted_movie['title']}' удален!", fg="red")
        else:
            status_label.config(text="Ошибка: Выберите фильм для удаления!", fg="red")
    
    tk.Button(selection_window, text="Удалить", command=delete_selected, bg="red", fg="white").pack(pady=10)

def main():
    global status_label
    
    root = tk.Tk()
    root.title("Movie Library - Фильмотека")
    root.geometry("700x600")
    root.configure(bg="#f0f0f0")
    
    # Загрузка данных
    load_data()
    
    # Фрейм для ввода данных
    input_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="groove")
    input_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(input_frame, text="ДОБАВЛЕНИЕ ФИЛЬМА", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=5)
    
    tk.Label(input_frame, text="Название:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    title_entry = tk.Entry(input_frame, width=25)
    title_entry.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="Жанр:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    genre_entry = tk.Entry(input_frame, width=20)
    genre_entry.grid(row=1, column=3, padx=5, pady=5)
    
    tk.Label(input_frame, text="Год:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    year_entry = tk.Entry(input_frame, width=15)
    year_entry.grid(row=2, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="Рейтинг (0-10):", bg="#f0f0f0").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    rating_entry = tk.Entry(input_frame, width=15)
    rating_entry.grid(row=2, column=3, padx=5, pady=5)
    
    # Кнопки добавления и удаления
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(fill="x", padx=10, pady=5)
    
    add_button = tk.Button(button_frame, text="ДОБАВИТЬ ФИЛЬМ", bg="green", fg="white", font=("Arial", 10, "bold"),
                          command=lambda: add_movie(title_entry, genre_entry, year_entry, rating_entry, table_frame))
    add_button.pack(side="left", padx=5)
    
    delete_button = tk.Button(button_frame, text="УДАЛИТЬ ФИЛЬМ", bg="red", fg="white", font=("Arial", 10, "bold"),
                            command=lambda: delete_movie(table_frame))
    delete_button.pack(side="left", padx=5)
    
    # Фрейм для фильтрации
    filter_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="groove")
    filter_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(filter_frame, text="ФИЛЬТРАЦИЯ", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=5)
    
    tk.Label(filter_frame, text="Фильтр по жанру:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    filter_genre_entry = tk.Entry(filter_frame, width=20)
    filter_genre_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=lambda: filter_by_genre(filter_genre_entry, table_frame)).grid(row=1, column=2, padx=5)
    
    tk.Label(filter_frame, text="Фильтр по году:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    filter_year_entry = tk.Entry(filter_frame, width=20)
    filter_year_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=lambda: filter_by_year(filter_year_entry, table_frame)).grid(row=2, column=2, padx=5)
    
    tk.Button(filter_frame, text="СБРОСИТЬ ФИЛЬТРЫ", bg="orange", 
              command=lambda: reset_filters(filter_genre_entry, filter_year_entry, table_frame)).grid(row=1, column=3, rowspan=2, padx=20)
    
    # Статус бар
    status_label = tk.Label(root, text="Готов к работе", relief="sunken", anchor="w", bg="#ffffcc")
    status_label.pack(fill="x", side="bottom", padx=10, pady=5)
    
    # Фрейм для таблицы
    table_frame = tk.Frame(root, bg="white")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Отображение фильмов
    display_movies(table_frame, movies)
    
    root.mainloop()

if __name__ == "__main__":
    import os  # для проверки существования файла
    main()
