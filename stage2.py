from llm import models
import json
import ast
import requests
from stage1 import stage1

#API Keys, add your own
OPENAI_TOKEN = "your key here"
HF_API_TOKEN = "your key here"

#Test task and response
easy = "A farmer wants to cross a river and take with him a wolf, a goat and a"\
" cabbage. He has a boat, but it can only fit himself plus either the wolf, the"\
" goat or the cabbage. If the wolf and the goat are alone on one shore, the wolf "\
"will eat the goat. If the goat and the cabbage are alone on the shore, the goat"\
" will eat the cabbage. How can the farmer bring the wolf, the goat and the cabbage"\
"across the river without anything being eaten?"

'''
Easy Puzzle Answer:
First, the farmer takes the goat across. The farmer returns alone and then takes the wolf across, but returns with the goat. Then the farmer takes the cabbage across, leaving it with the wolf and returning alone to get the goat.
'''

hard = "Solve this puzzle: You have five boxes in a row numbered 1 to 5,"\
"in which a cat is hiding. Every night he jumps to an adjacent box, and "\
"every morning you have one chance to open a box to find him. How do you "\
"win this game of hide and seek?"

'''
Hard Puzzle answer:
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
#choose difficulty:
task = easy
#get self-discovered instructions from stage1
stage1 = stage1(task=task,token=OPENAI_TOKEN)
instructions = stage1.implement()

#request a solution
ai = models.select(
    model_name="gpt4",
    token = OPENAI_TOKEN
)

prompt = "By filling in the blank fields in the attached json follow the instructions one by one to solve the following task. Respond in json"\
"Provide an explanation for why your answer is correct"\
+ task + "<instructions>" + instructions + "</instructions>"

response = ai.request(
            prompt=prompt,
            temperature = 0.7
            )

print("Solution:\n" + response)