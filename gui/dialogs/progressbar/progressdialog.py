import random
from typing import Optional
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QProgressDialog, QLabel

tips = [
    "The Bomb Bag and the Hook Beetle are often interchangeable. In places you would normally be expected to use the Bomb Bag, look for nearby bomb flowers to grab with the Hook Beetle.",
    "Think you're stuck somewhere with no way to get back to safety? Look around for a bomb flower. Dying will safely return you to the last statue you saved at or the last loading zone you crossed.",
    "Logic assumes that you will use keys in the worst way possible, so it is impossible to lock yourself out of access to keys.",
    "Enabling tricks is a fun way to expand the logical possibilities of the randomizer, but some tricks can greatly increase the difficulty of seeds.",
    "Fi can give you some helpful information about the seed, such as which dungeons are required and how many keys you have. You can always call her with D-pad down, even without a sword.",
    "Hold down the B button to quickly advance text.",
    "Flooded Faron Woods can be entered by talking to the Water Dragon inside the Great Tree.",
    "Bokoblin Base can be entered by talking to the gossip stone in the first room of Eldin Volcano.",
    "You can end Fledge's Pumpkin Archery minigame early by shooting the bell atop the Knight Academy.",
    "If a character tells you to 'come back later if you want something', this means that the 'Story-based Requirements' setting is enabled. You'll need to do additional things to get that person's item.",
]


class ProgressDialog(QProgressDialog):
    def __init__(self, title, description, max_value):
        QProgressDialog.__init__(self)
        self.step_text = description
        self.tip_text = random.choice(tips)
        self.hint_timer = QTimer()
        self.hint_timer.timeout.connect(self.new_tip)
        self.hint_timer.start(7500)
        self.setWindowTitle(title)
        label = QLabel(description)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLabel(label)
        self.setMaximum(max_value)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setFixedWidth(400)
        self.setAutoReset(False)
        self.setCancelButton(None)
        self.show()

    def new_tip(self):
        self.tip_text = random.choice(tips)
        self.update_label_text(tip_text=self.tip_text)

    def set_current_action(self, text: str) -> None:
        self.update_label_text(step_text=text)

    def update_label_text(
        self, step_text: Optional[str] = None, tip_text: Optional[str] = None
    ) -> None:
        label_text = ""
        if step_text:
            label_text += step_text
            self.step_text = step_text
        else:
            label_text += self.step_text
        label_text += "\n\n"
        if tip_text:
            label_text += tip_text
            self.tip_text = tip_text
        else:
            label_text += self.tip_text
        self.setLabelText(label_text)
