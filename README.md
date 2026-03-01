# Machine Learning Morris

A machine learning web-project that lets you train prediction models and interact with them through a LLM. 

## Description of contents
### Backend
A fast-api application that provides acess to the modules trough endpoints

#### model_trainer
- Responsible for training models on data and provides model for backend api

#### data_handler
- fetch data from api
- recieve data from frontend

#### llm_model
- Interacts with model and data trough tools

### Frontend
- Simple webpage, an input field, send data and messages to backend.
- Get output produced by LLM using provided tools. 
