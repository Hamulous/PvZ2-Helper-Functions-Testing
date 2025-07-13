try:
    import sys
    from colorama import init, Fore
    init()
    from json import loads
    from importlib import import_module
    from readchar import readchar
    import os
    from time import time
    import runpy
except Exception as e:
    print(f"ERROR: {e}")
    input()

# Extended color map for authors
author_colors = {
    "stuff26": Fore.LIGHTMAGENTA_EX,
    "hamulous": Fore.LIGHTWHITE_EX,
    "jaykrow": Fore.RED
}

def main():
    while True:
        try:
            with open(open_in_exe("function_config.json"), "r", encoding="utf-8") as file:
                functions = loads(file.read())

            print(f"{Fore.YELLOW}PvZ2 Helper Functions by stuff26")
            print(f"Version {Fore.GREEN}{functions['version']}")
            print(f"{Fore.YELLOW}Intended for usage with files for Sen 4.0 by Haruma\n")

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

            available_functions = {}
            function_num = 1

            for function_title in functions['functions']:
                new_section(function_title)
                for function in functions['functions'][function_title]:
                    available_functions[str(function_num)] = function.get("function_name", "unknown")
                    display_option(function, function_num)
                    function_num += 1
            display_dashed_line()

            while True:
                user_input = input(f"{Fore.RED}>>> {Fore.YELLOW}").strip().strip('"').strip("'")
                if user_input not in available_functions.keys():
                    print(f"{Fore.MAGENTA}Please select a valid option")
                    continue
                break

            for x in available_functions:
                if user_input == x:
                    function_name = available_functions[x]
                    break

            if is_function_compiler:
                sys.path.append(os.path.join(sys._MEIPASS, "scripts"))
            else:
                sys.path.append(os.path.abspath("scripts"))

            try:
                function_module = import_module(function_name)
                function_to_call = getattr(function_module, "main")
                use_main = True
            except AttributeError:
                use_main = False

            print(f"{Fore.LIGHTBLUE_EX}Executing {Fore.GREEN}{function_name}{Fore.LIGHTBLUE_EX}...")
            display_dashed_line()
            print()

            while True:
                try:
                    pre_time = time()
                    if use_main:
                        function_to_call()
                    else:
                        print(f"{Fore.YELLOW}No 'main()' function found — running top-level code.")
                        runpy.run_path(open_in_exe(os.path.join("scripts", function_name + ".py")), run_name="__main__")
                    function_time = time() - pre_time

                    display_dashed_line()
                    print(f"\n{Fore.LIGHTMAGENTA_EX}Process completed in {round(function_time, 4)} seconds")
                    print("(press any button to continue)")
                    readchar()
                    break

                except Exception as e:
                    print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
                    display_dashed_line()
                    print()
                    print(f"{Fore.LIGHTBLUE_EX}Would you like to retry this function (Y/N)")
                    should_exit = False
                    while True:
                        answer = readchar().upper()
                        if answer == "Y":
                            print(f"{Fore.YELLOW}{answer}")
                            display_dashed_line()
                            break
                        elif answer == "N":
                            should_exit = True
                            break
                    if should_exit:
                        display_dashed_line()
                        print(f"\n{Fore.LIGHTMAGENTA_EX}Returning to main menu")
                        print("(press any button to continue)")
                        readchar()
                        break
        except Exception as e:
            print(f"\n{Fore.MAGENTA}ERROR: {e}")
            print("(press any button to return to the menu)")
            readchar()

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
    name = option_details.get("name", "Unknown")
    details = option_details.get("details", "No description available.")
    function_input = option_details.get("input", "Unknown")
    function_output = option_details.get("output", "Unknown")
    author = option_details.get("author", "unknown")
    author_color = author_colors.get(author.lower(), Fore.LIGHTBLACK_EX)

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

    excluded = {"PSDExporterImade", "fix_multi_sprite_frames", "ExportSprites", "Coolimageresizer", "universal_functions"}  # Add your excluded scripts here
    found = []
    if os.path.exists(script_dir):
        for file in os.listdir(script_dir):
            if file.endswith(".py") and not file.startswith("__"):
                name = file[:-3]
                if name not in listed and name not in excluded:
                    found.append(name)
    return found

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Process ended early by user (press any key to exit)")
        readchar()
    except Exception as e:
        print(f"\n{Fore.MAGENTA}ERROR: {e}")
        readchar()
