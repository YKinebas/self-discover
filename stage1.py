from llm import models
import json
import ast
import requests

class stage1:

    def __init__(self, task, token):
        self.task = "<task>" + task + "<\task>"
        self.token = token

        '''
        select model to be used. API key should match model requested,
        and different settings might be needed for different models.
        I tend to use gpt-3.5 for the price/performance tradeoff.
        '''
        self.ai = models.select(
            model_name="gpt4",
            token = token
        )

        #Import the variables
        with open("reasoningModules.json","r") as f:
            self.modules = json.load(f)

        with open("stage1Prompts.json","r") as f:
            self.prompts = json.load(f)

    def select(self):
        #Stage 1 actions
        #Select stage
        selectResponse = self.ai.request(
            prompt=
            self.prompts["primer"]+
            str(self.modules)+
            self.task+
            self.prompts["selectPrompt"]
        )
        selectedModules = {
            "Reasoning Modules" : ast.literal_eval(
                selectResponse)["response"]
            }
        print("Selected Modules:\n"+
            str(selectedModules))
        
        return selectedModules

    def adjust(self):
        selectedModules = self.select()
        #Adjust stage
        adjustResponse = self.ai.request(
            prompt=
            self.prompts["primer"]+
            str(selectedModules)+
            self.task+
            self.prompts["adjustPrompt"],
            temperature = 0.7
        )
        
        adjustedModules = {
            "Reasoning Modules" : ast.literal_eval(
                adjustResponse)["Reasoning Modules"]
            }

        print("Adjusted Modules:\n"+
            str(adjustedModules))
        
        return adjustedModules

    def implement(self):
        adjustedModules = self.adjust()
        #Implement stage
        implementResponse = self.ai.request(
            prompt=
            self.prompts["primer"]+
            str(adjustedModules)+
            self.task+
            self.prompts["implementPrompt"],
            temperature = 0.7
        )
        print("Implementation:\n"+
            str(implementResponse))

        return implementResponse