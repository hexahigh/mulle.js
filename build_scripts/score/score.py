import json
import os
import sys
from pprint import pprint
frames = []
score_tracks = {}

score_input_file = os.path.realpath(sys.argv[1])
movie_dir = os.path.dirname(score_input_file)
movie = os.path.basename(movie_dir)

with open(score_input_file, 'r') as fp:
    score = json.load(fp)
    # pprint(score.items())
    frame_num = 1

    for frame in score:
        track_num = 1
        for track in frame['score']:
            if track_num > 4:
                if track_num not in score_tracks:
                    score_tracks[track_num - 4] = {}
                score_tracks[track_num - 4][frame_num] = track

            if track != {} and 'width' in track and track['width'] == 394 and track['height'] == 154:
                print('Frame num: %d track: %d' % (frame_num, track_num))
                pprint(track)
                if track_num == 8 and frame_num >= 23:
                    frames.append(track)
            track_num += 1
        frame_num += 1

with open('frames.json', 'w') as fp:
    json.dump(frames, fp)
with open(os.path.join(movie_dir, 'score_tracks_%s.json' % movie), 'w') as fp:
    json.dump(score_tracks, fp, indent=4)
