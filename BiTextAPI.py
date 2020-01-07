import requests
import json

# User token, required for API access
oauth_token = '243041a5c8244832ada0b9db1e98772a'

# API request data: Language and text to be analyzed
user_language = "eng"
user_text = "Your house is beautiful but the street is not great"
#user_text = input("Escribe el texto a analizar: ");

print ("\nBITEXT API. Sentiment Analysis endpoint. Python sample code\n")
print ("--------------------------------------------------\n\n")

# Building the POST request to sentiment analysis endpoint
endpoint = "https://svc02.api.bitext.com/sentiment/"
headers = { "Authorization" : "bearer " + oauth_token, "Content-Type" : "application/json" }
params = { "language" : user_language, "text" : user_text }

# Sending the POST request
res = requests.post(endpoint, headers=headers, data=json.dumps(params))

# Processing the result of the POST request
post_result = json.loads(res.text).get('success')   # Success of the request
post_result_code = res.status_code                  # Error code, if applicable
post_msg = json.loads(res.text).get('message')      # Error message, if applicable
action_id = json.loads(res.text).get('resultid')    # Identifier to request the analysis results

print("POST: '" + post_msg + "'\n\n");

# 401 is the error code corresponding to an invalid token
if post_result_code == 401:
    print("Your authentication token is not correct\n");

if (post_result):
    print("Waiting for analysis results...\n\n");

    # GET request loop, using the response identifier returned in the POST answer
    analysis = None
    while analysis == None:
        res = requests.get(endpoint + action_id + '/', headers=headers);

        if res.status_code == 200 :
            analysis = res.text;

    # The loop ends when we have response to the GET request
    get_msg = res.reason
    print("GET: '" + get_msg + "'\n\n");

    # In the GET response we have the result of the analysis
    print("Analysis results:\n\n");
    print(analysis + "\n");

    #-----------------------------------------------------------
    #print(res.json()["resultid"]) #Testear
    score = res.json()["sentimentanalysis"][0]["score"]
    #print(score)
    sentiment_analysis = res.json()["sentimentanalysis"]
    #print(sentiment_analysis)
    longitud_lista = len(sentiment_analysis)
    #print(longitud_lista)
    
    score_total = 0
    # Recorremos la lista
    for valor in sentiment_analysis:
        valorActual = float(valor['score'])
        score_total = score_total +  valorActual
        #print(score_total)
    print(score_total)

    if score_total > 0.0:
        print("La emoción del mensaje es positiva");
    elif score_total < 0.0:
        print("La emoción del mensaje es negativa");
    else: 
        print("Es un mensaje neutro");
    
