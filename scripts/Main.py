import tkinter as tk
from tkinter import simpledialog, messagebox
from Manager import DatabaseManager
import os
from Downloarder import download
from tkinter import ttk

data_folder = r".\data"

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Database Manager")

        # Set the style for application
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Set dark theme colors
        self.dark_color = "#333533"
        self.light_color = "#e8eddf"
        self.accent_color = "#f5cb5c"
        self.btn_color = "#242423"
        self.configure(bg=self.dark_color)
        self.style.configure('.', background=self.dark_color, foreground=self.light_color, font=('Helvetica', 10))
        self.style.configure('TButton', padding=(10, 5), width=20, anchor='center', font=('Helvetica', 10))
        self.style.map('TButton', background=[('pressed', self.accent_color), ('active', self.btn_color)], 
                foreground=[('disabled', '#888888')])  # greyed out text when button is disabled

        self.db = None

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Create Database
        self.create_db_btn = ttk.Button(self, text="Create Database", command=self.create_database)
        self.create_db_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        

        # Database list
        self.db_list = tk.Listbox(self, height=20, bg=self.dark_color, fg=self.light_color, relief='flat')
        self.db_list.bind('<<ListboxSelect>>', self.on_db_select)
        self.db_list.grid(row=1, column=0, rowspan=15, padx=10, pady=2, sticky='ew')

        # scrape images
        self.scrape_images_btn = ttk.Button(self, text="Scrape Images", command=self.scrape_images)
        self.scrape_images_btn.grid(row=1, column=1, padx=10, pady=2)

        # Finish Scraping
        self.finish_scraping_btn = ttk.Button(self, text="Finish Scraping", command=self.finish_scraping)
        self.finish_scraping_btn.grid(row=2, column=1, padx=10, pady=2)

        # Set as Background/Object
        self.toggle_bg_obj_btn = ttk.Button(self, text="Set as Background/Object", command=self.toggle_background_object)
        self.toggle_bg_obj_btn.grid(row=3, column=1, padx=10, pady=2)

        # Cut Out Images
        self.cut_out_images_btn = ttk.Button(self, text="Cut Out Images", command=self.cut_out_images)
        self.cut_out_images_btn.grid(row=4, column=1, padx=10, pady=2)

        # put in context
        self.put_in_context_btn = ttk.Button(self, text="Put in Context", command=self.put_in_context)
        self.put_in_context_btn.grid(row=5, column=1, padx=10, pady=2)

        # see database
        self.see_db_btn = ttk.Button(self, text="See Database", command=self.see_database)
        self.see_db_btn.grid(row=6, column=1, padx=10, pady=2)

        # Label Images
        self.label_images_btn = ttk.Button(self, text="Label Images", command=self.label_images)
        self.label_images_btn.grid(row=7, column=1, padx=10, pady=2)

        # Clean Data
        self.clean_db_btn = ttk.Button(self, text="Clean Database", command=self.clean_data)
        self.clean_db_btn.grid(row=8, column=1, padx=10, pady=2)

        # Delete Database
        self.delete_db_btn = ttk.Button(self, text="Delete Database", command=self.delete_database)
        self.delete_db_btn.grid(row=9, column=1, padx=10, pady=2)

        # download
        self.download_btn = ttk.Button(self, text="Download", command=self.download_database)
        self.download_btn.grid(row=10, column=1, padx=10, pady=2)

        self.update_db_list()



    def update_db_list(self):
        self.db_list.delete(0, tk.END)
        dbs = os.listdir(data_folder)
        for db in dbs:
            self.db_list.insert(tk.END, db)

    def on_db_select(self, evt):
        print("Selected")
        w = evt.widget
        index = int(w.curselection()[0])
        name = w.get(index)[9:] # Get the name of the database without the "Database_" prefix
        self.db = DatabaseManager.load(name)
        self.update_buttons()

    def update_buttons(self):
        if self.db is not None:
            if not self.db.scraped :
                self.scrape_images_btn.config(state='normal')
                self.finish_scraping_btn.config(state='disabled')
                if self.db.CurNbImages != 0:
                    self.finish_scraping_btn.config(state='normal')
                    self.download_btn.config(state='normal')
                    self.see_db_btn.config(state='normal')
                self.cut_out_images_btn.config(state='disabled')
                self.label_images_btn.config(state='disabled')
                self.put_in_context_btn.config(state='disabled')
                self.download_btn.config(state='disabled')
                self.see_db_btn.config(state='disabled')
            else :
                self.download_btn.config(state='normal')
                self.see_db_btn.config(state='normal')
                self.scrape_images_btn.config(state='disabled')
                self.finish_scraping_btn.config(state='disabled')
                if self.db.isBackground:
                    self.toggle_bg_obj_btn.config(text="Set as Object")
                    self.cut_out_images_btn.config(state='disabled')
                    self.put_in_context_btn.config(state='disabled')
                    if self.db.labeled:
                        self.label_images_btn.config(state='disabled')
                    else:
                        self.label_images_btn.config(state='normal')
                else:
                    self.toggle_bg_obj_btn.config(text="Set as Background")
                    self.label_images_btn.config(state='disabled')
                    if self.db.cut:
                        self.cut_out_images_btn.config(state='disabled')
                        self.put_in_context_btn.config(state='normal')
                        if self.db.inContext:
                            self.put_in_context_btn.config(state='disabled')
                    else:
                        self.cut_out_images_btn.config(state='normal')

    def create_database(self):
        name = simpledialog.askstring("Create Database", "Enter the name of the database:")
        isBackground = messagebox.askyesno("Create Database", "Set as background database?")
        self.db = DatabaseManager.create(name, isBackground)
        self.update_db_list()
        self.update_buttons()

    def delete_database(self):
        if self.db is not None:
            self.db.delete()
            messagebox.showinfo("Delete Database", "Database deleted successfully!")
            self.db = None
            self.update_db_list()
            self.update_buttons()
        else:
            messagebox.showerror("Error", "No database selected!")

    def toggle_background_object(self):
        if self.db is not None:
            if self.db.isBackground:
                self.db.setAsObject()
                self.update_buttons()
            else:
                self.db.setAsBackground()
                self.update_buttons()
            # messagebox.showinfo("Toggle Background/Object", "Database type changed successfully!")
        else:
            messagebox.showerror("Error", "No database selected!")

    def scrape_images(self):
        if self.db is not None:
            research = simpledialog.askstring("Scrape Images", "Enter the research:")
            num_images = simpledialog.askinteger("Scrape Images", "Enter the number of images to scrape:") 
            self.db.scrape(num_images, research)
            messagebox.showinfo("Scrape Images", "Images scraped successfully!")
            self.update_db_list()  # To refresh the state of buttons
            self.update_buttons()
        else:
            messagebox.showerror("Error", "No database selected!")

    def finish_scraping(self):
        if self.db is not None:
            self.db.finishScraping()
            # self.scrape_images_btn.config(state='disabled')
            # self.finish_scraping_btn.config(state='disabled')
            # self.cut_out_images_btn.config(state='normal')
            # if self.db.isBackground:
            #     self.label_images_btn.config(state='normal')
            self.update_buttons()
            # messagebox.showinfo("Finish Scraping", "Scraping finished successfully!")
        else:
            messagebox.showerror("Error", "No database selected!")

    def cut_out_images(self):
        if self.db is not None:
            self.db.cutOut()
            messagebox.showinfo("Cut Out Images", "Images cut out successfully!")
            self.update_db_list()  # To refresh the state of buttons
            self.update_buttons()
        else:
            messagebox.showerror("Error", "No database selected!")
    
    def label_images(self):
        if self.db is not None:
            messagebox.showinfo("Label Images", "'w' to write, 'r' to restart, 'q' to quit")
            self.db.label()
            messagebox.showinfo("Label Images", "Images labeled successfully!")
            self.update_buttons()
        else:
            messagebox.showerror("Error", "No database selected!")

    def put_in_context(self):
        if self.db is None:
            messagebox.showerror("Error", "No database selected!")
            return
        bg_db_name = simpledialog.askstring("Put in Context", "Enter the name of the background database:")
        if not os.path.exists(os.path.join(data_folder, f'Database_{bg_db_name}')):
            messagebox.showerror("Error", "Background database does not exist!")
            return
        bg_db = DatabaseManager.load(bg_db_name)
        if not bg_db.isBackground:
            messagebox.showerror("Error", "Background database is not a background database!")
            return
        if not bg_db.labeled:
            messagebox.showerror("Error", "Background database is not labelled!")
            return
        if not self.db.cut:
            messagebox.showerror("Error", "Images are not cut out!")
            return
        self.db.putInContext(bg_db)
        messagebox.showinfo("Put in Context", "Images put in context successfully!")
        self.update_buttons()

    def download_database(self):
        folder = self.db.cur_folder
        if folder is not None :
            download(folder)
    
    def see_database(self):
        self.db.checkFolder()
   
    def clean_data(self):
        if self.db is not None:
            self.db.cleanAll()
            messagebox.showinfo("Clean Data", "Data cleaned successfully!")

        else:
            messagebox.showerror("Error", "No database selected!")
        self.update_buttons()

if __name__ == "__main__":
    app = Application()
    app.mainloop()