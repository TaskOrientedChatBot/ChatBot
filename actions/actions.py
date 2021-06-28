# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from functools import reduce
from googlesearch import search
from random import randrange


class ActionEnvConfig(Action):
    REQUEST_FREQUENCY = 0.5
    NUM_RETRIEVED_LINKS = 2
    POSSIBLE_PACKAGE_RESPONSES = ["La link-urile de aici am gasit niste informatii despre {}: \n{}",
                                  "Cateva link-uri despre {}: \n{}",
                                  "Am gasit cate ceva despre {}: \n{}",
                                  "Uite cateva link-uri interesante despre configurat {}: \n{}",
                                  "Daca esti interesat de {}, poti incepe cu link-urile de aici: \n{}"]
    POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES = ["Uite cateva tutoriale bune pentru {}: \n{}",
                                               "Ca sa inveti {}, poti incepe cu link-urile acestea: \n{}",
                                               "Link-urile de aici ar trebui sa contina suficiente informatii despre"
                                               "\n{}",
                                               "Poti incepe sa inveti despre {} cu link-urile de mai jos: \n{}",
                                               "Link-urile de aici ar trebui sa fie de folos pentru invatat {}: \n{}"]

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
                rand_response_idx = randrange(len(ActionEnvConfig.POSSIBLE_PACKAGE_RESPONSES))
                dispatcher.utter_message(text=ActionEnvConfig.POSSIBLE_PACKAGE_RESPONSES[rand_response_idx]
                                         .format(value_, links))
            if entity_ == 'programming_language':
                rand_response_idx = randrange(len(ActionEnvConfig.POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES))
                dispatcher.utter_message(text=ActionEnvConfig.POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES[rand_response_idx]
                                         .format(value_, links))

        return result

    @staticmethod
    def _get_links_for_entity(entity_value):
        info_query = '{} tutorial'
        resulting_links = ''

        query = info_query.format(entity_value)
        links = list(search(query, tld="com", num=ActionEnvConfig.NUM_RETRIEVED_LINKS,
                            stop=ActionEnvConfig.NUM_RETRIEVED_LINKS,
                            pause=ActionEnvConfig.REQUEST_FREQUENCY))
        links_plus_idx = list(zip(links, list(range(1, len(links) + 1))))
        links = list(map(lambda x: '\t' + str(x[1]) + '.' + x[0], links_plus_idx))
        resulting_links += reduce(lambda a, b: a + '\n' + b, links)

        return resulting_links


class ActionDomainGeneralKnowledge(Action):
    REQUEST_FREQUENCY = 0.5
    NUM_RETRIEVED_LINKS = 2
    POSSIBLE_PACKAGE_RESPONSES = ["La link-urile de aici am gasit niste informatii despre {}: \n{}",
                                  "Cateva informatii generale despre {}: \n{}",
                                  "Cateva lucruri despre {}: \n{}",
                                  "Uite cateva link-uri despre {}: \n{}",
                                  "Informatii de baza despre {} gasesti aici: \n{}"]
    POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES = ["Uite cateva tutoriale bune pentru {}: \n{}",
                                               "Informatii generale despre {}: \n{}",
                                               "Poti sa citesti aici despre {}, pentru inceput: \n{}",
                                               "Poti incepe sa inveti despre {} cu link-urile de mai jos: \n{}"]
    POSSIBLE_DOMAIN_RESPONSES = ["Aici am gasit niste informatii de baza despre {}: \n{}",
                                 "Cateva informatii generale despre domeniul de {}: \n{}",
                                 "Daca esti interesat de domeniul de {}, poti incepe sa citesti de aici: \n{}"]

    def name(self) -> Text:
        return "action_domain_general_knowledge"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        entities = latest_message['entities']
        slots = tracker.slots.keys()

        entities_plus_values = []

        result = []
        for el in entities:
            entities_plus_values.append((el['entity'], el['value']))

            if el['entity'] in slots:
                result.append(SlotSet(el['entity'], el['value']))

        for entity_, value_ in entities_plus_values:
            links = self._get_links_for_entity(value_)
            if entity_ == 'package':
                rand_response_idx = randrange(len(ActionDomainGeneralKnowledge.POSSIBLE_PACKAGE_RESPONSES))
                dispatcher.utter_message(text=ActionDomainGeneralKnowledge.POSSIBLE_PACKAGE_RESPONSES[rand_response_idx]
                                         .format(value_, links))
            if entity_ == 'programming_language':
                rand_response_idx = randrange(len(ActionDomainGeneralKnowledge.POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES))
                dispatcher.utter_message(text=ActionDomainGeneralKnowledge
                                         .POSSIBLE_PROGRAMMING_LANGUAGE_RESPONSES[rand_response_idx]
                                         .format(value_, links))
            if entity_ == 'domain':
                rand_response_idx = randrange(len(ActionDomainGeneralKnowledge.POSSIBLE_DOMAIN_RESPONSES))
                dispatcher.utter_message(text=ActionDomainGeneralKnowledge.POSSIBLE_DOMAIN_RESPONSES[rand_response_idx]
                                         .format(value_, links))

        return result

    @staticmethod
    def _get_links_for_entity(entity_value):
        info_query = '{} general information'
        resulting_links = ''

        query = info_query.format(entity_value)
        links = list(search(query, tld="com", num=ActionDomainGeneralKnowledge.NUM_RETRIEVED_LINKS,
                            stop=ActionDomainGeneralKnowledge.NUM_RETRIEVED_LINKS,
                            pause=ActionDomainGeneralKnowledge.REQUEST_FREQUENCY))
        links_plus_idx = list(zip(links, list(range(1, len(links) + 1))))
        links = list(map(lambda x: '\t' + str(x[1]) + '.' + x[0], links_plus_idx))
        resulting_links += reduce(lambda a, b: a + '\n' + b, links)

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
