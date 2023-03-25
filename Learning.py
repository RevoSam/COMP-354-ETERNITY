import tkinter as tk

#Colors
DISPLAY_LABEL_COLOR = "#E7EBEA"
BUTTON_PAD_COLOR = "#FFFFFF"
BUTTON_OPERATOR_COLOR = "#E7EBEA"
BUTTON_EQUAL_COLOR = "#F19120"
LABEL_COLOR = "#000000"
LABEL_SMALL_FONT_STYLE = ("ARIAL", 14)
LABEL_LARGE_FONT_STYLE = ("ARIAL", 35, "bold")
PAD_FONT_STYLE = ("Inter", 30)


class Eternity:
    def __init__(self):
        self.window = tk.Tk()
        #set the size of the window
        self.window.geometry("700x500")
        #disable resizing
        self.window.resizable(0,0)
        self.window.title("Eternity")

        #Creating the frames
        self.display_frame = self.initialize_display_frames()
        self_buttons_frame = self.initialize_buttons_frame()

        #Creating the Labels to show total and current calculation
        self.total = "0"
        self.currentCalculation = "0"
        self.total_label, self.current_label = self.initialize_display_labels()

        #Initialize the buttons
        self.pad_values = {
            1: (3, 0),
            2: (3, 1),
            3: (3, 2),

            4: (2, 0),
            5: (2, 1),
            6: (2, 2),

            7: (1, 0),
            8: (1, 1),
            9: (1, 2),

            0: (4, 2),
            '.': (4,1),
            '√': (4,0)
        }

        self.operations = {'+', '-', '×', '/'}
        self.special_operations = {'←', 'AC', 'e', 'Π'}


        self.self_buttons_frame = self.initialize_buttons_frame()
        self.initialize_pad_buttons()
        self.initialize_operators_button()
        self.initialize_special_operators_button()
        self.initialize_equal_button()


    def initialize_display_labels(self):
        total_label = tk.Label(self.display_frame, text = self.total, anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_frame, text = self.currentCalculation, anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_LARGE_FONT_STYLE)
        current_label.pack(expand=True, fill="both")

        return total_label, current_label


    def initialize_display_frames(self):
        frame = tk.Frame(self.window, height = 100, bg = DISPLAY_LABEL_COLOR)
        frame.pack(expand=True, fill="both")
        return frame
    
    def initialize_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def initialize_pad_buttons(self):
        for value, grid_loc in self.pad_values.items():
            baground_color = BUTTON_OPERATOR_COLOR
            if isinstance(value, int):
                baground_color = BUTTON_PAD_COLOR
            button = tk.Button(self.self_buttons_frame, text = str(value), bg = baground_color, fg = LABEL_COLOR, font=PAD_FONT_STYLE, borderwidth=0, padx=10)
            button.grid(row=grid_loc[0], column=grid_loc[1], sticky=tk.NSEW)
    
    def initialize_operators_button(self):
        i = 1
        for symbol in self.operations:
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10)
            button.grid(row = i, column = 3, sticky=tk.NSEW)
            i+=1

    def initialize_special_operators_button(self):
        i = 0
        for symbol in self.special_operations:
            baground_color = BUTTON_OPERATOR_COLOR
            font_color = LABEL_COLOR
            if symbol == 'AC':
                baground_color = BUTTON_EQUAL_COLOR
                font_color = BUTTON_PAD_COLOR
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, padx=10)
            button.grid(row = 0, column = i, sticky=tk.NSEW)
            i+=1

    def initialize_equal_button(self):
        button = tk.Button(self.self_buttons_frame, text = '=', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10)
        button.grid(row = 3, column = 4, rowspan = 2, sticky=tk.NSEW)

    def run(self):
        self.window.mainloop()




if __name__ == "__main__":
    myEternity = Eternity()
    myEternity.run()


