import json

import modules.intialize as intialize

content = intialize.load_file("input.txt")  # Load the file

# Separate the nodes
nodes = intialize.seperate_nodes(content)

# Name the nodes and create a JSON structure
nodes_json = {}

for node in nodes:
    node_name = intialize.get_node_name(node)
    node_pos = intialize.get_node_position(node)
    node_pins = intialize.get_node_pins(node) # It outputs a list of tuples (pin_name, pin_direction, pin_type, pin_value)

    node_properties = {}

    if node_pos:
        node_pos_x, node_pos_y = node_pos
        node_properties["PositionX"] = node_pos_x
        node_properties["PositionY"] = node_pos_y

    node_properties["Pins"] = {}
    for pin_name, pin_direction, pin_type, pin_value in node_pins:
        pin_data = {
            "Direction": pin_direction,
            "Type": pin_type
        }
        if pin_value != "":
            pin_data["Value"] = pin_value
        node_properties["Pins"][pin_name] = pin_data

    nodes_json[node_name] = node_properties

# Write the result to output.json
with open("output.json", "w") as outfile:
    json.dump(nodes_json, outfile, indent=4)
    print("Done! Check output.json")