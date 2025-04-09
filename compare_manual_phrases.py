import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch
from matplotlib.path import Path
import re

def load_labeled_lines(filepath):
    lines = []
    labels = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            match = re.match(r'^([A-Za-z0-9]+):\s*(.*)', raw)
            if match:
                label = match.group(1).strip()
                text = match.group(2).strip()
                labels[label] = len(lines)
                lines.append(text)
            else:
                lines.append(raw)
    return lines, labels

def load_phrases(filepath):
    phrases = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if "|" not in line:
                continue
            label, phrase = line.strip().split("|", 1)
            phrases[label.strip()] = phrase.strip()
    return phrases

# === Load input ===
poem_lines, poem_labels = load_labeled_lines("poem.txt")
song_lines, song_labels = load_labeled_lines("song.txt")
match_phrases = load_phrases("phrases.txt")

matched_labels = sorted(set(poem_labels) & set(song_labels) & set(match_phrases))
print(f"✅ Matched labels: {matched_labels}")

# === Layout ===
fig, ax = plt.subplots(figsize=(14, 10))
plt.axis('off')
font_size = 11
char_width = 0.0085
line_spacing = 1.4
poem_x = 0.05
song_x = 0.55
match_color = "darkorange"

# poem_y_coords = {}
# song_y_coords = {}
# 
# for i, line in enumerate(poem_lines):
    # y = 1 - i * line_spacing / len(poem_lines)
    # ax.text(poem_x, y, line, fontsize=font_size, ha='left')
    # poem_y_coords[i] = y
# 
# for i, line in enumerate(song_lines):
    # y = 1 - i * line_spacing / len(song_lines)
    # ax.text(song_x, y, line, fontsize=font_size, ha='left')
    # song_y_coords[i] = y

# === Only show matched lines, tightly spaced and vertically centered ===
visible_poem_lines = [poem_labels[l] for l in matched_labels]
visible_song_lines = [song_labels[l] for l in matched_labels]
visible_poem_lines.sort()
visible_song_lines.sort()

num_visible_lines = len(matched_labels)
line_spacing = 0.1  # tighter spacing
y_start = 0.5 + (num_visible_lines - 1) * line_spacing / 2

poem_y_coords = {}
song_y_coords = {}

for i, label in enumerate(matched_labels):
    y = y_start - i * line_spacing

    p_idx = poem_labels[label]
    s_idx = song_labels[label]

    ax.text(poem_x, y, poem_lines[p_idx], fontsize=font_size, ha='left')
    ax.text(song_x, y, song_lines[s_idx], fontsize=font_size, ha='left')

    poem_y_coords[p_idx] = y
    song_y_coords[s_idx] = y


def phrase_center_x(full_text, phrase, x_base):
    idx = full_text.lower().find(phrase.lower())
    if idx == -1:
        print(f"⚠️ Could not find phrase '{phrase}' in line: {full_text}")
        return x_base + 0.35, 0.07  # fallback
    prefix = full_text[:idx]
    px = x_base + len(prefix) * char_width + len(phrase) * char_width / 2
    width = len(phrase) * char_width
    return px, width

# === Draw ===
for label in matched_labels:
    p_idx = poem_labels[label]
    s_idx = song_labels[label]
    phrase = match_phrases[label]

    y1 = poem_y_coords[p_idx]
    y2 = song_y_coords[s_idx]

    cx1, w1 = phrase_center_x(poem_lines[p_idx], phrase, poem_x)
    cx2, w2 = phrase_center_x(song_lines[s_idx], phrase, song_x)

    ax.add_patch(Ellipse((cx1, y1), w1 + 0.02, 0.045, edgecolor=match_color, facecolor='none', lw=1.5))
    ax.add_patch(Ellipse((cx2, y2), w2 + 0.02, 0.045, edgecolor=match_color, facecolor='none', lw=1.5))

    # Connector
    verts = [
        (cx1, y1),
        ((cx1 + cx2) / 2, (y1 + y2) / 2 + 0.05),
        (cx2, y2)
    ]
    path = Path(verts, [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    patch = PathPatch(path, facecolor='none', edgecolor=match_color, lw=1.2)
    ax.add_patch(patch)

plt.savefig("comparison_final_output.png", dpi=300)
plt.close()
print("✅ Output saved to: comparison_final_output.png")

