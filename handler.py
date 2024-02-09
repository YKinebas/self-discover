from llm import models
import json
import ast
import requests

#API Keys, add your own
OPENAI_TOKEN = "your key here"
HF_API_TOKEN = "your key here"

'''
select model to be used. API key should match model requested,
and different settings might be needed for different models.
I tend to use gpt-3.5 for the price/performance tradeoff.
'''
ai = models.select(
    model_name="gpt35",
    token = OPENAI_TOKEN
    )

#Import the variables
with open("reasoningModules.json","r") as f:
    modules = json.load(f)

with open("stage1Prompts.json","r") as f:
    prompts = json.load(f)

#Test task and response
task = "Solve this puzzle: You have five boxes in a row numbered 1 to 5,"\
"in which a cat is hiding. Every night he jumps to an adjacent box, and "\
"every morning you have one chance to open a box to find him. How do you "\
"win this game of hide and seek?"

'''
Puzzle answer:
Check boxes 2, 3, and 4 in order until you find him. Here’s why: He’s either in an
 odd or even-numbered box. If he’s in an even box (box 2 or 4) and you check box 2
and here’s there, great; if not you know he was in box 4, which means the next 
night he will move to box 3 or 5. The next morning, check box 3; if he’s not there 
that means he was in box 5 and so the next night he’ll be in box 4, and
you’ve got him. If he was in an odd-numbered box to begin with (1, 3, or 5),
though, you might not find him in that first round of checking boxes 2, 3
and 4. But if this is the case, you know that on the fourth night he’ll
have to be in an even-numbered box (because he switches every night: 
odd, even, odd, even), so then you can start the process again as described above. 
This means if you check boxes 2, 3, and 4 in that order, you will find him within
 two rounds (one round of 2, 3, 4; followed by another round of  2, 3, 4).
'''

taskPrompt = "<task>" + task + "<\task>"

#Stage 1 actions
#Select stage
selectResponse = ai.request(
    prompt=
    prompts["primer"]+
    str(modules)+
    taskPrompt+
    prompts["selectPrompt"]
)

selectedModules = {
    "Reasoning Modules" : ast.literal_eval(
        selectResponse)["response"]
    }
print("Selected Modules:\n"+
      str(selectedModules))

#Adjust stage
adjustResponse = ai.request(
    prompt=
    prompts["primer"]+
    str(selectedModules)+
    taskPrompt+
    prompts["adjustPrompt"]
)

adjustedModules = {
    "Reasoning Modules" : ast.literal_eval(
        adjustResponse)["response"]
    }

print("Adjusted Modules:\n"+
      str(adjustedModules))

#Implement stage
implementResponse = ai.request(
    prompt=
    prompts["primer"]+
    str(adjustedModules)+
    taskPrompt+
    prompts["implementPrompt"]
)
print("Implementation:\n"+
      str(implementResponse))
'''
The prompts need changing to improve performance, currently repeating the selected modules and sometimes deleting them.
No Adjustment being made
Implementation does not create a step-flow, json mode may need switching off
'''