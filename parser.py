def load_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def seperate_nodes(content):
    nodes = content.split('\n')
    return nodes

file_path = 'input.txt'
content = load_file(file_path)
print(content)