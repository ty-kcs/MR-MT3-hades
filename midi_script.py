import miditoolkit
import glob
import os
from tqdm import tqdm

# データセットのルートディレクトリを設定
dataset_root = "/home/tyler/tyler_july/MR-MT3-GoogleColab/dataset_for_colab"

# 処理するサブディレクトリ（test, train, validation）
subdirs = ["test", "train", "validation"]

for subdir in subdirs:
    print(f"Processing {subdir} directory...")
    midis = sorted(glob.glob(os.path.join(dataset_root, subdir, "*/MIDI/")))
    
    for midi in tqdm(midis):
        print(f"Processing: {midi}")
        stems = sorted(glob.glob(os.path.join(midi, "*.mid")))
        insts = []
        
        for stem in stems:
            midi_obj = miditoolkit.MidiFile(stem)
            for inst in midi_obj.instruments:
                insts.append(inst)

        if insts:  # インストゥルメントが見つかった場合のみ処理
            new_midi_obj = miditoolkit.MidiFile()
            new_midi_obj.ticks_per_beat = midi_obj.ticks_per_beat
            new_midi_obj.time_signature_changes = midi_obj.time_signature_changes
            new_midi_obj.tempo_changes = midi_obj.tempo_changes
            new_midi_obj.key_signature_changes = midi_obj.key_signature_changes
            new_midi_obj.instruments = insts

            output_path = os.path.join(os.path.dirname(os.path.dirname(midi)), "all_src_v2.mid")
            new_midi_obj.dump(output_path)
            print(f"Created: {output_path}")
        else:
            print(f"No instruments found in {midi}")

print("Processing completed.")