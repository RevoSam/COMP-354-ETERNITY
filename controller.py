import math
import tkinter as tk
from tkinter import filedialog as fd
import os
import csv
import Functions.special_fn as specialFunctions
import Functions.subordinate_fn as subordinateFunctions
from tkinter import messagebox
from model import EternityModel
from view import EternityView
from Parsing import convert_str_to_num, is_a_number, parse_string_multi_values

# Controller class for Eternity
class EternityController:
    
    # Constructor
    def __init__(self):
        # create new Model and View members
        self.model = EternityModel()
        self.view = EternityView(self)

    """---------------------------------------------------------------------------------------------
    HANDLE BUTTONS CLICK FOR SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    # method to create new windows for special functions user selected
    def functions_buttons_click(self, function):
        print(function)
        if function == "ab^n":
            self.view.create_special_function_window("ab^n", 0, 1, 1, 1)
        if function == "Gamma":
            self.view.create_special_function_window("Gamma", 1, 0, 0, 0)
        if function == "x_power_n":
            self.view.create_special_function_window("x_power_n", 1, 1, 0, 0)
        if function == "arccos":
            self.view.create_special_function_window("arccos", 1, 0, 0, 0)
        if function == "sinh":
            self.view.create_special_function_window("sinh", 1, 0, 0, 0)
        if function == "logb":
            self.view.create_special_function_window("logb", 1, 0, 1, 0)
        if function == "MAD":
            self.view.create_mad_sd_window("MAD")
        if function == "sd":
            self.view.create_mad_sd_window("SD")
        if function == "Save":
            self.save_results(self.model.get_current_calculation())
        if function == "Recall":
            # open recall window, else show error if there's no saved result to recall
            if len(self.model.get_saved_results()) > 0:
                self.view.create_recall_window("main")
            else:
                messagebox.showerror("Recall Error", "Error: There is no saved result to recall!")

    """---------------------------------------------------------------------------------------------
    CONTROL MAD/SD CHILD WINDOW OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    def validate_input_mad_sd(self, *args):
        legalCharachters = set("123456789.,")
        if len(self.view.child_window_functions.x_input.get()) > 0:
            if not legalCharachters.issuperset(str(self.view.child_window_functions.x_input.get()[-1]).strip()):
                self.view.child_window_functions.x_input.delete(len(str(self.view.child_window_functions.x_input.get())) - 1, tk.END)
        
    # method to process data points inputted manually and call function to calculate MAD / SD
    def validate_and_calculate_using_inputedValues(self, isSample, callingFunction):
        input = str(self.view.child_window_functions.x_input.get())
        data_points = input.split(',')
        self.execute_mad_or_sd("manual", data_points, isSample, callingFunction)
        
    # method to process imported CSV and call function to calculate MAD / SD
    def open_file_dialogue(self, isSample, callingFunction):
        self.view.child_window_functions.x_input.delete(0, tk.END)
        #Launch the dialogue in the same directory where the application is running
        filepath = fd.askopenfilename(initialdir=os.getcwd(), title="File to import", filetypes=(("CSV", "*.csv"),))
        with open(filepath, 'r') as file:
            #print(file.read())
            csvreader = csv.reader(file, delimiter=',')
            data_points = []
            for row in csvreader:
                for i in range(len(row)):
                    data_points.append(row[i])
            # for i in range(len(data_points)):
            #     sum += int(data_points[i])
            #print("AVG: " + str((sum / len(data_points))))
        self.execute_mad_or_sd("csv", data_points, isSample, callingFunction)
        
    # method to calculate MAD and SD based on input
    def execute_mad_or_sd(self, input_mode, data_points, isSample, callingFunction):
        data_points_floats = parse_string_multi_values(data_points)
        if data_points_floats is None:
            if input_mode == "csv":
                messagebox.showerror("Invalid Input Error", "Make sure data points in CSV are real numbers only!")
            elif input_mode == "manual":
                messagebox.showerror("Invalid Input Error", "Please enter 2 or more real numbers separated by commas!")
        else:
            fnName = ""
            result = 0.0
            if callingFunction == "MAD":
                result = specialFunctions.mad(data_points_floats)
                fnName = "MAD = " + str(result)
            elif callingFunction == "SD":
                bool = True if (isSample.get() == 1) else False
                result = specialFunctions.standard_deviation(data_points_floats, bool)
                fnName = "SD = " + str(result)
            self.view.total_label.config(text = fnName)
            self.model.set_current_calculation(str(result))
            self.update_current()
            self.view.child_window_functions.destroy()

    """---------------------------------------------------------------------------------------------
    CONTROL ARCCOS/SINH(X)/GAMMA/X^Y/AB^X/LOGB(X) CHILD WINDOW OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    # input e/pi/square root/recall values in current texbox of special function window
    def child_add_special_operations(self, symbol):
        value = 0
        entry = self.view.child_window_functions.focus_get()
        if isinstance(entry, tk.Entry):
            if symbol == 'e':
                value = str(subordinateFunctions.EULER)
            if symbol == 'PI':
                value = str(subordinateFunctions.PI)
            if symbol == 'sqrt':
                if len(entry.get()) > 0:
                    value = subordinateFunctions.sqrt(convert_str_to_num(entry.get()))
            if symbol == "recall":
                # open the recall window, else show error if there's no saved result to recall 
                if len(self.model.get_saved_results()) > 0:
                    self.view.create_recall_window("child", entry)
                else:
                    messagebox.showerror("Recall Error", "Error: There is no saved result to recall!")
            # replace content in current textbox with special value
            entry.delete(0, tk.END)
            entry.insert(0, value)

    # method to validate each input variable of a function and call execute function if validated True
    def validate_and_execute_special_fn(self, function):
        if (function == "Gamma"):
            x = self.view.child_window_functions.x_input.get()
            if (is_a_number(x) and convert_str_to_num(x) > 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a positive real number!")
        if (function == "sinh"):
            x = self.view.child_window_functions.x_input.get()
            if (is_a_number(x)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real number!")
        if (function == "arccos"):
            x = self.view.child_window_functions.x_input.get()
            if (is_a_number(x) and convert_str_to_num(x) >= -1 and convert_str_to_num(x) <= 1):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real number between -1 and 1!")
        if (function == "ab^n"):
            a = self.view.child_window_functions.a_input.get()
            b = self.view.child_window_functions.b_input.get()
            n = self.view.child_window_functions.n_input.get()
            if (is_a_number(a, b, n) and convert_str_to_num(b) > 0 and convert_str_to_num(b) != 1 and convert_str_to_num(a) != 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter real numbers for a, b, n where a cannot be 0, b cannot be 1 and b is a positive real number!")
        if (function == "x_power_n"):
            x = self.view.child_window_functions.x_input.get()
            n = self.view.child_window_functions.n_input.get()
            if (is_a_number(x, n)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter real numbers for x, n!")
        if (function == "logb"):
            x = self.view.child_window_functions.x_input.get()
            a = self.view.child_window_functions.a_input.get()
            if (is_a_number(x, a) and convert_str_to_num(a) != 1 and convert_str_to_num(x) > 0 and convert_str_to_num(a) > 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter positive real numbers for a, x and a cannot be 1!")

    """---------------------------------------------------------------------------------------------
    EXECUTE SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    # method to perform calculations for special functions
    def execute_function(self, function):
        self.view.child_window_functions.x = self.view.child_window_functions.x_input.get()
        self.view.child_window_functions.n = self.view.child_window_functions.n_input.get()
        self.view.child_window_functions.a = self.view.child_window_functions.a_input.get()
        self.view.child_window_functions.b = self.view.child_window_functions.b_input.get()

        #Here is where we will call our functions
        # a != 0, b > 0, b!= 1
        if function == "ab^n":
            self.view.total_label.config(text = self.view.child_window_functions.a + "*" + self.view.child_window_functions.b + "**" + self.view.child_window_functions.n)
            self.model.set_current_calculation(str(specialFunctions.natural_exp(convert_str_to_num(self.view.child_window_functions.a), convert_str_to_num(self.view.child_window_functions.b), convert_str_to_num(self.view.child_window_functions.n))))
            self.update_current()
        # x > 0
        if function == "Gamma":
            self.view.total_label.config(text = "Γ(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.gamma(convert_str_to_num(self.view.child_window_functions.x))))
            self.update_current()
        # x, n are real numbers
        if function == "x_power_n":
            self.view.total_label.config(text = self.view.child_window_functions.x + "**" + self.view.child_window_functions.n)
            self.model.set_current_calculation(str(specialFunctions.power(convert_str_to_num(self.view.child_window_functions.x), convert_str_to_num(self.view.child_window_functions.n))))
            self.update_current()
        # x >= -1 and x <= 1
        if function == "arccos":
            self.view.total_label.config(text = "arccos(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.arccos(convert_str_to_num(self.view.child_window_functions.x))))
            self.update_current()
        # x is a real number
        if function == "sinh":
            self.view.total_label.config(text = "sinh(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.sinh(convert_str_to_num(self.view.child_window_functions.x))))
            self.update_current()
        # x, b > 0, b != 1
        if function == "logb":
            self.view.total_label.config(text = "log" + self.view.child_window_functions.a + "(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(math.log(convert_str_to_num(self.view.child_window_functions.x), convert_str_to_num(self.view.child_window_functions.a))))
            self.update_current()
        self.view.child_window_functions.destroy()

    """---------------------------------------------------------------------------------------------
    SAVE/RECALL OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    # save the results from current calculation
    def save_results(self, currentCalculation):
        # only allow 7 saves, remove earliest save if exceeding 7
        if (len(self.model.get_saved_results()) >= 7):
            self.model.set_saved_results(self.model.get_saved_results()[1:])
        value_to_save = convert_str_to_num(currentCalculation)
        if (currentCalculation != "" and value_to_save is not None):
            # if the value is a valid number, add to array of saved results
            self.model.add_saved_result(value_to_save)
        else:
            # otherwise output error window
            messagebox.showerror("Save Error", "Error: Need a valid number to save!")

    # method to remove a certain saved value
    def remove_saved_value(self, listbox, main_or_child):
        selected_entry = listbox.curselection()
        # output error message and close recall window if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Delete Error", "Error: There is no saved result to delete!")
            self.close_recall_window(main_or_child)
        else:
            # delete the entry from listbox and array of saved values
            selected_value = listbox.get(selected_entry[0])
            listbox.delete(selected_entry)
            self.model.remove_saved_result(selected_value)
            # select the 1st entry again (if available)
            listbox.select_set(0)

    # method to recall a saved value to the main window or a child window
    def recall_saved_value(self, listbox, main_or_child, entry):
        selected_entry = listbox.curselection()
        # output error message if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Recall Error", "Error: There is no saved result to recall!")
            self.close_recall_window(main_or_child)
        selected_value = listbox.get(selected_entry[0])
        # if recalling to main, add the value to main window's current calculation label
        if (main_or_child == "main"):
            self.model.set_current_calculation(convert_str_to_num(selected_value))
            self.update_current()
        # if recalling to child, replace whatever's in textbox with the recalled value
        else:
            entry.delete(0, tk.END)
            entry.insert(0, convert_str_to_num(selected_value))
        # close recall window
        self.close_recall_window(main_or_child)

    # close recall window and return focus to the last window
    def close_recall_window(self, main_or_child):
        self.view.recall_window.destroy()
        if (main_or_child == "child"):
            self.view.child_window_functions.grab_set()

    """---------------------------------------------------------------------------------------------
    OTHER CALCULATOR OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    def add_special_operations(self, addedvalue):
        # self.special_operations = {'Del':'\u2190', 'e':'\u2107', 'PI': '\u03c0'}
        if addedvalue == 'Del':
            self.model.set_current_calculation(self.model.get_current_calculation()[0:len(self.model.get_current_calculation()) - 1])
        if addedvalue == 'e':
            self.model.set_current_calculation(str(subordinateFunctions.EULER))
        if addedvalue == 'PI':
            self.model.set_current_calculation(str(subordinateFunctions.PI))
        self.update_current()

    #Add the number to the current Calculation
    def add_to_current(self, addedvalue):
        value_to_add = addedvalue
        if addedvalue == '.':
          if self.model.get_current_calculation().find('.') > 0:
              value_to_add = ""
        self.model.set_current_calculation(self.model.get_current_calculation() + str(value_to_add))
        self.update_current()

    #Add the operation to the current Calculation
    def append_operation(self, operator):
        self.model.set_current_calculation(self.model.get_current_calculation() + operator)
        self.model.set_total(self.model.get_total() + self.model.get_current_calculation())
        self.model.set_current_calculation("")
        self.update_total()
        self.update_current()

    #Update the total label
    def update_total(self):
        totalCalculation = self.model.get_total()
        for operator, sign in self.view.operations.items():
            totalCalculation = totalCalculation.replace(operator, f' {sign} ')
        self.view.total_label.config(text = totalCalculation)

    #Update the current calculation label
    def update_current(self):
        self.view.current_label.config(text = self.model.get_current_calculation())

    #Clear both the Total and the Current Calculation labels
    def clear_calculation(self):
        self.model.set_total("")
        self.model.set_current_calculation("")
        self.update_total()
        self.update_current()
        
    #Evaluate the current calculation
    def evaluate_current_Calculation(self):
        self.model.set_total(self.model.get_total() + self.model.get_current_calculation())
        self.update_total()

        try:
            self.model.set_current_calculation(str(eval(self.model.get_total())))
            self.model.set_total("")
        except Exception as error:
            self.model.set_current_calculation("Error: ")
            #tk.Message(error)
        finally:
            self.update_current()

    """---------------------------------------------------------------------------------------------
    GETTER
    ---------------------------------------------------------------------------------------------"""
    
    # getter for controller's model
    def get_model(self):
        return self.model

    """---------------------------------------------------------------------------------------------
    MAIN METHOD
    ---------------------------------------------------------------------------------------------"""
    
    # call main method of view
    def main(self):
        self.view.main()



if __name__ == "__main__":
    myEternity = EternityController()
    myEternity.main()