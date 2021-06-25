# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

from googlesearch import search


class ActionEnvConfig(Action):
    REQUEST_FREQUENCY = 0.5
    NUM_RETRIEVED_LINKS = 2

    def name(self) -> Text:
        return "action_env_config"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        entities = latest_message['entities']
        slots = tracker.slots.keys()

        has_programming_language = False
        has_package = False
        has_domain = False

        entities_plus_values = []

        result = []
        for el in entities:
            if el['entity'] == 'programming_language':
                has_programming_language = True
            if el['entity'] == 'package':
                has_package = True
            if el['entity'] == 'domain':
                has_domain = True

            entities_plus_values.append((el['entity'], el['value']))

            if el['entity'] in slots:
                result.append(SlotSet(el['entity'], el['value']))

        for entity_, value_ in entities_plus_values:
            links = self._get_links_for_entity(value_)
            if entity_ == 'package':
                dispatcher.utter_message(text="La link-urile de aici am gasit niste informatii despre {}: \n{}"
                                         .format(value_, links))
            if entity_ == 'programming_language':
                dispatcher.utter_message(text="Uite cateva tutoriale bune pentru {}: \n{}"
                                         .format(value_, links))

        return result

    @staticmethod
    def _get_links_for_entity(entity_value):
        resulting_links = ''

        query = entity_value + ' tutorial'
        for idx, link in enumerate(search(query, tld="com", num=ActionEnvConfig.NUM_RETRIEVED_LINKS,
                                          stop=ActionEnvConfig.NUM_RETRIEVED_LINKS,
                                          pause=ActionEnvConfig.REQUEST_FREQUENCY)):
            resulting_links += '\t{}. {}\n'.format(idx + 1, link)

        return resulting_links
