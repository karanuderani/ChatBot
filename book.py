import os
import sys
import json
import uuid


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )
    


# Agent acess token: 

CLIENT_ACCESS_TOKEN = 'db75b21223d944f28331d2a0239a9ee5'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    # some unuque session id for user identification
    session_id = uuid.uuid4().hex

    #f = open("entities\place.json", "r")
    #json_data = json.loads(f.read())

    #entries = json_data['entries']

    #apiai.UserEntity("place", entries, session_id)
    #f = open("entities\place.json", "r")
    #json_data = json.loads(f.read())

    #entries = json_data['entries']
    #apiai.UserEntity("quantity", entries, session_id)
    
     

    while True:
        print(u"> ", end=u"")
        user_message = input()

        if user_message == u"exit":
            break
        request = ai.text_request()
        request.query = user_message

        response = request.getresponse().read().decode('utf-8')

        response = json.loads(response)
        result = response['result']
        action = result.get('action')

        if action is not None:
            if action == u"@booking":
                parameters = result['parameters']
                if result['parameters']['date'] and result['parameters']['childs'] and result['parameters']['adults'] and result['parameters']['location']:
                    amount = int(result['parameters']['adults']) * 1200 + int(result['parameters']['childs'])*800
                    print("The booking to " + result['parameters']['location'] + " has been made for " + result['parameters']['date'] + " for " +result['parameters']['adults'] + "Adults and " + result['parameters']['childs'] + " children")
                    print("Total booking amount is " + str(amount)+"/- Rupees")
                    with open('input.json', 'w') as outfile:
                        json.dump(response, outfile)

                    data = {}
                    data['location'] = result['parameters']['location']
                    data['date'] = result['parameters']['date']
                    data['adults'] = result['parameters']['adults']
                    data['childs'] = result['parameters']['childs']
                    data['amount'] = str(amount)

                    with open('output.json','w') as outfile:
                        json.dump(data, outfile)
                    
                else:
                    print (response['result']['fulfillment']['speech'])
            elif action == u"weather":
                if result['parameters']['date'] and result['parameters']['geo-city']:
                    parameters = result['parameters']
                    if parameters['condition']:
                        print ("It won't")
                    print(" The weather is going to be the {value}")
                    data = {}
                    data['date'] = result['parameters']['date']
                    data['geo-city'] = result['parameters']['geo-city']
                    data['condition'] = result['parameters']['condition']
                    with open('input2.json','w') as outfile:
                        json.dump(data, outfile)
                
                    data = {}
                    data['weather'] = "rainy" #Can be anything based on the result
                    data['response'] = "False" #Can be true or false based on the current weather
                    with open('output2.json','w') as outfile:
                        json.dump(data, outfile)
                
                else:
                    print (response['result']['fulfillment']['speech'])
                
            else:
                print (response['result']['fulfillment']['speech'])

        
        
        
if __name__ == '__main__':
    main()
