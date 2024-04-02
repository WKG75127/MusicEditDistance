import xml.etree.ElementTree as ET
import glob
import sys
import os

def edit_dist(list1, list2):
    len1 = len(list1)
    len2 = len(list2)

    # Create a table to store results of subproblems
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Fill dp[][] in bottom-up manner
    for i in range(len1 + 1):
        for j in range(len2 + 1):
            if i == 0:
                dp[i][j] = j * insertion_cost_func(list2[j - 1])
            elif j == 0:
                dp[i][j] = i * deletion_cost_func(list1[i - 1])
            elif list1[i - 1] == list2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i][j - 1] + insertion_cost_func(list2[j - 1]),      # Insert
                               dp[i - 1][j] + deletion_cost_func(list1[i - 1]),       # Remove
                               dp[i - 1][j - 1] + substitution_cost_func(list1[i - 1], list2[j - 1]),  # Replace
                               dp[i - 1][j - 1] + fragmentation_cost_func(list1[i - 1], list2[j - 6:j+5]),  # Fragmenation
                               dp[i - 1][j - 1] + compression_cost_func(list1[i - 6:i+5], list2[j - 1]))  # Compression

    return dp[len1][len2]
# Define functions for insertion, deletion, and substitution costs
def insertion_cost_func(item):
    return item[1]

def deletion_cost_func(item):
    return item[1]

def substitution_cost_func(item1, item2):
    cost = abs(item1[0]-item2[0]) *item1[1]/item2[1] if item2[1] != 0 else abs(item1[0]-item2[0]) *item1[1]
    return cost
def fragmentation_cost_func(compressed,fragments):
    for i in range(len(fragments)-2):
        if fragments[i][0]==fragments[i+1][0]:
            compressed_duration = fragments[i][1] + fragments[i+1][1]
            if compressed_duration == compressed[1]:
                return 1
        else:
            break
    return 100000
def compression_cost_func(fragments,compressed):
    for i in range(len(fragments)-2):
        if fragments[i][0]==fragments[i+1][0]:
            compressed_duration = fragments[i][1] + fragments[i+1][1]
            if compressed_duration == compressed[1]:
                return 1
        else:
            break
    return 100000
def extract_notes_from_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    notes = []

    # Iterate through each measure
    for measure in root.iter('measure'):
        # Iterate through each note in the measure
        for note in measure.iter('note'):
            step_element = note.find('pitch/step')
            step = ord(step_element.text)-64 if step_element is not None else 0.0
            octave_element = note.find('pitch/octave')
            octave = int(octave_element.text) if octave_element is not None else 0.0
            alter_element = note.find('pitch/alter')
            alter = float(alter_element.text) if alter_element is not None else 0.0
            duration_element = note.find('duration')
            duration = int(duration_element.text) if duration_element is not None else 0.0

            pitch = step+7*octave + 0.5*alter
            notes.append((pitch,duration))

    return notes

# Example usage
songs = []
path = "C:\\Users\\wkg75\\Documents\\Python\\MusicXml"
for filename in glob.glob(os.path.join(path,'*.musicxml')):
    result = extract_notes_from_musicxml(filename)
    songs.append(result)
edit_distance=[]
for song in songs:
    song_distance = []
    for comp in songs:
        edit = edit_dist(song,comp)
        song_distance.append(edit)
    edit_distance.append(song_distance)
