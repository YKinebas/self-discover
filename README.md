Self-Discover Module
    
    Based on paper:

        **Self-Discover: Large Language Models Self-Compose Reasoning Structures**

        Authors: Pei Zhou and Jay Pujara and Xiang Ren and Xinyun Chen and Heng-Tze Cheng and Quoc V. Le and Ed H. Chi and Denny Zhou and Swaroop Mishra and Huaixiu Steven Zheng
        Year 2024

        eprint 2402.03620

        https://arxiv.org/abs/2402.03620

    This is an unofficial illustration of the consepts presented in the paper, used for research and educational purposes only.

Structure:

    **llm.models** holds methods for interaction with openai and HF APIs. API keys need to be provided in each case.
    **Stage1prompt.json** contain the prompts for the Self-Discovery phase of the framework
    **reasoningModules.json** hold the 39 reasoning modules proposed in the source paper
    **stage1.py** is where the self discovery logic happens
    **stage2.py** is where the central logic sits, this is where you can play with the framework