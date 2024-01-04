import pandas as pd 
import os
import re
from typing import Dict
import json

from grading_config import GradingConfig

LOAD_FILE_DIR = os.path.join(os.getcwd(),"load-files")
GRADING_CONFIGURATION_FILE = os.path.join(os.getcwd(), "grading-config.json")
ANALYZED_FILE = os.path.join(os.getcwd(), "analyzed-files", "analyzed-grades.csv")

def main():
    clear_screen()

    main_menu_opts = ["Edit Configuration", "Load File", "Analyze File"] 
    main_menu = generate_menu(main_menu_opts)

    user_choice = main_menu()

    while user_choice != -1:
        if(user_choice == 1):
            load_configuration_driver()
        elif(user_choice == 2):
            load_files_driver()
        elif(user_choice == 3):
            print("3")
        
        pause()
        user_choice = main_menu()

def get_grading_configuration(path):
    
    try:
        with open(path, "r") as file:
            return json.load(file)
    except:
        return {} 
        
        
def load_configuration_driver():
    grading_configuration = GradingConfig.from_file(GRADING_CONFIGURATION_FILE)

    configuration_menu_options = ["Add Category", "Edit Category", "Remove Category"]
    config_menu = generate_menu(configuration_menu_options)

    grading_configuration.display() 
    menu_choice = config_menu()

    while(menu_choice != -1):
        if(menu_choice ==1):
            add_config_category(grading_configuration)
        elif(menu_choice == 2):
            edit_configuration(grading_configuration)
        elif(menu_choice == 3):
            remove_config_category(grading_configuration)

        GradingConfig.to_file(GRADING_CONFIGURATION_FILE, grading_configuration)
        grading_configuration.display()
        menu_choice = config_menu()


def add_config_category(grading_configuration: GradingConfig):
    name = input("Enter the name of the category: ")
    weight = get_cat_weight()
    grading_configuration.add_category(name)
    grading_configuration.add_weight(name, weight)
    add_tags(grading_configuration, name) 

def add_tags(config: GradingConfig, name: str):
    tag = input("Enter tag names for this category (enter `stop` to stop): ").lower()
    while tag != "stop":
        config.add_tag(name, tag)
        tag = input("Enter tag names for this category (enter `stop` to stop): ").lower()


def edit_configuration(config: GradingConfig):
    edit_config_menu = generate_menu(config.get_categories().copy())
    print("Which catgory would you like to edit?") 
    edit_choice = edit_config_menu()
    cat_name = config.get_categories()[edit_choice - 1]

    cat_keys = ["weight", "tags"]
    sub_cat_menu = generate_menu(cat_keys)

    print("Which field would you like to edit?")
    sub_cat_choice = sub_cat_menu()

    while(sub_cat_choice != -1):
        if(sub_cat_choice == 1):
            config.edit_weight(cat_name, get_cat_weight())
        elif(sub_cat_choice == 2):
            edit_config_tags(config, cat_name) 
        print("Which field would you like to edit?")
        sub_cat_choice = sub_cat_menu()

def edit_config_tags(config: GradingConfig, name: str):
    tag_choices = ["add", "edit", "remove"]
    tag_menu = generate_menu(tag_choices)

    tag_menu_choice = tag_menu()

    while tag_menu_choice != -1:
        if(tag_menu_choice == 1):
            add_tags(config, name)
        elif(tag_menu_choice == 2):
            cat_tags = config.get_tags(name)
            cat_select_menu = generate_menu(cat_tags)
            cat_select_choice = cat_select_menu()
            config.edit_tag(name, cat_select_choice - 1, input("Enter new tag name: "))
        elif(tag_menu_choice == 3):
            cat_tags = config.get_tags(name)
            cat_select_menu = generate_menu(cat_tags)
            cat_select_choice = cat_select_menu()
            config.remove_tag(name, cat_select_choice - 1)

        tag_menu_choice = tag_menu()

   


        

def remove_config_category(config: GradingConfig):
    categories = config.get_categories()
    delete_config_menu = generate_menu(categories.copy())
    print("Which category would you like to remove?")
    delete_choice = delete_config_menu()
    config.remove_category(categories[delete_choice - 1])

def get_cat_weight():
    weight_input = input("Please enter a category weight between 0.00 and 1.00: ")
    try:
        weight = float(weight_input)
        if not (0 < weight <= 1):
            raise ValueError
        return weight
    except ValueError:
        print("Invalid input!")
        pause()
        return get_cat_weight()
        

def load_files_driver():
    clear_screen()
    files = get_load_files(LOAD_FILE_DIR)

    grading_config = GradingConfig.from_file(GRADING_CONFIGURATION_FILE) 

    select_file_menu = generate_menu(files.copy())

    file_choice = select_file_menu()

    chosen_file = files[file_choice - 1] 
    raw_grade_df = pd.read_csv(chosen_file)    
    overall_grade_df = calc_overall_grade(raw_grade_df, grading_config)
    
    overall_grade_df.to_csv(ANALYZED_FILE)
    
def calc_overall_grade(df: pd.DataFrame, grading_config: GradingConfig):
    
    student_average_df = df.copy()
    categories = grading_config.get_categories()
    for cat in categories:
        cat_cols = filter_columns(grading_config.get_tags(cat), df.columns.to_list())
        student_average_df[cat] = df.apply(lambda x: calc_cat_average(x, cat_cols) * grading_config.get_weight(cat), axis=1)

    student_average_df["total_grad"] = student_average_df[categories].apply(lambda x: x.sum(), axis=1)
    print(student_average_df)

    return student_average_df 

def filter_columns(key_words: [str], cols: [str]):
    # Will match any column that contains one of the keywords provided.
    # Will also match if numbers follow keyword, ex: `pa4``
    pattern = '|'.join([f'\\b{re.escape(keyword)}\\d*\\b' for keyword in key_words])

    return list(filter(lambda col: re.findall(pattern, col, re.IGNORECASE), cols))
 

def calc_cat_average(row: pd.Series, cat_cols):
    curr_cat_row = row[cat_cols]
    assignment_totals = calculate_cat_col_totals(cat_cols)
    cat_total = dict_reduce(lambda curr, accum: curr + accum, assignment_totals, 0) 

    return curr_cat_row.sum() / cat_total


def calculate_cat_col_totals(lst: [str]):
    assignments = {}
    for col in lst:
        total_string = re.sub(r'.*\[(.*?)\].*', r'\1', col)
        assignments[col] = int(re.sub("[^0-9]", "", total_string))
    
    return assignments

def get_load_files(path: str) -> [str]:
    if not os.path.isdir(path):
      os.mkdir(path)

    return list(map(lambda x: os.path.join(path, x), os.listdir(path)))

def generate_menu(opts_param: [str]):
    opts = opts_param.copy()
    
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