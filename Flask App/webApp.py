from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json
import requests

app = Flask(__name__)



def loadApiKeys(mltype):
    with open('azurekeys.json') as data_file:
        apikeys = json.load(data_file)
    if mltype=="classification":
        return apikeys['classification']
    elif mltype=="prediction":
        return apikeys['prediction']
    else:
        print("Algorithm doesn't exist")



@app.route('/')
def index():

    return render_template('index.htm')

@app.route('/prediction')
def render_prediction():
    return render_template('prediction.html')

@app.route('/classification')
def render_classification():
    return render_template('classification.html')

	
#owner pages

@app.route('/ownerAnalysis')
def ownerAnalysis():
    return render_template('ownerAnalysis.html')

@app.route('/eda')
def eda():
    return render_template('eda.html')

	
@app.route('/ownerHome')
def ownerHome():
    return render_template('ownerHome.htm')



@app.route('/ownerPrediction')
def ownerPrediction():
    return render_template('ownerPrediction.htm')

#userpages

@app.route('/user_home')
def user_home():
    return render_template('user_home.htm')

@app.route('/userPrediction')
def userPrediction():
    return render_template('userPrediction.htm')

@app.route('/userAnalytics')
def userAnalytics():
    return render_template('userAnalytics.htm')
	
#investor Pages
@app.route('/investorHome')
def investorHome():
    return render_template('investorHome.htm')

@app.route('/investorPrediction')
def investorPrediction():
    return render_template('investorPrediction.htm')

@app.route('/investorAnalysis')
def investorAnalysis():
    return render_template('investorAnalysis.htm')


@app.route('/prediction/getPrediction', methods=['POST'])
def get_prediction():
    try:
        apikeys=loadApiKeys('prediction')
        if apikeys == None:
            print("Api Keys file has some issue")
            return_dict = {"predicted_price":"Some Error occured with api keys file"}
            return json.dumps(return_dict)
        else:

            host_response_rate=request.json['host_response_rate']
        host_total_listings_count=request.json['host_total_listings_count']
        accommodates=request.json['accommodates']
        bathrooms=request.json['bathrooms']
        beds=request.json['beds']
        security_deposit=request.json['security_deposit']
        number_of_reviews=request.json['number_of_reviews']
        review_scores_rating=request.json['review_scores_rating']
        reviews_per_month=request.json['reviews_per_month']
        ScoredRating=request.json['ScoredRating']
        moderatePolicy=request.json['moderatePolicy']
        flexiblePolicy=request.json['flexiblePolicy']
        Apartment=request.json['Apartment']
        Privateroom=request.json['Privateroom']
        Notinstant_bookable=request.json['Notinstant_bookable']
        superhost=request.json['superhost']


        algoType = request.json['algoType']
    #print(str(algoType)+"\t"+str(credit_score)+"\t"+str(og_first_time_home_buyer)+"\t"+str(og_upb)+"\t"+str(og_loan_term)+"\t"+str(og_quarter_year)+"\t"+str(og_seller_name)+"\t"+str(og_servicer_name))
    #make ai call
        if algoType=="pred_df":
            url=apikeys['boosteddecisiontree']['url']
            api_key=apikeys['boosteddecisiontree']['apikey']
        elif algoType=="pred_nn":
            url=apikeys['neuralnetwork']['url']
            api_key=apikeys['neuralnetwork']['apikey']
        elif algoType=="pred_lr":
            url=apikeys['linearregression']['url']
            api_key=apikeys['linearregression']['apikey']


        data =  {

            "Inputs": {

                "input1":
                    {
                        "ColumnNames": ["host_response_rate", "host_total_listings_count", "accommodates", "bathrooms", "beds", "security_deposit", "cleaning_fee","number_of_reviews","review_scores_rating","reviews_per_month","ScoredRating","moderatePolicy","flexiblePolicy","strictPolicy","Apartment","Privateroom","Notinstant_bookable","superhost"],
                        "Values": [ [host_response_rate,host_total_listings_count,accommodates,bathrooms,beds,security_deposit,cleaning_fee,number_of_reviews,review_scores_rating,reviews_per_month,ScoredRating,moderatePolicy,flexiblePolicy,strictPolicy,Apartment,Privateroom,Notinstant_bookable,superhost]]
                    },        },
            "GlobalParameters": {
            }
        }
        body = str.encode(json.dumps(data))

        #url = 'https://ussouthcentral.services.azureml.net/workspaces/5de0e8bd28f74cf9a40babb3f1799a53/services/300d6267d2f843c9a5975621ff077a09/execute?api-version=2.0&details=true'
        #api_key = 'wQWgTpa3GyVACzg7Q6jVDdwt5JEDnfdvqqG21PKDr+UHmZWRQJh1XfrtLVON846vEDEXoDgnruZ1s9zd4Drzyw==' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        response = requests.post(url, data=body,headers=headers)
        #print(response.content)

        response_json=json.loads(response.content)
        predicted_price=response_json['Results']['output1']['value']['Values'][0][7]

        if predicted_price == "":
            predicted_price = "Some error occured"
            return_dict = {"predicted_price":predicted_price}
            return json.dumps(return_dict)
    except:
        return_dict = {"predicted_price":"Some error occured"}
        return json.dumps(return_dict)

