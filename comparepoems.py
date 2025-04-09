import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
import re

def load_labeled_lines(filepath):
    lines = []
    labels = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()):
            line = line.rstrip('\n')
            match = re.match(r'^([A-Z]+):\s*(.*)', line)
            if match:
                label = match.group(1)
                content = match.group(2)
                labels[label] = i
                lines.append(content)
            else:
                lines.append(line)
    return lines, labels

# Load the poem and song
poem_lines, poem_labels = load_labeled_lines("poem.txt")
song_lines, song_labels = load_labeled_lines("song.txt")

# Get only matching labels
matching_keys = set(poem_labels.keys()) & set(song_labels.keys())

# Draw
fig, ax = plt.subplots(figsize=(14, 12))
plt.axis('off')

poem_x, song_x = 0.1, 0.6
line_height = 1.2
y_base = max(len(poem_lines), len(song_lines)) * line_height + 1

poem_pos = {}
song_pos = {}

for i, line in enumerate(poem_lines):
    y = y_base - i * line_height
    ax.text(poem_x, y, line, fontsize=10, va='top', ha='left', wrap=True)
    poem_pos[i] = (poem_x, y)

for i, line in enumerate(song_lines):
    y = y_base - i * line_height
    ax.text(song_x, y, line, fontsize=10, va='top', ha='left', wrap=True)
    song_pos[i] = (song_x, y)

for label in sorted(matching_keys):
    poem_idx = poem_labels[label]
    song_idx = song_labels[label]
    
    (x1, y1) = poem_pos[poem_idx]
    (x2, y2) = song_pos[song_idx]
    
    rect_width = 0.75
    rect_height = 1
    ax.add_patch(Rectangle((x1 - 0.01, y1 - 0.9), rect_width, rect_height, fill=False, edgecolor='blue', lw=1.5))
    ax.add_patch(Rectangle((x2 - 0.01, y2 - 0.9), rect_width, rect_height, fill=False, edgecolor='blue', lw=1.5))

    con = ConnectionPatch(xyA=(x1 + rect_width, y1 - 0.4),
                          xyB=(x2, y2 - 0.4),
                          coordsA='data', coordsB='data',
                          arrowstyle='-', color='blue', lw=1)
    ax.add_artist(con)

plt.tight_layout()
# one of the below lines should suffice...
plt.show()
plt.savefig("comparison_output.png", dpi=300)
