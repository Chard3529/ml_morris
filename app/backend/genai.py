"""
--- genai ---

This module interacts with the predictor to return forecast and metrics of the model.
Can be asked non specific questions about the model, and will call functions as needed. 
If no functions match the prompt it just responds normally. The genai acts as the interface
to the frontend
"""
from openai import OpenAI
import json
from .predictor import get_model_metrics, predict_gas_price_next_week, get_this_weeks_price

# The model i am using.
MODEL = "gpt-5-nano"

# System promt for the lmm agent
SYSTEM_PROMT = {
        "role": "system", 
        "content": """You are a helpful assistant. Your job is to use the provided tools to interact with a Linear regression model. 
        The model can predict the gas price next week in dollars per gallon, with the tool predict_gas_price_next_week.
        The get_model_metrics tool returns a tuple of time-series cross-validation metrics for the model. The first tuple value
        is mean RMSE, the second tuple is R2 score. """
        }

# Reads tools from tools.json:
with open('./backend/tools.json', "r") as f:
    TOOLS = json.load(f)

def handle_tool_calls(tool_calls):
    """
    Handles the tool calls by calling the appropriate local function
    takes an array of tool_calls from chatgpt, checks what functions are called
    stores result and returns an array of tool_messages.
    """
    tool_messages = []
    for tool_call in tool_calls:
        f_name = tool_call.function.name

        if (f_name == 'get_model_metrics'):
            result = get_model_metrics()

        elif (f_name == 'predict_gas_price_next_week'):
            result = predict_gas_price_next_week()
            
        elif (f_name == 'get_this_weeks_price'):
            result = get_this_weeks_price()
        
        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": f_name,
            "content": json.dumps(result)
        })
    return tool_messages

def ask_agent(prompt_text):
    """
    Handles all the main communication with the llm, creates an openai client,
    sends the user promt, and calls functions as needed. 
    Returns the message recieved from the llm
    """
    client = OpenAI()

    prompt = {"role": "user", "content": f"{prompt_text}"}
    
    # Sends system promt, message from user and tools to the gpt-5-nano
    response = client.chat.completions.create(
        model=MODEL,
        messages=[SYSTEM_PROMT,prompt],
        tools=TOOLS
    )

    # Get response from llm
    message = response.choices[0].message

    # Checks for calls to functions and and handles the response 
    if message.tool_calls:
        tool_messages = handle_tool_calls(message.tool_calls)
    
        final = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[SYSTEM_PROMT, prompt, message] + tool_messages
            
        )
        return final.choices[0].message.content
    # If there are no tool calls just return the message
    else:
        return message.content
    

