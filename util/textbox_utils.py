CHARACTERS_PER_LINE = 39


def break_lines(text, characters_per_line=CHARACTERS_PER_LINE):
    words = text.split()
    final_text = ""
    chars_in_line = 0
    for word in words:
        # add 1 to account for the space at the beginning of the word
        chars_in_line += len(word) + 1
        if chars_in_line >= characters_per_line:
            # strip trailing space at the end of each line
            final_text = final_text[:-1]
            final_text += f"\n{word} "
            # account for the space again
            chars_in_line = len(word) + 1
        else:
            final_text += f"{word} "
    # strip the trailing space at the end of the string
    final_text = final_text[:-1]
    return final_text


def make_mutliple_textboxes(texts):
    final_text = ""
    for text in texts:
        text = text.rstrip("\n")
        final_text += text
        lines = text.count("\n") + 1
        needed_linebreaks = -lines % 4 + 1
        final_text += "\n" * needed_linebreaks
    return final_text


def break_and_make_multiple_textboxes(texts):
    return make_mutliple_textboxes((break_lines(text) for text in texts))


if __name__ == "__main__":
    test_separator = "===================================="
    print(
        break_lines(
            "The <y<Spirit of the Sword>> guides the goddess' chosen hero to <r<Skyloft Village>>"
        )
    )
    print(test_separator)
    print(break_lines("Hey, you look like you have a Questions?"))
    print(test_separator)
    print(break_lines("Skyloft Peater/Peatrice's Crystals has Bug Net"))
    print(test_separator)
    print(
        make_mutliple_textboxes(
            [
                break_lines(
                    "The <y<Spirit of the Sword>> guides the goddess' chosen hero to <r<Skyloft Village>>"
                ),
                break_lines("Hey, you look like you have a Questions?"),
                "end",
            ]
        )
    )
    print(test_separator)
    print(
        break_lines(
            "<r<Knight Academy - Owlan's Crystals>> has <y<Eldin Song of the Hero Part>>"
        )
    )
    print(
        break_and_make_multiple_textboxes(
            [
                "<y<Progressive Sword>> can be found at <r<Sealed Grounds - Chest inside Sealed Temple>> at Noon in the after noon at 1235 <y<Progressive Sword>> can be found somewhere",
                "<r<Sandship - Bow>> has <y<SS Map>>",
            ]
        )
    )
