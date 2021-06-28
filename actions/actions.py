# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from googlesearch import search
from functools import reduce


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


class ActionRespondAIQuestions(Action):
    QUERIES = {
        "learn_ai/ask_ai": "Artificial Intelligence definition",
        "learn_ai/ask_dl": "Deep learning definition",
        "learn_ai/ask_ml": "Machine learning definition",
    }

    RESOURCES_EXHAUSTED = "Am epuizat informatiile despre aceasta tema. Continui cautarea pe google.com pentru: "

    def name(self) -> Text:
        return "action_respond_ai_questions"

    def __init__(self):
        self.counter = 0
        self.state = None
        self.mem_responses = None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"]["name"]
        response_selector = tracker.latest_message.get("response_selector", None)
        response = response_selector["default"]["response"]
        intent_response_key = response["intent_response_key"]
        responses = response["responses"]

        if intent == "ask_for_more":
            if self.state is None:
                dispatcher.utter_message(text="Despre ce subiect ai dori sa afli mai multe? :)")
                return []

            # we should check if in ask_for_more intent we have a specific entity (ml, dl, ai)
            # if we don't, it means we are referring to the previous one
            # sometimes the bot can get the answers wrong, so we'd better retrieve them from a buffer
            if self.counter < (len(self.mem_responses) - 1):
                self.counter += 1
            else:
                query = self.QUERIES[self.state]
                dispatcher.utter_message(self.RESOURCES_EXHAUSTED + query)
                links = list(search(query, lang="en", num=5, stop=5, pause=0.5))
                response = "Am gasit urmatoarele rezultate care te-ar putea ajuta:\n"
                response += reduce(lambda a, b: a + "\n" + b, links)

                dispatcher.utter_message(text=response)

                self.state = None
                self.counter = 0
                return []
        else:
            if intent_response_key != self.state:
                self.mem_responses = responses
                self.state = intent_response_key
                self.counter = 0
            else:
                self.counter += 1

        response = self.mem_responses[self.counter]["text"]
        dispatcher.utter_message(text=response)

        return []
