CHARACTERS_PER_LINE = 39


def break_lines(text):
    chars_in_line = 1
    final_text = ''
    skip = False
    for char in text:
        if chars_in_line >= CHARACTERS_PER_LINE:
            if char == ' ':
                # we happen to be on a space, se we can just break here
                final_text += '\n'
                skip = True
            else:
                # work backwards to find the space to break on
                for i in range(len(final_text) - 1, 0, -1):
                    if final_text[i] == ' ':
                        final_text = final_text[:i] + '\n' + final_text[i + 1:]
                        break
            chars_in_line = 0
        chars_in_line += 1
        if not skip:
            final_text += char
        skip = False
    return final_text


def make_mutliple_textboxes(texts):
    final_text = ''
    for text in texts:
        final_text += text
        lines = text.count('\n')
        while lines % 4 != 0:
            final_text += '\n'
            lines += 1
    return final_text




if __name__ == '__main__':
    print(break_lines('The <y<Spirit of the Sword>> guides the goddess\' chosen hero to <r<Skyloft Village>>'))
    print(break_lines('Hey, you look like you have a Questions?'))
    print(break_lines('Skyloft Peater/Peatrice\'s Crystals has Bug Net'))
    print(make_mutliple_textboxes([break_lines('The <y<Spirit of the Sword>> guides the goddess\' chosen hero to <r<Skyloft Village>>'), break_lines('Hey, you look like you have a Questions?'), 'end']))
