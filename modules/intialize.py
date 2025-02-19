import re

def load_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# Seperates individual nodes from the content (nodes are in between Begin Object and End Object)
def seperate_nodes(content):
    nodes = []
    in_object = False
    current_object = []

    for line in content.splitlines():
        if "Begin Object" in line:
            in_object = True
            current_object = [line]
        elif "End Object" in line:
            in_object = False
            current_object.append(line)
            nodes.append("\n".join(current_object))
        elif in_object:
            current_object.append(line)
    
    return nodes


# Example line: FunctionReference=(MemberParent="/Script/CoreUObject.Class'/Script/Engine.KismetSystemLibrary'",MemberName="PrintString") (for functions)
def get_node_name(node):
    # Get the line below the Begin Object line
    line = node.splitlines()[1]
    
    # Get the name from "MemeberName" part
    name = line.split("MemberName=")[1].split('"')[1]
    return name
    
# Examples: NodePosX=256 NodePosY=16
def get_node_position(node):
    # Find the line that contains: NodePosX
    x, y = None, None
    for line in node.splitlines():
        if "NodePosX" in line:
            x = int(line.split("NodePosX=")[1].split(" ")[0])
        if "NodePosY" in line:
            y = int(line.split("NodePosY=")[1])
    if x is not None and y is not None:
        return (x, y)
    else:
        return None

def get_node_pins(node):
    # Find the line that contains: CustomProperties and output the following: PinName, Direction (may not be there, in that case we'll make it Input), PinType.PinCategory and DefaultValue (may not be there)
    pins = []
    for line in node.splitlines():
        if "CustomProperties Pin" in line:
            pin_name = line.split("PinName=")[1].split('"')[1]
            
            # Direction (Input if not there)
            direction = "Input"         
            if "Direction=" in line: 
                direction = line.split("Direction=")[1].split('"')[1]
                if direction == "EGPD_Output":
                    direction = "Output"
            
            # Pin Origin
            pin_origin = ""
            match = re.search(r'PinSubCategoryObject="([^"]*)"', line)
            if match:
                pin_origin = match.group(1)
            
            # Pin Subtype
            match = re.search(r'PinType.PinSubCategory="([^"]*)"', line)
            pin_subtype = ""
            if match:
                pin_subtype = match.group(1)
            
            # Pin Type
            read_pin_type = line.split("PinType.PinCategory=")[1].split('"')[1]
            pin_type = fix_pin_type(read_pin_type, pin_subtype, pin_origin)
    
            # Pin Value
            pin_value = ""
            match = re.search(r'DefaultValue="([^"]*)"', line)
            if match:
                pin_value = match.group(1)
            
            pins.append((pin_name, direction, pin_type, pin_value, pin_origin))
    
    return pins  # Return an empty list if no pins are found

def fix_pin_type(pin_type, pin_subtype, pin_origin):
    pin_origin_1 = pin_origin.split("'")[1] if pin_origin != "" else ""
    pin_origin = pin_origin_1.split(".")[1] if pin_origin_1 != "" else ""
    
    if pin_origin == "Vector":
        return "vector"
    elif pin_origin == "LinearColor":
        return "linearcolor"

    
    if pin_subtype == "":
        return pin_type
    else:
        print(f"type: {pin_type}, subtype: {pin_subtype}")
        return pin_subtype
    
    return pin_type