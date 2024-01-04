import json

class GradingConfig:
    def __init__(self):
        self.config = {}
    
    def add_category(self, name: str):
        self.config[name] = {"weight": 0, "tags": []}

    def get_categories(self):
        return list(self.config.keys())

    def remove_category(self, name):
        del self.config[name]

    def add_weight(self, name: str, weight: int):
        self.config[name]["weight"] = weight

    def get_weight(self, name):
        return self.config[name]["weight"]

    def edit_weight(self, name: str, weight: int):
        self.config[name]["weight"] = weight
    
    def add_tag(self, name: str, tag:str):
        self.config[name]["tags"].append(tag)

    def get_tags(self, name: str):
        return self.config[name]["tags"]

    def remove_tag(self, name: str, index: int):
        self.config[name]["tags"].pop(index)
        
    def edit_tag(self, name: str, index: int, new_tag: str):
        self.remove_tag(name, index)
        self.add_tag(name, new_tag)

    def get_cat_keys(self, name: str):
        return list(self.config[name].keys())


    def display(self):
        print("Grading Configuration\n")
        if(len(self.config.keys()) == 0):
            return print("Please add some categories...\n")
        for key, value in self.config.items():
            print(f"{key}\t{value['weight']}\t{value['tags']}")
        print()



    @staticmethod
    def from_file(file_path: str):
        grading_config = GradingConfig()
        try: 
            with open(file_path, "r") as file:
                data = json.load(file)
                for key, value in data.items():
                    grading_config.config[key] = value

        except:
            print("Failed to load configurations from file")
        
        return grading_config
    
    @staticmethod
    def to_file(file_path: str, grading_config):
        with open(file_path, "w") as file:
            json.dump(grading_config.config, file)