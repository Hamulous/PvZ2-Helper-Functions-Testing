try:
    import sys
    from colorama import init, Fore
    init()
    from json import loads
    from importlib import import_module
    from readchar import readchar
    import os
    from time import time
except Exception as e:
    print(f"ERROR: {e}")
    input()

author_colors = {
    "stuff26": Fore.LIGHTMAGENTA_EX,
    "hamulous": Fore.LIGHTWHITE_EX,
    "jaykrow": Fore.RED,
    "unknown": Fore.LIGHTBLACK_EX
}

def open_in_exe(relative_path):
    global is_function_compiler
    is_function_compiler = True
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
        is_function_compiler = False
    return os.path.join(base_path, relative_path)

def display_option(option_details, function_num):
    name = option_details.get("name", f"Unnamed Script #{function_num}")
    details = option_details.get("details", "No description available.")
    function_input = option_details.get("input", "Unknown")
    function_output = option_details.get("output", "Unknown")
    author = option_details.get("author", "unknown").lower()
    author_color = author_colors.get(author, author_colors["unknown"])

    print(f"{Fore.LIGHTMAGENTA_EX}[{function_num}]: {Fore.LIGHTGREEN_EX}{name}")
    print(f"{Fore.GREEN}- Function:  {Fore.LIGHTBLUE_EX}{details}")
    print(f"{Fore.GREEN}- Input:     {Fore.LIGHTBLUE_EX}{function_input}")
    print(f"{Fore.GREEN}- Output:    {Fore.LIGHTBLUE_EX}{function_output}")
    print(f"{Fore.GREEN}- Author:    {author_color}{author}\n")

def new_section(name):
    display_dashed_line()
    print(f"> {Fore.YELLOW}{name}")
    display_dashed_line()
    print()

def display_dashed_line():
    print(f"{Fore.RED}---------------------")

def find_scripts_not_in_config(config):
    script_dir = open_in_exe("scripts")
    listed = set()
    if "functions" in config:
        for group in config["functions"].values():
            for func in group:
                listed.add(func["function_name"])

    excluded = {"__init__", "universal_functions", "Coolimageresizer", "ExportSprites", "fix_multi_sprite_frames", "PSDExporterImade"}
    found = []
    if os.path.exists(script_dir):
        for file in os.listdir(script_dir):
            if file.endswith(".py") and not file.startswith("__"):
                name = file[:-3]
                if name not in listed and name not in excluded:
                    found.append(name)
    return found

def main():
    # Load function config
    with open(open_in_exe("function_config.json"), "r", encoding="utf-8") as file:
        functions = loads(file.read())

    # Header
    print(f"{Fore.YELLOW}PvZ2 Helper Functions by stuff26")
    print(f"Version {Fore.GREEN}{functions['version']}")
    print(f"{Fore.YELLOW}Intended for usage with files for Sen 4.0 by Haruma\n")

    # Append unlisted scripts
    if "functions" not in functions:
        functions["functions"] = {}

    unknown_scripts = find_scripts_not_in_config(functions)
    if unknown_scripts:
        if "[Unlisted Scripts]" not in functions["functions"]:
            functions["functions"]["[Unlisted Scripts]"] = []
        for unknown in unknown_scripts:
            functions["functions"]["[Unlisted Scripts]"].append({
                "name": f"Unknown Script ({unknown})",
                "details": "No description available.",
                "input": "Unknown",
                "output": "Unknown",
                "author": "unknown",
                "function_name": unknown
            })

    # Add script folder to path
    if is_function_compiler:
        sys.path.append(os.path.join(sys._MEIPASS, "scripts"))
    else:
        sys.path.append(os.path.abspath("scripts"))

    while True:
        # Display all options
        available_functions = {}
        function_num = 1
        print()
        print(f"{Fore.YELLOW}Select a function to run:")
        for function_title in functions['functions']:
            new_section(function_title)
            for function in functions['functions'][function_title]:
                available_functions[str(function_num)] = function["function_name"]
                display_option(function, function_num)
                function_num += 1
        display_dashed_line()

        while True:
            user_input = input(f"{Fore.RED}>>> {Fore.YELLOW}")
            if user_input not in available_functions:
                print(f"{Fore.MAGENTA}Please select a valid option")
                continue
            break

        function_name = available_functions[user_input]

        try:
            function_module = import_module(function_name)
            function_to_call = getattr(function_module, "main")
        except Exception as e:
            print(f"{Fore.MAGENTA}Could not load script: {e}")
            readchar()
            continue

        print(f"{Fore.LIGHTBLUE_EX}Executing {Fore.GREEN}{function_name}{Fore.LIGHTBLUE_EX}...")
        display_dashed_line()
        print()

        try:
            pre_time = time()
            function_to_call()
            elapsed = time() - pre_time
            display_dashed_line()
            print(f"\n{Fore.LIGHTMAGENTA_EX}Process completed in {round(elapsed, 4)} seconds")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")

        print(f"{Fore.LIGHTBLUE_EX}(press any button to return to menu)")
        readchar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Process ended early by user (press any button to exit)")
        readchar()
    except Exception as e:
        print(f"\n{Fore.MAGENTA}ERROR: {e}")
        readchar()
