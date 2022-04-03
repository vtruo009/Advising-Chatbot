from google.cloud import dialogflow_v2, storage



def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    # Replace with appropriate json file obtained from DialogFlow
    storage_client = storage.Client.from_service_account_json('.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    # print(buckets)
    
def CheckIntent(user_query):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path("adviserbot-bluy", "testrun1")
    intent_client = dialogflow_v2.IntentsClient()
    parent = dialogflow_v2.AgentsClient.agent_path("adviserbot-bluy")
    intents = intent_client.list_intents(request={"parent": parent})
    # for intent in intents:
    #     print("Intent display name: {}".format(intent.display_name))
    text_input = dialogflow_v2.TextInput(text=user_query, language_code="en-US")
    query_input = dialogflow_v2.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    # if response.query_result.intent.display_name == 'Check Prerequisites':
    intent = response.query_result.intent.display_name
    params = response.query_result.parameters.get('course')
    # Get the prereqs here and print the prereqs
    print(response.query_result.fulfillment_text)
    # print(
    #     "Detected intent: {} (confidence: {})\n".format(
    #         response.query_result.intent.display_name,
    #         response.query_result.intent_detection_confidence,
    #     )
    # )
    if intent == "Check Sufficiency":
        return (intent, [response.query_result.parameters.get("course"), response.query_result.parameters.get("course1")])
    return intent, params