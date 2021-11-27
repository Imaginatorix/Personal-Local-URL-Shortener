import requests
import webbrowser
import json
import os
from tkinter import *
from tkinter import messagebox

class Look_Up():
    def __init__(self):
        self.screen = Tk()
        self.screen.title("Start Up")
        self.screen.resizable(0, 0)

        os.chdir("main")
        self.FILE_NAME = "links.json"
        if not os.path.exists(self.FILE_NAME):
            self.links = {}
            self.save_json()
        else:
            with open(self.FILE_NAME, "r") as f:
                self.links = json.load(f)

        self.w = self.screen.winfo_screenwidth() >> 1
        self.h = self.screen.winfo_screenheight() >> 1
        self.mid_place_x = self.w >> 1
        self.mid_place_y = self.h >> 1

        self.screen.geometry(f"{self.w}x{self.h}+{self.mid_place_x}+{self.mid_place_y}")

        self.structure()
        self.screen.mainloop()

    def structure(self):
        self.color_theme = (240, 94, 35)
        self.prompt = "What do you want?"
        self.allowance = self.side_percent(0.05)[1]
        self.entered = StringVar()
        # MAIN FRAME
        self.screen_frame = Frame(self.screen, bg = "black")
        # TOP
        self.top_frame = Frame(self.screen_frame, bg = "black")
        # TOP WIDGETS
        self.username_label = Label(self.top_frame, text = "Local URL Shortener", font = ("Helvetica", self.font_size(0.2, 1, self.h), "underline", "bold"), bg = "black", fg = "Lime")
        # ADD
        self.username_label.pack(pady = (self.allowance, 0))
        # TOP
        self.top_frame.pack()
        # BOTTOM
        self.bottom_frame = Frame(self.screen_frame, bg = "black")
        # ADD
        ### FRAME DESIGN
        self.outer_box = LabelFrame(self.bottom_frame, bg = "black")
        self.inner_box = LabelFrame(self.outer_box, bg = "black")
        self.outer_box.pack(pady = self.allowance, padx = self.allowance >> 1)
        self.inner_box.pack(pady = self.allowance, padx = self.allowance)
        ### END OF FRAME DESIGN
        self.enter_box = Entry(self.inner_box, font = ("Helvetica", self.font_size(0.1, 1, self.h)), textvariable = self.entered, width = self.side_percent(0.8)[0], exportselection = 0)
        self.send = Button(self.inner_box, text = "SEND", font = ("Helvetica", self.font_size(0.1, 1, self.h), "bold"), bg = "#%02x%02x%02x" % self.color_theme, command = self.get_output)

        self.widget_height1 = self.send.winfo_reqheight()
        self.widget_height2 = self.enter_box.winfo_reqheight()

        self.enter_box.pack(pady = self.widget_height2, padx = self.widget_height2)
        self.send.pack(pady = (0, self.widget_height1 >> 1), padx = self.widget_height1)
        # BIND
        self.enter_box.bind("<FocusIn>", self.click_tbsend_area)
        self.enter_box.bind("<FocusOut>", self.away_tbsend_area("<FocusOut>"))
        self.screen.bind("<Return>", self.get_output)
        # BOTTOM
        self.bottom_frame.pack()
        # Show all
        self.screen_frame.pack(expand = True, fill = BOTH)

    def font_size(self, part, lines, height):
        total_font_height = int(height * part)
        height_per_line = int(total_font_height / (lines * 2))
        return height_per_line

    def side_percent(self, percent):
        height = int(self.h * percent)
        width = int(self.w * percent)
        return [width, height]

    def get_output(self, event = None):
        if self.enter_box.cget("fg") != "grey" and len(self.entered.get()) > 0:
            COMMANDS = ["~add", "~del", "~links"]
            input_data = self.entered.get()
            self.output_update()
            if input_data in self.links:
                webbrowser.open_new_tab(self.links[input_data])
            elif "~" in input_data:
                arguments = input_data.split()
                if arguments[0] not in COMMANDS:
                    message = ["Must follow this format:", "<command> <parameter 1> <parameter 2> ...", f"Available commands: {COMMANDS}"]
                    messagebox.showinfo("[FORMAT ERROR]", "\n".join(message))
                else:
                    if arguments[0] == "~add":
                        if len(arguments) == 3:
                            start, key, link = arguments
                            full_link = self.get_final_link(link)
                            if self.test_link(full_link):
                                to_replace = "yes"
                                if key in self.links:
                                    message = [f"The key '{key}' already exist.", "Do you want to override the key?", f"Content: {self.links[key]}"]
                                    to_replace = messagebox.askquestion("[KEY ALREADY EXISTS]", "\n".join(message))

                                if to_replace == "yes":
                                    self.register_link(key, full_link)
                                    messagebox.showinfo("[REGISTER SUCCESSFUL!]", f"Successfully added `{key}: {link}`")
                            else:
                                messagebox.showinfo("[REGISTER UNSUCCESSFUL]", f"Link `{link}` is not available.")
                        else:
                            message = ["Must follow this format:", "~add <key> <link>"]
                            messagebox.showinfo("[FORMAT ERROR]", "\n".join(message))
                    elif arguments[0] == "~del":
                        if len(arguments) == 2:
                            start, key = arguments
                            if key in self.links:
                                message = [f"Are you sure you want to delete '{key}'?", f"Content: {self.links[key]}"]
                                to_delete = messagebox.askquestion("[ARE YOU SURE?]", "\n".join(message))

                                if to_delete == "yes":
                                    messagebox.showinfo("[DELETE SUCCESSFUL!]", f"Successfully deleted `{key}: {self.links[key]}`")
                                    del self.links[key]
                                    self.save_json()
                            else:
                                messagebox.showinfo("[DELETE UNSUCCESSFUL]", f"Key `{key}` does not exist.")
                        else:
                            message = ["Must follow this format:", "~add <key>"]
                            messagebox.showinfo("[FORMAT ERROR]", "\n".join(message))
                    elif arguments[0] == "~links":
                        if len(arguments) == 1:
                            messagebox.showinfo("[LINKS]", self.links)
                        else:
                            message = ["Must follow this format:", "~links"]
                            messagebox.showinfo("[FORMAT ERROR]", "\n".join(message))
            else:
                if "." in input_data and not len(input_data.split()) - 1: # remove unnecessarry checking, if it doesn't have dot from extension or has more than one word, it's not a website
                    full_link = self.get_final_link(input_data)
                    if self.test_link(full_link):
                        webbrowser.open_new_tab(full_link)
                        return

                webbrowser.open_new_tab(f"https://duckduckgo.com/?q={input_data}")

    def output_update(self):
        self.prompt = "What else do you want?"
        self.enter_box.delete(0, "end")
        self.away_tbsend_area("<FocusOut>")
        self.send.focus_set()
            
    def click_tbsend_area(self, event):
        if self.enter_box.cget("fg") == "grey":
            self.enter_box.delete(0, "end")
            self.enter_box.config(fg = "black")

    def away_tbsend_area(self, event):
        if self.entered.get() == "":
            self.enter_box.insert(0, self.prompt)
            self.enter_box.config(fg = "grey")

    def get_final_link(self, link):
        try:
            response = requests.head(link)
            return link
        except requests.exceptions.MissingSchema as e:
            return str(e).split()[-1][:-1]

    def test_link(self, link):
        try:
            response = requests.head(link)
            return True
        except requests.exceptions.ConnectionError as e:
            return False

    def save_json(self):
        with open(self.FILE_NAME, "w") as f:
            json.dump(self.links, f)

    def register_link(self, key, link):
        self.links[key] = link
        self.save_json()

if __name__ == "__main__":
    Look_Up()










        


















