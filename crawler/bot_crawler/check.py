
<<<<<<< HEAD
with open("bhid.txt") as f:
=======
with open("output_test.txt") as f:
>>>>>>> 464b8d8b41e858b5bb1a02d8c8bfde779d1a0f8e
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
    
<<<<<<< HEAD
    unique_data.add(desc)
=======
    unique_data.add(desc)
>>>>>>> 464b8d8b41e858b5bb1a02d8c8bfde779d1a0f8e
