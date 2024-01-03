import pandas as pd 
import os
import re
from typing import Dict
import json

LOAD_FILE_DIR = os.path.join(os.getcwd(),"load-files")
GRADING_CONFIGURATION_FILE = os.path.join(os.getcwd(), "grading-config.json")

def main():
    clear_screen()

    main_menu_opts = ["Edit Configuration", "Load File", "Analyze File"] 
    main_menu = generate_menu(main_menu_opts)

    user_choice = main_menu()

    while user_choice != -1:
        if(user_choice == 1):
            print("1")
        elif(user_choice == 2):
            load_files_driver()
        elif(user_choice == 3):
            print("3")
        
        pause()
        user_choice = main_menu()

def get_grading_configuration(path):
    pass
    

def load_files_driver():
    clear_screen()
    files = get_load_files(LOAD_FILE_DIR)
    grading_cats = get_grading_configuration(GRADING_CONFIGURATION_FILE)
    select_file_menu = generate_menu(files.copy())


    file_choice = select_file_menu()

    if(file_choice == -1):
        return print("\nReturning to main menu")
    chosen_file = files[file_choice - 1] 
    raw_grade_df = pd.read_csv(chosen_file)    
    calc_students_average(raw_grade_df, {"lab": [.4], "pa": [.6]})
    
    
def calc_students_average(df: pd.DataFrame, categories: Dict):
    
    student_average_df = df[["Last Name", "First Name"]].copy()
    for key, [weight] in categories.items():
        student_average_df[key] = df.apply(lambda x: calc_cat_average(x, key) * weight, axis=1)

    student_average_df["total_grad"] = student_average_df[categories.keys()].apply(lambda x: x.sum(), axis=1)

    print(student_average_df)
     
def calc_cat_average(row: pd.Series, cat):
    cat_cols = list(filter(lambda col: re.findall(f'\\b{cat}\\b', col, re.IGNORECASE), row.index.tolist()))
    
    curr_cat_row = row[cat_cols]
    assignment_totals = get_assignment_totals(cat_cols)
    cat_total = dict_reduce(lambda curr, accum: curr + accum, assignment_totals, 0) 

    return curr_cat_row.sum() /cat_total


def get_assignment_totals(lst: [str]):
    assignments = {}
    for col in lst:
        total_string = re.sub(r'.*\[(.*?)\].*', r'\1', col)
        assignments[col] = int(re.sub("[^0-9]", "", total_string))
    
    return assignments

def get_load_files(path: str) -> [str]:
    if not os.path.isdir(path):
      os.mkdir(path)

    return list(map(lambda x: os.path.join(path, x), os.listdir(path)))

def generate_menu(opts: [str]):
    
    def format_opts(options):
        def format_opts_calc(options, result):
            if len(options) == 0:
                return result
            
            head = options.pop(0)
            result.append(f"{len(result) + 1}: {head}")

            return format_opts_calc(options, result)

        return format_opts_calc(options, []) 
    

    def get_user_input(menu_options: [str]):
        foreach(lambda x: print(x), menu_options) 
        user_choice = input(f"\nPlease select an opiton (enter -1 to exit): ")
        try:
            num_choice = int(user_choice)
            if(-1 > num_choice > len(menu_options)):
                raise ValueError
            return num_choice

        except ValueError:
            print("Please enter a valid number")
            pause()
            return get_user_input(menu_options)
            
    formatted_opts = format_opts(opts)

    return lambda : get_user_input(formatted_opts)

def pause():
    print("\nPress enter to continue...\n")
    input()
    clear_screen()

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def foreach(func, lst: [any]):
    for item in lst:
        func(item)

def flatten(item):

    def flatten_calc(item, lst: [any], result: [any]):
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
        
        if len(lst) > 0:
            return flatten_calc(lst.pop(0), lst, result)

        return result       

    if not len(item) > 0:
       return item

    return flatten_calc(item.pop(0), item, [])

def dict_reduce(func, dict, initial):
   accum = initial 
   for key in dict.keys():
        accum = func(dict[key], accum) 

   return accum

main()