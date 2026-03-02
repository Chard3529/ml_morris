"""
--- genai ---

This module interacts with the predictor to return forecast and metrics of the model.
Can be asked non specific questions about the model, and will call functions as needed. 
If no functions match the prompt it just responds normally. The genai acts as the interface
to the frontend
"""
from openai import OpenAI
import json
from .predictor import get_model_metrics, predict_gas_price_next_week

# Define tools in json format:
tools = [
    {
        "type": "function",

        "function": {
            "name": "get_model_metrics",
            "description": "Returns a tuple with metrics for the model: (mean_RSME , mean_R2_score)",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",

        "function": {
            "name": "predict_gas_price_next_week",
            "description": "Returns a prediction of the gas price next week",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def ask_agent(prompt_text):
    client = OpenAI()

    engineered_prompt = {
        "role": "system", 
        "content": """You are a helpful assistant. Your job is to use the provided tools to interact with a Linear regression model. 
        The model can predict the gas price next week in dollars per gallon, with the tool predict_gas_price_next_week.
        The get_model_metrics tool returns a tuple of time-series cross-validation metrics for the model. The first tuple value
        is mean RMSE, the second tuple is R2 score."""
        }
    prompt = {"role": "user", "content": f"{prompt_text}"}
    
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[engineered_prompt,prompt],
        tools=tools
    )

    message = response.choices[0].message

    # Checks for calls to functions and and handles the response 
    if message.tool_calls:
        tool_messages = []
        for tool_call in message.tool_calls:
            f_name = tool_call.function.name

            if (f_name == 'get_model_metrics'):
                result = get_model_metrics()

            elif (f_name == 'predict_gas_price_next_week'):
                result = predict_gas_price_next_week()
            
            tool_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": f_name,
                "content": json.dumps(result)
            })
            
        final = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[ engineered_prompt, prompt, message] + tool_messages
            
        )
        return final.choices[0].message.content
    # If there are no tool calls just return the message
    else:
        return message.content
    

