# import pandas as pd 
import os

LOAD_FILE_DIR = "./load-files"

def main():
   
    main_menu_opts = ["Edit Configuration", "Load File", "Analyze File"] 
    # while menu_choice != str(len(main_menu_opts) + 1):
        
    # load_files = get_load_files(LOAD_FILE_DIR)

    
def get_load_files(path: str):
    if os.path.isabs(path):
      os.mkdir(path)

    list(map(lambda x: x, os.listdir(path)))

def generate_menu(opts: [str]):
    
    def format_opts(options, count):
        if len(options) == 0:
            return Lis 


    # formated_opts = 


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