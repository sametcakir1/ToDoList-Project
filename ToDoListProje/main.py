import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# TodoApp sınıfı oluşturdum
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="lightgray")
        self.root.title("Todo List App")

        # Görevlerin Saklanması için veri yapısı
        self.tasks = []

        # Arayüz tasarladığım bölüm
        self.create_screen()

        # Veriyi Dosyaya Kaydetme ve Yükleme
        self.load_tasks_from_file()

    def create_screen(self):
        # Ana ekran tasarımı

        selection_frame = tk.Frame(self.root)
        selection_frame.config(bg="white")
        selection_frame.grid(row=0, column=0, padx=10, pady=10)

        image_path = "imagee.png"
        if os.path.exists(image_path):
            image = tk.PhotoImage(file=image_path)


            image_label = tk.Label(self.root, image=image, bg="lightgray")
            image_label.image = image  # referansı tutturdum
            image_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Butonlar
        add_button = tk.Button(selection_frame, text="Görev Ekle", command=self.show_add_task_window, bg="lightgray",fg="black")
        add_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        delete_button = tk.Button(selection_frame, text="Görev Sil", command=self.show_delete_task_window, bg= "lightgray", fg="black")
        delete_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        mark_button = tk.Button(selection_frame, text="Görev Tamamla", command=self.show_mark_task_window,bg="lightgray", fg="black")
        mark_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        show_details_button = tk.Button(selection_frame, text="Detayları Göster", command=self.show_task_details_window, bg="lightgray", fg="black")
        show_details_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Görevlerin görüntülendiği tablo
        self.task_table = ttk.Treeview(selection_frame, columns=("Task", "Details", "Priority", "Status"),show="headings", selectmode="browse")

        self.task_table.heading("Task", text="Görev")
        self.task_table.heading("Details", text="Ayrıntılar")
        self.task_table.heading("Priority", text="Öncelik")
        self.task_table.heading("Status", text="Durum")
        self.task_table.column("Task", width=150)
        self.task_table.column("Details", width=150)
        self.task_table.column("Priority", width=80)
        self.task_table.column("Status", width=100)

        self.task_table.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Scrollbar'lar
        scrollbar_y = tk.Scrollbar(selection_frame, orient="vertical", command=self.task_table.yview)
        scrollbar_y.grid(row=0, column=2, rowspan=3, sticky="ns")
        self.task_table.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(selection_frame, orient="horizontal", command=self.task_table.xview)
        scrollbar_x.grid(row=3, column=1, sticky="ew")
        self.task_table.configure(xscrollcommand=scrollbar_x.set)

        # Ana ekranı güncelle methodum
        self.update_selection_screen()

    # Detayları göster penceremin kontrolünü burada sağladım.
    def show_task_details_window(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            task_details_window = tk.Toplevel(self.root)
            task_details_window.title("Görev Detayları")

            task_label = tk.Label(task_details_window, text=f"Görev Adı: {self.tasks[selected_task_index]['task']}")
            task_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            details_label = tk.Label(task_details_window,text=f"Ayrıntılar: {self.tasks[selected_task_index]['details']}")
            details_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            priority_label = tk.Label(task_details_window, text=f"Öncelik: {self.tasks[selected_task_index]['priority']}")
            priority_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            status_label = tk.Label(task_details_window,text=f"Durum: {'Tamamlandı' if self.tasks[selected_task_index]['completed'] else 'Tamamlanmadı'}")
            status_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        else:
            messagebox.showwarning("Uyarı", "Lütfen görüntülemek istediğiniz görevi seçin.")
    # Görev ekleme penceremin kontrolü
    def show_add_task_window(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Görev Ekle")

        entry_label = tk.Label(add_task_window, text="Görev:")
        entry_label.grid(row=0, column=0, padx=10, pady=10)

        task_entry = tk.Entry(add_task_window, width=30)
        task_entry.grid(row=0, column=1, padx=10, pady=10)

        details_label = tk.Label(add_task_window, text="Ayrıntılar:")
        details_label.grid(row=1, column=0, padx=10, pady=10)

        details_entry = tk.Entry(add_task_window, width=30)
        details_entry.grid(row=1, column=1, padx=10, pady=10)

        priority_label = tk.Label(add_task_window, text="Öncelik:")
        priority_label.grid(row=2, column=0, padx=10, pady=10)

        priority_entry = tk.Entry(add_task_window, width=30)
        priority_entry.grid(row=2, column=1, padx=10, pady=10)

        add_button = tk.Button(add_task_window, text="Ekle",command=lambda: self.add_task_from_window(task_entry.get(), details_entry.get(), priority_entry.get(), add_task_window), bg="lightgray",fg="black")
        add_button.grid(row=3, column=0, columnspan=2, pady=10)
    # görev ekleme kısmındaki küçük detayları hallettim. Bunları methodun içinde anlattm
    def add_task_from_window(self, task, details, priority, window):
        # Öncelik kısmı String olamaz
        if task:
            try:
                priority = int(priority)
            except ValueError:
                messagebox.showwarning("Uyarı", "Öncelik sadece sayı olmalıdır.")
                return

            # Aynı öncelikte başka bir görev var mı kontrol et
            if any(i.get('priority') == priority for i in self.tasks):
                messagebox.showwarning("Uyarı", f"{priority} önceliğinde başka bir görev zaten var.")
                return

            new_task = {"task": task, "details": details, "priority": priority, "completed": False}
            # Bilgileri girilen görevi dosyaya ve tableye yazdırdım
            self.tasks.append(new_task)
            self.tasks.sort(key=lambda x: x.get('priority', 0))
            self.update_selection_screen()
            self.save_tasks_to_file()
            window.destroy()
        else:
            messagebox.showwarning("Uyarı", "Görev boş olamaz!")
    # silme ekranı kontrolü
    def show_delete_task_window(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            delete_task_window = tk.Toplevel(self.root)
            delete_task_window.title("Görev Sil")

            task_label = tk.Label(delete_task_window, text=f"Silmek istediğiniz görev: {self.tasks[selected_task_index]['task']}")
            task_label.grid(row=0, column=0, padx=10, pady=10)

            delete_button = tk.Button(delete_task_window, text="Sil", command=lambda: self.delete_task_from_window(selected_task_index, delete_task_window), bg="lightgray",fg="black")
            delete_button.grid(row=1, column=0, padx=10, pady=10)
        else:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz görevi seçin.")
     # Silme işleminin kontrolü
    def delete_task_from_window(self, index, window):
        del self.tasks[index]
        self.update_selection_screen()
        self.save_tasks_to_file()
        window.destroy()
    # Görev tamamlama işlemlerinin kontolü ve tamamlama penceresi kontrolü
    def show_mark_task_window(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            mark_task_window = tk.Toplevel(self.root)
            mark_task_window.title("Görev Tamamla")

            task_label = tk.Label(mark_task_window,
                                  text=f"Tamamladığınız görev: {self.tasks[selected_task_index]['task']}")
            task_label.grid(row=0, column=0, padx=10, pady=10)

            mark_button = tk.Button(mark_task_window, text="Tamamla",
                                    command=lambda: self.mark_task_from_window(selected_task_index, mark_task_window),
                                    bg="lightgray", fg="black")
            mark_button.grid(row=1, column=0, padx=10, pady=10)
        else:
            messagebox.showwarning("Uyarı", "Lütfen tamamladığınız görevi seçin.")
    # Dosyaya bakıp tamamlama işlemlerini kontol et
    def mark_task_from_window(self, index, window):
        if not self.tasks[index]["completed"]:
            # Eğer görev daha önce tamamlanmamışsa, işlemi gerçekleştir
            self.tasks[index]["completed"] = True
            self.update_selection_screen()
            self.save_tasks_to_file()
            window.destroy()
        else:
            messagebox.showinfo("Uyarı", "Bu görev zaten tamamlanmış durumda.")
    # Görev tablosunun güncel tutulmasının sağlanması
    def update_selection_screen(self):
        # Görev tablosunu temizle
        self.task_table.delete(*self.task_table.get_children())

        # Görevleri tabloya ekle
        for task in self.tasks:
            task_details = task.get("details", "")
            task_priority = task.get("priority", "")
            status = "Tamamlandı" if task["completed"] else "Tamamlanmadı"
            self.task_table.insert("", tk.END, values=(task["task"], task_details, task_priority, status))
    # Seçilen görevle ilgili işlemler
    def get_selected_task_index(self):
        selected_task = self.task_table.selection()
        if selected_task:
            # Seçilen görevin kimliğini al
            item_id = selected_task[0]

            # Görevin kimliğinden indeksi ayıkla
            index = self.task_table.index(item_id)

            return index
        return None
    # Json dosyasının açılması ve okunması task veri yapısına atılması
    def load_tasks_from_file(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                self.update_selection_screen()
        except FileNotFoundError:
            pass
    # Json dosyasına verilerin kaydedilmesi
    def save_tasks_to_file(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=2)
# Programın başlangıcını kontrol etmek için kullandım
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()