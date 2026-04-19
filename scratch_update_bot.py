import json

with open('scaled_map.json', 'r') as f:
    scaled_map = json.load(f)

# Convert dict to string that looks like python code
map_str = "PARKING_MAP = {\n"
for name, box in scaled_map.items():
    pts_str = ", ".join([f"({x}, {y})" for x, y in box])
    map_str += f'    "{name}": [{pts_str}],\n'
map_str += "}"

with open('carDetection/bot.py', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith("PARKING_MAP = {"):
        start_idx = i
    if start_idx != -1 and line.startswith("}"):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [map_str + "\n"] + lines[end_idx+1:]
    with open('carDetection/bot.py', 'w') as f:
        f.writelines(new_lines)
    print("Replaced PARKING_MAP in bot.py")
