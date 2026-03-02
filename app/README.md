# Gas price prediction demo

### To run the application:

1. Build the docker image by running:
```Bash
$ docker build -t gas_prediction_demo .
```

2. Write your openai key to an env file named .env, and put it in the
"/put_your_env_file_here"-folder. 

3. Run the docker application with the command:
```Bash
$ docker run --name gas_predictor -p 8501:8501 -d --env-file ./put_your_env_file_here/.env  gas_prediction_demo  
```
4. Open the webpage running on localhost in your browser:
http://localhost:8501

