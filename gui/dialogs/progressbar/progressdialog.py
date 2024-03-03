import random
from typing import Optional
from PySide6.QtCore import QEvent, QObject, Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QProgressDialog, QLabel, QPushButton

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
    "If you don't have a sword, you are expected to wait in-front of Deku Babas or sneak past Beamos to advance through the world.",
]


class ProgressDialog(QProgressDialog):
    def __init__(self, title, description, max_value, cancel=None):
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

        self.installEventFilter(self)

        if cancel:
            # This is a bit awkward but we cannot use the builtin self.canceled signal,
            # single the dialog will always automatically close when the signal
            # is triggered. So if our owner can handle cancellation, we rewire the
            # button to trigger our own callback.
            self.user_cancel = cancel
            cancel_button: QPushButton = self.findChild(QPushButton)
            cancel_button.clicked.disconnect(self.canceled)
            cancel_button.clicked.connect(cancel)
        else:
            # Otherwise cancellation is not allowed and the button is hidden.
            self.user_cancel = lambda: None
            self.setCancelButton(None)

        self.show()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self:
            if event.type() in (
                QEvent.KeyPress,
                QEvent.ShortcutOverride,
                QEvent.KeyRelease,
            ):
                if event.key() in (
                    Qt.Key_Return,
                    Qt.Key_Escape,
                    Qt.Key_Enter,
                ):
                    self.user_cancel()
                    # Always prevent attempts to cancel the dialog via ESC - the owner
                    # is responsible for closing this dialog when progress is done or
                    # cancellation has explicitly been handled.
                    event.accept()
                    return True
        return super(QProgressDialog, self).eventFilter(obj, event)

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
