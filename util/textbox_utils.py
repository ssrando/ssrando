CHARACTERS_PER_LINE = 39


def break_lines(text, characters_per_line=CHARACTERS_PER_LINE):
    words = text.split()
    final_text = ""
    chars_in_line = 0
    for word in words:
        chars_in_line += (
            len(word) + 1
        )  # add 1 to account for the space at the beginning of the word
        if chars_in_line >= characters_per_line:
            final_text = final_text[
                : len(final_text) - 1
            ]  # strip trailing space at the end of each line
            final_text += f"\n{word} "
            chars_in_line = len(word) + 1  # account for the space again
        else:
            final_text += f"{word} "
    final_text = final_text[
        : len(final_text) - 1
    ]  # strip the trailing space at the end of the string
    return final_text


def make_mutliple_textboxes(texts):
    final_text = ""
    for text in texts:
        final_text += text
        lines = text.count("\n")
        while lines % 4 != 0:
            final_text += "\n"
            lines += 1
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
