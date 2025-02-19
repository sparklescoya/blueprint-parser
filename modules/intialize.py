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
            
            # Pin Type
            pin_type = line.split("PinType.PinCategory=")[1].split('"')[1]
 
            # Pin Value
            pin_value = ""
            match = re.search(r'DefaultValue="([^"]*)"', line)
            if match:
                pin_value = match.group(1)
                
            # Origin Value
            pin_origin = ""
            match = re.search(r'PinSubCategoryObject="([^"]*)"', line)
            if match:
                pin_origin = match.group(1)
            
            pins.append((pin_name, direction, pin_type, pin_value, pin_origin))
    
    return pins  # Return an empty list if no pins are found

def fix_pin_type(pin_type, pin_origin):
    if pin_type == "StructProperty":
        return pin_origin
    return pin_type