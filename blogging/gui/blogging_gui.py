import tkinter as tk
from tkinter import messagebox
from blogging.controller import Controller

class BloggingGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Assignment 5 Blog System")
        self.controller = Controller()
        self.current_blog_id = None

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.make_login_screen()

    # ---------------------- LOGIN SCREEN ----------------------
    def make_login_screen(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.main_frame, text="Login", command=self.try_login).pack(pady=10)

    def try_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()

        try:
            ok = self.controller.login(u, p)
            if ok:
                self.make_main_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- MAIN MENU ----------------------
    def make_main_menu(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Blog System", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.main_frame, text="List Blogs", command=self.show_blogs).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="Create Blog", command=self.make_create_blog).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="Delete Blog", command=self.make_delete_blog).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="List Posts", command=self.show_posts).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="Create Post", command=self.make_create_post).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="Delete Post", command=self.make_delete_post).pack(fill="x", padx=50, pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(fill="x", padx=50, pady=5)

    # ---------------------- BLOG LIST ----------------------
    def show_blogs(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="All Blogs", font=("Arial", 16)).pack(pady=10)

        try:
            blogs = self.controller.list_blogs()
            self.blog_listbox = tk.Listbox(self.main_frame, width=60)
            self.blog_listbox.pack()

            for b in blogs:
                self.blog_listbox.insert("end", f"{b.id} - {b.title}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Select Blog", command=self.select_blog).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack(pady=5)

    def select_blog(self):
        try:
            sel = self.blog_listbox.get(self.blog_listbox.curselection())
            blog_id = int(sel.split(" - ")[0])
            self.controller.set_current_blog(blog_id)
            self.current_blog_id = blog_id
            messagebox.showinfo("Selected", f"Current blog set to {blog_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- CREATE BLOG ----------------------
    def make_create_blog(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Create Blog", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Blog ID:").pack()
        self.new_blog_id = tk.Entry(self.main_frame)
        self.new_blog_id.pack()

        tk.Label(self.main_frame, text="Title:").pack()
        self.new_blog_title = tk.Entry(self.main_frame)
        self.new_blog_title.pack()

        tk.Label(self.main_frame, text="Username:").pack()
        self.new_blog_user = tk.Entry(self.main_frame)
        self.new_blog_user.pack()

        tk.Label(self.main_frame, text="Email:").pack()
        self.new_blog_email = tk.Entry(self.main_frame)
        self.new_blog_email.pack()

        tk.Button(self.main_frame, text="Create", command=self.do_create_blog).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack()

    def do_create_blog(self):
        try:
            bid = int(self.new_blog_id.get())
            title = self.new_blog_title.get().strip()
            user = self.new_blog_user.get().strip()
            email = self.new_blog_email.get().strip()

            self.controller.create_blog(bid, title, user, email)
            messagebox.showinfo("Success", "Blog created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- DELETE BLOG ----------------------
    def make_delete_blog(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Delete Blog", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Blog ID:").pack()
        self.del_blog_id = tk.Entry(self.main_frame)
        self.del_blog_id.pack()

        tk.Button(self.main_frame, text="Delete", command=self.do_delete_blog).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack()

    def do_delete_blog(self):
        try:
            bid = int(self.del_blog_id.get())
            self.controller.delete_blog(bid)
            messagebox.showinfo("Deleted", "Blog deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- LIST POSTS ----------------------
    def show_posts(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Posts", font=("Arial", 16)).pack(pady=10)

        try:
            posts = self.controller.list_posts()
            self.post_list = tk.Listbox(self.main_frame, width=60)
            self.post_list.pack()

            for p in posts:
                self.post_list.insert("end", f"{p.code} - {p.title}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack(pady=10)

    # ---------------------- CREATE POST ----------------------
    def make_create_post(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Create Post", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Post Code:").pack()
        self.new_post_code = tk.Entry(self.main_frame)
        self.new_post_code.pack()

        tk.Label(self.main_frame, text="Title:").pack()
        self.new_post_title = tk.Entry(self.main_frame)
        self.new_post_title.pack()

        tk.Label(self.main_frame, text="Text:").pack()
        self.new_post_text = tk.Entry(self.main_frame)
        self.new_post_text.pack()

        tk.Button(self.main_frame, text="Create", command=self.do_create_post).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack()

    def do_create_post(self):
        try:
            code = int(self.new_post_code.get())
            title = self.new_post_title.get().strip()
            text = self.new_post_text.get().strip()

            self.controller.create_post(code, title, text)
            messagebox.showinfo("Success", "Post created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- DELETE POST ----------------------
    def make_delete_post(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        tk.Label(self.main_frame, text="Delete Post", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Post Code:").pack()
        self.del_post_code = tk.Entry(self.main_frame)
        self.del_post_code.pack()

        tk.Button(self.main_frame, text="Delete", command=self.do_delete_post).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.make_main_menu).pack()

    def do_delete_post(self):
        try:
            code = int(self.del_post_code.get())
            self.controller.delete_post(code)
            messagebox.showinfo("Deleted", "Post deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------- LOGOUT ----------------------
    def logout(self):
        try:
            self.controller.logout()
            self.current_blog_id = None
            self.make_login_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))



# ---------------------- MAIN PROGRAM ----------------------
def main():
    root = tk.Tk()
    app = BloggingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
