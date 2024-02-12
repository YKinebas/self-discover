import openai
import requests

class select:
    '''
    Interacts with LLM API to make requests
    Output is message content as a string
    token supplied needs to be valid for the model being used.
    
    Example usage:
    
    example = model(model_name="gpt4", token="your-token")
    response = example.request(prompt="your-prompt")
    '''
    def __init__(self, model_name, token):
        self.token = token
        self.model = self._get_model_method(model_name)

    def _get_model_method(self, model_name):
        if model_name == "mistral":
            return self.mistral
        elif model_name == "mixtral":
            return self.mixtral
        elif model_name == "gpt4":
            return self.gpt4
        elif model_name == "gpt35":
            return self.gpt35
        elif model_name == "qa":
            return self.qa
        elif model_name == "summary":
            return self.summary
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def request(self, prompt, *args, **kwargs):
        return self.model(prompt, self.token, *args, **kwargs)
    
    def mistral(self, prompt, token):
        '''
        Uses mistral 7b instruct endpoint on HF
        '''
        auth_header = "Bearer " + str(token)
        API_URL = "https://sxh2vro9g3e0zrga.eu-west-1.aws.endpoints.huggingface.cloud"
        headers = {"Authorization": auth_header}
        
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        input = "[INST]" + str(prompt) + "[/INST]"
        output = query({
            "inputs": input,
        })
        return output[0]['generated_text']
    
    def mixtral(self, prompt, token):
        '''
        Uses mixtral 8x7b  endpoint on HF
        '''
        auth_header = "Bearer " + str(token)
        API_URL = "https://eh3asj67ho60uvb3.us-east-1.aws.endpoints.huggingface.cloud"
        headers = {"Authorization": auth_header}
        
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        input = "[INST]" + str(prompt) + "[/INST]"
        output = query({
            "inputs": input,
        })
        try:
            return output
        except Exception as e:
            print("Error interacting with HF endpoint:")
            print(str(e))
    
    def gpt4(self, prompt, token, temperature = 0.3, asJson = True):
        '''
        Uses GPT-4 model using business API
        Output is string
        '''
        openai.api_key = token
        if asJson:
            completion = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature = temperature,
            response_format={ "type": "json_object" }
            )
        elif not asJson:
            completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature = temperature
            )
        response = completion.choices[0].message
        return str(response["content"])
    
    def gpt35(self, prompt, token, temperature = 0.3, asJson = True):
        '''
        Uses gpt-3.5-turbo-1106 model using business API
        If formatJson is true, output is json object
        '''
        openai.api_key = token
        if asJson:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature = temperature
            )
        elif not asJson:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature = temperature
            )
        response = completion.choices[0].message
        return str(response["content"])
    
    def qa(self, prompt, context, token):
        '''
        Returns simple summaries of text using HF free Interface API
        Uses roberta-base-squad2 model
        '''
        API_TOKEN = token
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        data = query(
            {
                "inputs": {
                    "question": prompt,
                    "context": context,
                }
            }
            )
        return str(data)
     
    def summary(self, prompt, token):
        '''
        Returns simple summaries of text using HF free Interface API
        Uses bart-large-cnn model
        '''
        API_TOKEN = token
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        data = query(
            {
                "inputs": prompt,
                "parameters": {"do_sample": False},
            }
        )
        return str(data)