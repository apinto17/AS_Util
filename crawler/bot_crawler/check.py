
with open("bhid.txt") as f:
    data = f.readlines()

print(len(data))
unique_data = set()

for d in data:
    sd = d.split("*")
    desc = sd[0]
    link = sd[1]
    cat = sd[2]
    if desc in unique_data:
        print(desc, cat)
        print()
    
    unique_data.add(desc)
