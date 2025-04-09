# Poem-Song Phrase Matcher

This project visualizes **matching phrases** between a poem and a song. It highlights
where specific labeled phrases appear in both texts and creates a side-by-side diagram
with curved connectors between the matching parts. The final output is a high-resolution image.

---

## Overview

Given:
- A poem (`poem.txt`)
- A song (`song.txt`)
- A set of matching phrases with labels (`phrases.txt`)

The script:
1. Loads and parses the labeled lines from each text.
2. Identifies matching phrase labels across poem, song, and phrase list.
3. Visually draws:
   - Labeled lines from the poem on the left
   - Corresponding lines from the song on the right
   - Circles around the matching phrases
   - Curved paths connecting related phrases between poem and song

---

## Input Files

### poem.txt / song.txt

Text files where **some lines begin with a label** like `A1: The stars shine bright`. Other lines are plain text.

Example:
