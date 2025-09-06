from mido import MidiFile, MidiTrack, Message, MetaMessage
import filedialog
import math

# Set these to your actual file paths
midi1_path = filedialog.file_path  # Base MIDI (target)
output_path = filedialog.save_path
midi2_path = None
insert = 0
repeat = 0


def set_vars_n_shii(art):
    global midi2_path
    if art == 'Zigzag (88 Keys)':
        midi2_path = '_internal\\gliss_88.mid'
    elif art == 'Double Zigzag (88 Keys)':
        midi2_path = '_internal\\db_gliss_88.mid'
    elif art == 'Short Double Zigzag (88 Keys)':
        midi2_path = '_internal\\short_db_gliss_88.mid'
    elif art == 'Zigzag (128 Keys)':
        midi2_path = '_internal\\gliss_128.mid'
    elif art == 'Double Zigzag (128 Keys)':
        midi2_path = '_internal\\dbl_gliss_128.mid'
    elif art == 'Short Double Zigzag (128 Keys)':
        midi2_path = '_internal\\fast_dbl_gliss_128.mid'
    elif art == 'Helix (128 Keys)':
        midi2_path = '_internal\\helix_128.mid'
    elif art == 'Double Helix (128 Keys)':
        midi2_path = '_internal\\dbl_helix_128.mid'
    elif art == 'Short Double Helix (128 Keys)':
        midi2_path = '_internal\\fast_dbl_helix_128.mid'
    elif art == 'Squares':
        midi2_path = '_internal\\sq.mid'


def set_vars_n_shii2(ins, rpt, gui):
    global insert
    global repeat
    insert = ins
    repeat = rpt
    merge_midi_snippet(gui)


def get_ticks_per_measure(mid: MidiFile, time_signature=(4, 4)):
    beats_per_measure, _ = time_signature
    return mid.ticks_per_beat * beats_per_measure


def get_total_measures(mid: MidiFile, time_signature=(4, 4)):
    ticks_per_measure = get_ticks_per_measure(mid, time_signature)

    max_ticks = 0
    for track in mid.tracks:
        track_ticks = sum(msg.time for msg in track)
        if track_ticks > max_ticks:
            max_ticks = track_ticks

    total_measures = math.ceil(max_ticks / ticks_per_measure)
    return total_measures


def extract_snippet(mid: MidiFile, start_measure: int, end_measure: int,
                    ticks_per_beat_src: int, ticks_per_beat_dst: int,
                    time_signature=(4, 4)):
    """
    Extracts a measure-based snippet from a MIDI file and scales tick timing
    to match a different ticks_per_beat resolution.
    """
    beats_per_measure, _ = time_signature
    ticks_per_measure_src = ticks_per_beat_src * beats_per_measure

    start_tick = start_measure * ticks_per_measure_src
    end_tick = end_measure * ticks_per_measure_src

    snippet_tracks = []

    for track in mid.tracks:
        current_tick = 0
        snippet = []

        for msg in track:
            current_tick += msg.time

            if msg.type == 'set_tempo':
                continue  # Remove tempo messages to prevent overriding base MIDI

            if start_tick <= current_tick < end_tick:
                relative_tick = current_tick - start_tick

                # Scale to target ticks_per_beat
                scaled_tick = int(relative_tick * (ticks_per_beat_dst / ticks_per_beat_src))

                snippet.append((msg.copy(), scaled_tick))

        snippet_tracks.append(snippet)

    return snippet_tracks


def insert_snippet_loop_absolute(base_midi: MidiFile, snippet_tracks, insert_at_measure: int, repeat_measures: int,
                                 time_signature=(4, 4)):
    ticks_per_measure = get_ticks_per_measure(base_midi, time_signature)

    for track_index, snippet in enumerate(snippet_tracks):
        if not snippet:
            continue

        # Accumulate all inserted events as (abs_tick, message) pairs
        all_events = []

        for repeat_index in range(repeat_measures):
            measure_tick = (insert_at_measure + repeat_index) * ticks_per_measure
            for msg, offset in snippet:
                abs_tick = measure_tick + offset
                all_events.append((abs_tick, msg.copy()))

        # Sort all by absolute tick
        all_events.sort(key=lambda x: x[0])

        # Recalculate delta times
        new_track = MidiTrack()
        new_track.append(MetaMessage('track_name', name=f'Looped Track {track_index}', time=0))
        last_tick = 0
        for abs_tick, msg in all_events:
            msg.time = abs_tick - last_tick
            last_tick = abs_tick
            new_track.append(msg)

        base_midi.tracks.append(new_track)


def merge_midi_snippet(gui):
    global insert
    global repeat
    mid1 = MidiFile(midi1_path)
    mid2 = MidiFile(midi2_path)

    # Measure info (optional but good for logging/debugging)
    total_measures_base = get_total_measures(mid1)
    total_measures_src = get_total_measures(mid2)

    from_measure = 0
    to_measure = 2
    insert_at = int(insert) - 1
    repeat_count = int(repeat)

    snippet_tracks = extract_snippet(
        mid2, from_measure, to_measure,
        ticks_per_beat_src=mid2.ticks_per_beat,
        ticks_per_beat_dst=mid1.ticks_per_beat
    )

    insert_snippet_loop_absolute(mid1, snippet_tracks, insert_at, repeat_count)
    mid1.save(output_path)

    print(f"✅ Merged and properly looping MIDI saved to: {output_path}")
    gui.show_finished_frame()


if __name__ == "__main__":
    merge_midi_snippet()

