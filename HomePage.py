import os
import re
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import random
import string

def generate_password():
    lowercase_alphabet = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    numbers = '123456789'
    symbols = "!@#$"

    combine = uppercase_letters + lowercase_alphabet + numbers + symbols
    length = 8

    password = "".join(random.sample(combine, length))
    return password

class RecipeManagerApp:
    def __init__(self, window, master):
        self.window = window
        self.master = master
        self.window.title('Recipe Manager Application')
        self.window.geometry('1366x768')
        self.window.state('zoomed')
        self.window.config(background='#eff5f6')

        # Window icon
        icon = PhotoImage(file='images\\pic-icon.png')
        self.window.iconphoto(True, icon)
        self.current_frame = None
        self.no_recipes_label = None

        # Initialize user data file
        self.initialize_user_file()
        self.initialize_recipe_file()

        # Show sign-in screen by default
        self.show_signin()

    def is_valid_username(self, username):
        """Validate the username based on specified criteria."""
        if len(username) < 8 or len(username) > 14:
            return False
        if username.isdigit():
            return False
        return True

    def is_valid_email(self, email):
        """Validate the email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def show_signin(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.window, width=1400, height=800, bg='white')
        self.current_frame.place(x=0, y=0)

        # Background image
        global img1
        img1 = ImageTk.PhotoImage(Image.open("images\\recipe2.jpg"))
        Label(self.current_frame, image=img1, border=0, bg='white').place(x=20, y=80)

        # Login form
        f1 = Frame(self.current_frame, width=350, height=350, bg='white')
        f1.place(x=800, y=150)

        Label(self.current_frame, text="Sign in", fg='#ff4f5a', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=910, y=120)

        # Username Entry
        global e1
        e1 = Entry(f1, width=25, fg='grey', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        e1.insert(0, 'Username')
        e1.bind('<FocusIn>', lambda e: self.on_entry_click(e1, 'Username'))
        e1.bind('<FocusOut>', lambda e: self.on_focusout(e1, 'Username'))
        e1.place(x=30, y=60)
        Frame(f1, width=295, height=2, bg='black').place(x=25, y=87)

        # Password Entry
        global e2
        e2 = Entry(f1, width=25, fg='grey', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        e2.insert(0, 'Password')
        e2.bind('<FocusIn>', self.on_password_focus_in)
        #e2.bind('<FocusOut>', lambda e: self.on_focusout(e2, 'Password'))
        e2.bind('<KeyRelease>', self.toggle_password_masking)
        e2.place(x=30, y=130)
        Frame(f1, width=295, height=2, bg='black').place(x=25, y=157)

        Button(f1, width=39, pady=7, text='Sign in', bg='#ff4f5a', fg='white', border=0, command=self.signin_cmd).place(x=35, y=204)
        Label(f1, text="Don't have an account?", fg="black", bg='white', font=('Microsoft YaHei UI Light', 9)).place(x=75, y=250)
        Button(f1, width=6, text='Sign up', border=0, bg='white', fg='#ff4f5a', command=self.show_signup).place(x=215, y=250)

    def on_entry_click(self, entry, placeholder):
        """Function to handle focus event for entry fields."""
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focusout(self, entry, placeholder):
        """Function to handle losing focus for entry fields."""
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')
    def on_password_focus_in(self, event):
       """Handle focus in for password entry."""
       if e2.get() == 'Password':
          e2.delete(0, "end")  # Clear placeholder
          e2.config(fg='black')  # Change text color
          e2.config(show='*')  # Apply masking immediately
    # Function to toggle password masking
    def toggle_password_masking(self, event):
        """Toggle password masking based on input."""
        if e2.get() == '':
            e2.config(show='')  # No masking
            e2.insert(0, 'Password')  # Restore placeholder
            e2.config(fg='grey')  # Placeholder color
        else:
            e2.config(show='*')  # Apply masking
    

    def user_exists(self, username):
        """Check if the username exists in the users.txt file."""
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()

            for user in users[1:]:  # Skip header
                user_data = user.strip().split()
                if len(user_data) >= 2 and user_data[1] == username:
                    return True
            return False
        except FileNotFoundError:
            return False

    def signin_cmd(self):
        username = e1.get()
        password = e2.get()

        try:
            if not username or not password:
                raise ValueError("Both fields are required.")

            if self.user_exists(username):
                if self.validate_credentials(username, password):
                    messagebox.showinfo("Success", "Login successful!")
                    e1.delete(0, 'end')
                    e2.delete(0, 'end')
                    self.show_dashboard(username)
                else:
                    raise ValueError("Invalid username or password.")
            else:
                raise ValueError("Invalid username or password.")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def validate_credentials(self, username, password):
        """Validate the user's credentials."""
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()

            for user in users[1:]:  # Skip header
                user_data = user.strip().split()
                if len(user_data) >= 3 and user_data[1] == username and user_data[2] == password:
                    return True
            return False
        except FileNotFoundError:
            return False

    def show_dashboard(self, username):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.window, bg='#eff5f6')
        self.current_frame.place(x=0, y=0, width=1366, height=768)
        self.current_user_id = self.get_user_id(username)

        # Header
        header = Frame(self.current_frame, bg='#009df4')
        header.place(x=0, y=0, width=1366, height=60)

        Button(header, text='Logout', bg='#32cf8e', font=("", 13, "bold"), bd=0, fg='white',
               cursor='hand2', activebackground='#32cf8e', command=self.logout).place(x=1250, y=15)

        Label(header, text=f'Welcome: {username}', bg='#009df4', font=("", 13, "bold"), fg='white').place(x=1060, y=15)

        # Sidebar
        sidebar = Frame(self.current_frame, bg='#ffffff')
        sidebar.place(x=0, y=60, width=300, height=708)

        Label(sidebar, text=f'{username}', bg='#ffffff', font=("", 15, "bold")).place(x=90, y=200)

        # Add Recipe
        dashboard_image = Image.open('images\\add-icon.png')
        photo = ImageTk.PhotoImage(dashboard_image)
        dashboard_label = Label(sidebar, image=photo, bg='#ffffff')
        dashboard_label.image = photo
        dashboard_label.place(x=35, y=289)

        Button(sidebar, text='Add Recipe', bg='#ffffff', font=("", 13, "bold"), bd=0,
               cursor='hand2', activebackground='#ffffff', command=self.open_add_recipe_popup).place(x=80, y=291)
        
        # Other User's Recipes
        manage_image = Image.open('images\\cook.png')
        photo = ImageTk.PhotoImage(manage_image)
        manage_label = Label(sidebar, image=photo, bg='#ffffff')
        manage_label.image = photo
        manage_label.place(x=35, y=340)

        Button(sidebar, text="Other User's Recipe", bg='#ffffff', font=("", 13, "bold"), bd=0,
               cursor='hand2', activebackground='#ffffff', command=self.show_other_recipes).place(x=80, y=345)
        
        # Shared Recipes
        shared = Image.open('images\\share.png')
        photo = ImageTk.PhotoImage(shared)
        shared_label = Label(sidebar, image=photo, bg='#ffffff')
        shared_label.image = photo
        shared_label.place(x=35, y=391)

        Button(sidebar, text='Shared Recipes', bg='#ffffff', font=("", 13, "bold"), bd=0,
               cursor='hand2', activebackground='#ffffff').place(x=80, y=399)
        

        # Logo
        logo_image = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(sidebar, image=photo, bg='#ffffff')
        logo_label.image = photo
        logo_label.place(x=70, y=80)

        Label(self.current_frame, text='Welcome to Recipe Manager Application', font=("", 13, "bold"), fg='#0064a8', bg='#eff5f6').place(x=340, y=80)

        self.display_user_recipes()
  
    def logout(self):
        self.current_user_id = None
        self.show_signin()

    def get_user_id(self, username):
        """Get the user ID for a given username."""
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()

            for user in users[1:]:  # Skip header
                user_data = user.strip().split()
                if len(user_data) >= 2 and user_data[1] == username:
                    return user_data[0]  # Return UserId
            return None
        except FileNotFoundError:
            return None

    def initialize_user_file(self):
        """Initialize the user data file with headers."""
        if not os.path.exists('users.txt'):
            with open('users.txt', 'w') as file:
                file.write("UserId Username Password\n")  # Adding headers

    def initialize_recipe_file(self):
        """Initialize the recipe data file with headers."""
        if not os.path.exists('Recipe.txt'):
            with open('Recipe.txt', 'w') as file:
                file.write("RecipeId UserId RecipeName Instructions Ingredients Category\n")  # Adding headers

    def show_signup(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.window, width=1400, height=800, bg='white')
        self.current_frame.place(x=0, y=0)

        # Background image
        global img2
        img2 = ImageTk.PhotoImage(Image.open("images\\recipe2.jpg"))
        Label(self.current_frame, image=img2, border=0, bg='white').place(x=20, y=80)

        # Sign up form
        f2 = Frame(self.current_frame, width=350, height=450, bg='white')
        f2.place(x=800, y=150)

        Label(self.current_frame, text="Sign up", fg='#ff4f5a', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=910, y=120)

        # Username Entry
        global e3
        e3 = Entry(f2, width=25, fg='grey', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        e3.insert(0, 'Username')
        e3.bind('<FocusIn>', lambda e: self.on_entry_click(e3, 'Username'))
        e3.bind('<FocusOut>', lambda e: self.on_focusout(e3, 'Username'))
        e3.place(x=30, y=60)
        Frame(f2, width=295, height=2, bg='black').place(x=25, y=87)
        

        # Generate Password Button
        Button(f2, text='Generate Password', bg='#ff4f5a', fg='white', border=0, 
               command=lambda: e4.delete(0, 'end') or e4.insert(0, generate_password())).place(x=210, y=100)
        # Password Entry
        global e4
        e4 = Entry(f2, width=25, fg='grey', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        e4.insert(0, 'Password')
        e4.bind('<FocusIn>', lambda e: self.on_entry_click(e4, 'Password'))
        e4.bind('<FocusOut>', lambda e: self.on_focusout(e4, 'Password'))
        e4.place(x=30, y=130)
        Frame(f2, width=295, height=2, bg='black').place(x=25, y=157)

        # Email Entry
        global e5
        e5 = Entry(f2, width=25, fg='grey', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        e5.insert(0, 'Email')
        e5.bind('<FocusIn>', lambda e: self.on_entry_click(e5, 'Email'))
        e5.bind('<FocusOut>', lambda e: self.on_focusout(e5, 'Email'))
        e5.place(x=30, y=200)
        Frame(f2, width=295, height=2, bg='black').place(x=25, y=227)

        Button(f2, width=39, pady=7, text='Sign up', bg='#ff4f5a', fg='white', border=0, command=self.signup_cmd).place(x=35, y=280)
        Label(f2, text="Already have an account?", fg="black", bg='white', font=('Microsoft YaHei UI Light', 9)).place(x=75, y=320)
        Button(f2, width=6, text='Sign in', border=0, bg='white', fg='#ff4f5a', command=self.show_signin).place(x=215, y=320)


    def signup_cmd(self):
        username = e3.get()
        password = e4.get()
        email = e5.get()

        try:
            if not username or not password or not email:
                raise ValueError("All fields are required.")
        
            # Validate the username
            if not self.is_valid_username(username):
                raise ValueError("Username must be between 8 and 14 characters long and cannot be all digits.")
            
            # Validate the email
            if not self.is_valid_email(email):
                raise ValueError("Invalid email format.")

            if self.user_exists(username):
                raise ValueError("Username already exists. Please choose a different username.")
            # Validate the password
            if not password:
                raise ValueError("Password is required.")
            if len(password) < 6:  # Example criteria: minimum length
                raise ValueError("Password must be at least 6 characters long.")
            # Add the new user to the file
            user_id = self.get_next_user_id()
            with open("users.txt", "a") as file:
                file.write(f"{user_id:<10}{username:<20}{password:<64}{email:<30}\n")

            messagebox.showinfo("Success", "Signup successful! You can now sign in.")
            self.show_signin()

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def get_next_user_id(self):
        """Generate the next UserId based on existing users."""
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()
                if len(users) > 1:  # Check if there are users present
                    last_user = users[-1].strip().split()
                    return int(last_user[0]) + 1  # Increment the last UserId
                else:
                    return 1  # Start from 1 if no users exist
        except FileNotFoundError:
            return 1  # Start from 1 if the file does not exist

    def open_add_recipe_popup(self):
       """Open the popup to add a new recipe."""
       self.popup = Toplevel(self.window)
       self.popup.title("Add Recipe")
       self.popup.geometry("500x450")
       self.popup.configure(background='#bbe4e9')

       # Labels
       Label(self.popup, text="Add your Recipe", bg="#bbe4e9", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(25, 25), sticky='nsew')
    
       Label(self.popup, text="Recipe Name:", bg="#bbe4e9", font=("bold", 10)).grid(row=1, column=0, pady=(10, 15), sticky='w')
       Label(self.popup, text="Ingredients:", bg="#bbe4e9", font=("bold", 10)).grid(row=2, column=0, pady=(10, 15), sticky='w')
       Label(self.popup, text="Instructions:", bg="#bbe4e9", font=("bold", 10)).grid(row=3, column=0, pady=(10, 15), sticky='w')
       Label(self.popup, text="Category:", bg="#bbe4e9", font=("bold", 10)).grid(row=4, column=0, pady=(10, 15), sticky='w')

       # Entry fields
       self.recipe_name_entry = Entry(self.popup, width=50)
       self.ingredients_entry = Entry(self.popup, width=50)  
       self.instructions_entry = Entry(self.popup, width=50)  
       self.category_entry = Entry(self.popup, width=50)

       # Aligning entry fields with labels
       self.recipe_name_entry.grid(row=1, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
       self.ingredients_entry.grid(row=2, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
       self.instructions_entry.grid(row=3, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
       self.category_entry.grid(row=4, column=1, padx=(10, 10), pady=(5, 10), sticky='w')


       # Add Recipe button
       Button(self.popup, text="Add Recipe",font=("bold", 12),bd=0, command=self.add_recipe_cmd, bg="#5585b5").grid(row=5, column=1, pady=20)


    def add_recipe_cmd(self):
        """Handle the add recipe command."""
        recipe_name = self.recipe_name_entry.get()
        instructions = self.instructions_entry.get() # Get text from Text widget
        ingredients = self.ingredients_entry.get()  # 
        category = self.category_entry.get()

        self.add_recipe(recipe_name, instructions, ingredients, category, self.popup)

    def add_recipe(self, recipe_name, instructions, ingredients, category, popup):
        """Add the new recipe to the Recipe.txt file with an auto-incrementing RecipeId."""
        if recipe_name and instructions and ingredients and category:
            # Get the next RecipeId
            next_recipe_id = self.get_next_recipe_id()

            with open("Recipe.txt", "a") as file:
                file.write(f"{next_recipe_id} # {self.current_user_id} # {recipe_name} # {instructions} # {ingredients} # {category}\n")
            messagebox.showinfo("Success", "Recipe added successfully!")
            popup.destroy()
            self.display_user_recipes()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def get_next_recipe_id(self):
        """Generate the next RecipeId based on existing recipes."""
        try:
            with open("Recipe.txt", "r") as file:
                recipes = file.readlines()
                if len(recipes) > 1:  # Check if there are recipes present
                    last_recipe = recipes[-1].strip().split()
                    return int(last_recipe[0]) + 1  # Increment the last RecipeId
                else:
                    return 1  # Start from 1 if no recipes exist
        except FileNotFoundError:
            return 1  # Start from 1 if the file does not exist

    def display_user_recipes(self):
        """Display the recipes of the logged-in user in a table format."""
        # Create a frame to display the recipes
        self.recipe_frame = Frame(self.current_frame, bg='#ffffff')
        self.recipe_frame.place(x=340, y=110, width=1000, height=580)

        Label(self.recipe_frame, text="Manage Your Recipes", font=("Arial", 16, "bold"), bg='white', fg='#0064a8').pack(pady=10)

        # Create a table with headings
        table = Frame(self.recipe_frame, bg='#bbe4e9')
        table.pack()

        headings = ["Recipe Name", "Instructions", "Ingredients", "Category", "Actions"]
        for idx, heading in enumerate(headings):
            Label(table, text=heading, font=("Arial", 12, "bold"), bg='#bbe4e9').grid(row=0, column=idx, padx=10, pady=5)

        try:
            with open("Recipe.txt", "r") as file:
                recipes = file.readlines()
                has_recipes = False  # Flag to check if user has recipes
                row = 1
                for recipe in recipes[1:]:  # Skip header
                    recipe_data = recipe.strip().split(' # ')
                    if len(recipe_data) >= 6 and recipe_data[1] == str(self.current_user_id):
                        has_recipes = True
                        recipe_id, user_id, recipe_name, instructions, ingredients, category = recipe_data
                        Label(table, text=recipe_name, bg='#bbe4e9', wraplength=230).grid(row=row, column=0, padx=10, pady=5)
                        Label(table, text=instructions, bg='#bbe4e9', wraplength=230).grid(row=row, column=1, padx=10, pady=5)
                        Label(table, text=ingredients, bg='#bbe4e9', wraplength=230).grid(row=row, column=2, padx=10, pady=5)
                        Label(table, text=category, bg='#bbe4e9', wraplength=230).grid(row=row, column=3, padx=10, pady=5)

                         # Add delete button
                        delete_button = Button(table, text="Delete Recipe", bg='#5585b5', font=("", 10, "bold"), bd=0, fg='black', command=lambda r_id=recipe_id: self.delete_recipe(r_id))
                        delete_button.grid(row=row, column=4, padx=10, pady=5)

                        # Add edit button
                        edit_button = Button(table, text="Edit Recipe", bg='#32cf8e', font=("", 10, "bold"), bd=0, fg='black', command=lambda r_id=recipe_id, r_name=recipe_name, r_instructions=instructions, r_ingredients=ingredients, r_category=category: self.open_edit_recipe_popup(r_id, r_name, r_instructions, r_ingredients, r_category))
                        edit_button.grid(row=row, column=5, padx=10, pady=5)

                        row += 1
                if not has_recipes:
                 if not self.no_recipes_label:
                        self.no_recipes_label = Label(self.recipe_frame, text="You do not have Recipes \n\n Click Add button to add your Recipe", font=("Arial", 10, "bold"), bg='white', fg='#be3144')
                        self.no_recipes_label.pack(pady=20)
                else:
                    if self.no_recipes_label:
                        self.no_recipes_label.pack_forget()  # Remove the no recipes message
                        self.no_recipes_label = None  # Reset the label
        except FileNotFoundError:
            pass
    
    def show_other_recipes(self):
        popup = Toplevel(self.master)
        popup.title("Other People's Recipes")
        popup.geometry("700x400")

        # Create a canvas and a scrollbar
        canvas = Canvas(popup, bg='#bbe4e9')
        scrollbar = Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='#bbe4e9')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a table with headings
        headings = ["Recipe Name", "Instructions", "Ingredients", "Category"]
        for idx, heading in enumerate(headings):
            Label(scrollable_frame, text=heading, font=("Arial", 12, "bold"), bg='#bbe4e9', fg='black').grid(row=0, column=idx, padx=10, pady=5)

        row = 1
        with open("Recipe.txt", "r") as file:
            recipes = file.readlines()
            for recipe in recipes[1:]:  # Skip header
                recipe_data = recipe.strip().split(' # ')
                if len(recipe_data) >= 6 and recipe_data[1] != str(self.current_user_id):  # Exclude current user's recipes
                    recipe_id, user_id, recipe_name, instructions, ingredients, category = recipe_data
                    Label(scrollable_frame, text=recipe_name, bg='#bbe4e9', wraplength=200).grid(row=row, column=0, padx=10, pady=5)
                    Label(scrollable_frame, text=instructions, bg='#bbe4e9', wraplength=200).grid(row=row, column=1, padx=10, pady=5)
                    Label(scrollable_frame, text=ingredients, bg='#bbe4e9', wraplength=200).grid(row=row, column=2, padx=10, pady=5)
                    Label(scrollable_frame, text=category, bg='#bbe4e9', wraplength=200).grid(row=row, column=3, padx=10, pady=5)
                    row += 1

        if row == 1:  # If no other recipes found
            Label(scrollable_frame, text="No recipes found from other users.", bg='#bbe4e9', fg='red').grid(row=1, columnspan=4, padx=10, pady=5)




    def delete_recipe(self, recipe_id):
        """Delete a recipe after confirming from the user."""
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this recipe?")
        if confirm:
            # Read the recipes and filter out the one to delete
            with open("Recipe.txt", "r") as file:
                recipes = file.readlines()  # Make sure this is correctly indented

            # Open the file again to write back the remaining recipes
            with open("Recipe.txt", "w") as file:
                for recipe in recipes:
                    if not recipe.startswith(str(recipe_id) + " # "):  # Ensure you match the separator used
                        file.write(recipe)
        
            messagebox.showinfo("Success", "Recipe deleted successfully!")
            self.display_user_recipes()  # Refresh the list after deletion

    def open_edit_recipe_popup(self, recipe_id, recipe_name, instructions, ingredients, category):
        """Open the popup to edit an existing recipe."""
        self.popup = Toplevel(self.window)
        self.popup.title("Edit Recipe")
        self.popup.geometry("500x450")  # Adjusted size to match the add recipe form
        self.popup.configure(background='#bbe4e9')

        # Labels
        Label(self.popup, text="Edit Recipe", bg="#bbe4e9", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(25, 25), sticky='nsew')

        Label(self.popup, text="Recipe Name:", bg="#bbe4e9", font=("bold", 10)).grid(row=1, column=0, pady=(10, 15), sticky='w')
        Label(self.popup, text="Ingredients:", bg="#bbe4e9", font=("bold", 10)).grid(row=2, column=0, pady=(10, 15), sticky='w')
        Label(self.popup, text="Instructions:", bg="#bbe4e9", font=("bold", 10)).grid(row=3, column=0, pady=(10, 15), sticky='w')
        Label(self.popup, text="Category:", bg="#bbe4e9", font=("bold", 10)).grid(row=4, column=0, pady=(10, 15), sticky='w')

        # Entry fields
        self.edit_recipe_name_entry = Entry(self.popup, width=50)
        self.edit_recipe_name_entry.insert(0, recipe_name)
    
        self.edit_ingredients_entry = Entry(self.popup, width=50)
        self.edit_ingredients_entry.insert(0, ingredients)

        self.edit_instructions_entry = Entry(self.popup, width=50)
        self.edit_instructions_entry.insert(0, instructions)

        self.edit_category_entry = Entry(self.popup, width=50)
        self.edit_category_entry.insert(0, category)

        # Aligning entry fields with labels
        self.edit_recipe_name_entry.grid(row=1, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
        self.edit_ingredients_entry.grid(row=2, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
        self.edit_instructions_entry.grid(row=3, column=1, padx=(10, 10), pady=(5, 10), sticky='w')
        self.edit_category_entry.grid(row=4, column=1, padx=(10, 10), pady=(5, 10), sticky='w')

        # Save Changes button
        Button(self.popup, text="Save Changes", font=("bold", 12), bd=0, command=lambda: self.save_edited_recipe(recipe_id), bg="#5585b5").grid(row=5, column=1, pady=20)


    def save_edited_recipe(self, recipe_id):
        """Save the edited recipe details to the file."""
        new_name = self.edit_recipe_name_entry.get()
        new_instructions = self.edit_instructions_entry.get()
        new_ingredients = self.edit_ingredients_entry.get()
        new_category = self.edit_category_entry.get()

        if new_name and new_instructions and new_ingredients and new_category:
            # Read the recipes and update the specific one
            with open("Recipe.txt", "r") as file:
               recipes = file.readlines()

            with open("Recipe.txt", "w") as file:
                for recipe in recipes:
                    if recipe.startswith(str(recipe_id) + " "):  # If it's the recipe to be updated
                       # Update the recipe details
                       recipe_data = recipe.strip().split(' # ')
                       file.write(f"{recipe_id} # {recipe_data[1]} # {new_name} # {new_instructions} # {new_ingredients} # {new_category}\n")
                    else:
                       file.write(recipe)  # Write the recipe unchanged if it's not the one being edited

            messagebox.showinfo("Success", "Recipe updated successfully!")
            self.popup.destroy()
            self.display_user_recipes()  # Refresh the list after updating
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    
if __name__ == "__main__":
    root = Tk()
    app = RecipeManagerApp(root, master=root)
    root.mainloop()
