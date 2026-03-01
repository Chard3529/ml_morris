# Machine Learning Morris

A machine learning web-project that lets you train prediction models and interact with them through a LLM. 

## 3 modules
### Model_trainer
- Responsible for training models on data and provides model for backend api
- Ran at spesific times for prestored data
- Can be called with new data from frontend

### Backend-API
- Requests model with data from frontend
- Uses model to make predictions.
- Interaction happens trough an llm with tools.
- Store tools in json

### Frontend
- Simple webpage, an input field, send data and messages to backend.
- Get output produced by LLM using provided tools. 