@app.route('/classification/getClassification', methods=['POST'])
def get_classification():
    try:
        apikeys=loadApiKeys('classification')
        if apikeys == None:
            print("Api Keys file has some issue")
            classified_as="Some Error occured with api keys file"
            scored_probability = ""
            return_dict = {"classified_as":classified_as,"scored_probability":scored_probability}
            return json.dumps(return_dict)
        else:
            host_response_rate=request.json['host_response_rate']
            city=request.json['city']
            room_type=request.json['room_type']
            accommodates=request.json['accommodates']
            bathrooms=request.json['bathrooms']
            price=request.json['price']
            cancellation_policy=request.json['cancellation_policy']
            security_deposit=request.json['security_deposit']
            cleaning_fee=request.json['cleaning_fee']
            instant_bookable=request.json['instant_bookable']
            TV=request.json['TV']
            beds=request.json['beds']
            algoType = request.json['algoType']
        #print(curr_act_upb+"\t"+loan_age+"\t"+months_to_legal_maturity+"\t"+curr_interest_rate+"\t"+curr_deferred_upb)
        #make ai call
        if algoType=="pred_df":
            url=apikeys['decisionjungle']['url']
            api_key=apikeys['decisionjungle']['apikey']
        elif algoType=="pred_nn":
            url=apikeys['bayestwopoint']['url']
            api_key=apikeys['bayestwopoint']['apikey']
        elif algoType=="pred_lr":
            url=apikeys['logisticregression']['url']

        data =  {

            "Inputs": {

                "input1":
                    {
                        "ColumnNames": ["host_response_rate", "city", "room_type", "accommodates", "bathrooms","beds","price","cancellation_policy","security_deposit","cleaning_fee","instant_bookable","TV"],
                        "Values": [[host_response_rate, city, room_type, accommodates, bathrooms,beds,price,cancellation_policy,security_deposit,cleaning_fee,instant_bookabl,TV]]
                    },        },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        #url = 'https://ussouthcentral.services.azureml.net/workspaces/5de0e8bd28f74cf9a40babb3f1799a53/services/300d6267d2f843c9a5975621ff077a09/execute?api-version=2.0&details=true'
        #api_key = 'wQWgTpa3GyVACzg7Q6jVDdwt5JEDnfdvqqG21PKDr+UHmZWRQJh1XfrtLVON846vEDEXoDgnruZ1s9zd4Drzyw==' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        response = requests.post(url, data=body,headers=headers)
        #print(response.content)

        response_json=json.loads(response.content)
        if response_json['Results']['output1']['value']['Values'][0][5] == "0":
            scored_probability=response_json['Results']['output1']['value']['Values'][0][6]
            classified_as="Negative"
        elif response_json['Results']['output1']['value']['Values'][0][5] == "1":
            scored_probability=response_json['Results']['output1']['value']['Values'][0][6]
            classified_as="Neutral"
        elif response_json['Results']['output1']['value']['Values'][0][5] == "2":
            scored_probability=response_json['Results']['output1']['value']['Values'][0][6]
            classified_as="Positive"
        else:
            classified_as="Some Error occured in Classification"
            scored_probability = ""
            return_dict = {"classified_as":classified_as,"scored_probability":scored_probability}
            return json.dumps(return_dict)
    except:
        return_dict = {"classified_as":"Some Error occured."}
        return json.dumps(return_dict)

#@app.route('/api/visitors', methods=['POST'])
# def put_visitor():
#     user = request.json['name']
#     if client:
#         data = {'name':user}
#         db.create_document(data)
#         return 'Hello %s! I added you to the database.' % user
#     else:
#         print('No database')
#         return 'Hello %s!' % user
#
# @atexit.register
# def shutdown():
#     if client:
#         client.disconnect()

if __name__ == '__main__':
    app.run(debug=True)
