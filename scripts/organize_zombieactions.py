import json
import os

def get_name(s):
    """
    Extracts the name from a string formatted as 'RTID(X@Y)'.
    """
    return s.replace("RTID(", "").replace(")", "").replace("$", "").split("@")[0]

def main():
    zombie_props_path = input("Enter the full path to ZOMBIEPROPERTIES.json: ").strip('"')
    zombie_actions_path = input("Enter the full path to ZOMBIEACTIONS.json: ").strip('"')

    # Load JSON files
    with open(zombie_props_path, "r", encoding="utf-8") as zombie_props:
        zombieprops_contents = json.load(zombie_props)
    with open(zombie_actions_path, "r", encoding="utf-8") as zombie_actions:
        zombieactions_contents = json.load(zombie_actions)

    zombieprops_list = zombieprops_contents["objects"]
    zombieactions_list = zombieactions_contents["objects"]

    # Build lookup for actions by alias
    action_lookup = {}
    for action in zombieactions_list:
        for alias in action.get("aliases", []):
            action_lookup[alias] = action

    ordered_action_names = []
    seen = set()

    # Extract the mf actions
    for zombie in zombieprops_list:
        actions = zombie.get("objdata", {}).get("Actions", [])
        for action_str in actions:
            name = get_name(action_str)
            if name not in seen:
                ordered_action_names.append(name)
                seen.add(name)

    # Reset!
    ordered_actions = []
    added_aliases = set()

    for name in ordered_action_names:
        if name in action_lookup:
            action = action_lookup[name]
            # Avoid duplicates if multiple aliases map to same object
            action_id = id(action)
            if action_id not in added_aliases:
                ordered_actions.append(action)
                added_aliases.add(action_id)

    # Add any leftover (unused) actions
    for action in zombieactions_list:
        if id(action) not in added_aliases:
            ordered_actions.append(action)

    # Output to same directory as ZOMBIEACTIONS.json
    output_dir = os.path.dirname(zombie_actions_path)
    output_path = os.path.join(output_dir, "zombieactions_results.json")

    zombieactions_contents["objects"] = ordered_actions
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(zombieactions_contents, f, indent=4)

    print(f"Organized {len(ordered_actions)} actions into {output_path}")

if __name__ == "__main__":
    main()
