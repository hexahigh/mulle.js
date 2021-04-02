import re


def parse_animation_chart(animation_chart):
    matches_outer = re.match(r'\[#Actions:\[(.+)\], #Paths:\[(.*)\]\]', animation_chart)
    if not matches_outer:
        print('Unable to parse: %s' % animation_chart)
        return
    animations = {}

    for action_match in re.findall(r'#([a-zA-Z0-9]+):\[(.*?)\](?:, |$)', matches_outer.group(1)):
        members = re.finditer(r'(\[#(.+?),\[?([0-9,]+)\]?\])|[0-9]|#([A-Za-z0-9]+)', action_match[1])
        frames = []
        for frame in members:
            match = frame.group(0)
            if match[0] == '[':
                arguments = []
                for argument in frame.group(3).split(','):
                    arguments.append(int(argument))
                frames.append({'function': frame.group(2), 'arguments': arguments})
            elif match[0] == '#':
                frames.append(match[1:])
            else:
                frames.append(int(match))  # Reference

        animations[action_match[0]] = frames
    return animations
