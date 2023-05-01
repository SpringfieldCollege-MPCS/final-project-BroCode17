
conv =[{1:"me"}]
def create_conversation(name: str):
    index = 2
    conv.append({index: name})
    index += 1

def show_conversation():
    for e in conv:
        for v in e.values():
            print(v)