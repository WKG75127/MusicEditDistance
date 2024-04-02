import xml.etree.ElementTree as ET
import glob
import sys
import os
def extract_notes_from_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    notes = []

    # Iterate through each measure
    for measure in root.iter('measure'):
        # Iterate through each note in the measure
        for note in measure.iter('note'):
            step_element = note.find('pitch/step')
            step = step_element.text if step_element is not None else 0.0
            octave_element = note.find('pitch/octave')
            octave = octave_element.text if octave_element is not None else 0.0
            alter_element = note.find('pitch/alter')
            alter = float(alter_element.text) if alter_element is not None else 0.0
            duration_element = note.find('duration')
            duration = int(duration_element.text) if duration_element is not None else 0.0

            pitch = step+octave
            if alter == 1:
                pitch = pitch+ "#"
            elif alter == -1:
                pitch = pitch + "b"
            notes.append((pitch,duration))

    return notes

# Example usage
songs = []
path = "C:\\Users\\wkg75\\Documents\\Python\\MusicXml"
for filename in glob.glob(os.path.join(path,'*.musicxml')):
    result = extract_notes_from_musicxml(filename)
    songs.append(result)
print(songs)


