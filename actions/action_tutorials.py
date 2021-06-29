from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from functools import reduce


class ActionLearnSubject(Action):
    INTRO_MESSAGE = "Ca să înveți {}, poți începe cu link-urile acestea: \n"
    TUTORIAL = {
        "cv": "- http://cs231n.stanford.edu/\n"
              "- https://www.tensorflow.org/tutorials/images/cnn\n"
              "- https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html\n",
        "nlp": "- http://web.stanford.edu/class/cs224n/\n"
               "- https://www.tensorflow.org/hub/tutorials/tf2_text_classification\n"
               "- https://pytorch.org/tutorials/beginner/deep_learning_nlp_tutorial.html\n",
    }
    ENT_MAPPING = {
        "cv": "Computer Vision",
        "nlp": "Natural Language Processing"
    }

    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_respond_learn_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = [ent["entity"] for ent in tracker.latest_message["entities"]]
        if len(entities) > 1:
            ent_message = reduce(
                lambda a, b: ActionLearnSubject.ENT_MAPPING[a] + " and " + ActionLearnSubject.ENT_MAPPING[b], entities)
        else:
            ent_message = ActionLearnSubject.ENT_MAPPING[entities[0]]

        response = ActionLearnSubject.INTRO_MESSAGE.format(ent_message)
        for entity in entities:
            response += "{}: \n".format(ActionLearnSubject.ENT_MAPPING[entity])
            response += ActionLearnSubject.TUTORIAL[entity]

        dispatcher.utter_message(text=response)
        return []
