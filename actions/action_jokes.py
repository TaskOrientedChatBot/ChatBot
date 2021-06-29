from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from utils.paths import get_data_dir
import random
import json
import os


class ActionTellJoke(Action):
    JOKES_FILE = os.path.join(get_data_dir(), "jokes.json")
    JOKES_INTRO = [
        "Am râs mult la următoarea glumă:",
        "O glumă foarte bună ar fi:",
        "Mi-a plăcut mult următoarea glumă:",
        "Una din preferatele mele este:",
        "Sunt sigur ca o sa găsești amuzantă următoarea glumă:"
    ]

    def name(self) -> Text:
        return "action_tell_joke"

    def __init__(self):
        self.jokes = None
        with open(self.JOKES_FILE, "r") as fp:
            self.jokes = json.load(fp)

        if self.jokes is None:
            raise ValueError("Jokes file couldn't be opened.")

        if not len(self.jokes):
            raise ValueError("Jokes file can't be empty.")

        self.num_jokes = len(self.jokes)
        self.current_joke = 0

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        joke = self.jokes[self.current_joke]
        text, image = joke["text"], joke["image"]

        message = ""
        if text:
            message += "{}\n".format(text)
        if image:
            if not message:
                message += "{}\n".format(random.choice(self.JOKES_INTRO))
            message += "Link: {}".format(image)

        dispatcher.utter_message(text=message)
        self.current_joke += 1
        # just reset the index for joke if all of them have been told
        if self.current_joke >= self.num_jokes:
            self.current_joke = 0
        return []
