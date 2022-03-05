import boto3
import json
import requests
import yaml
# from requests_aws4auth import AWS4Auth

region = 'us-east-1' # For example, us-west-1
service = 'es'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
auth = ('vishnudut','VvishnuDut1!')


host = 'https://search-restaurantdb-2kcj6kxfssnod2fzfpep2qub3e.us-east-1.es.amazonaws.com' # The OpenSearch domain endpoint with https://
index = 'restaurants_index'
url = host + '/' + index 
type_url = host + '/' + index + '/' + 'restaurant_type' + '/' + '_mappings'
post_url = host + '/' + index + '/' + '_doc'
headers = { "Content-Type": "application/json" }
ob = {
    "restaurant_type":{
            "properties":{
                "restaurant_id":{
                    "type":"text"
                },
                "cuisine":{
                    "type":"text"
                }
            }
        }
}
params = {
    "include_type_name":"true"
}
def create_type():
    return requests.put(type_url,auth=auth,data = json.dumps(ob),headers=headers, params=params)

# r = create_type()
# print(r.json())

def create_index():
    return requests.put(url,auth=auth)

# response = create_index()
# print(response.json())]

files = ['American','Indian','Italian','Japanese','Korean']
for file in files:
    data = yaml.safe_load(open(file+'.json'))
    c = 0
    for record in data: 
        document = {
            "restaurent_id":record['id'],
            "cuisine":file,
        }
        response = requests.post(post_url,auth=auth, headers=headers, data=json.dumps(document))
        c+=1
        # print(c)
        # print(response.json())


# Lambda execution starts here
def lambda_handler(event, context):
    pass
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    # query = {
    #     "size": 25,
    #     "query": {
    #         "multi_match": {
    #             "query": event['queryStringParameters']['q'],
    #             "fields": []
    #         }
    #     }
    # }

    # # Elasticsearch 6.x requires an explicit Content-Type header
    # headers = { "Content-Type": "application/json" }

    # # Make the signed HTTP request
    # r = requests.get(url, auth=auth, headers=headers, data=json.dumps(query))

    # # Create the response and add some extra content to support CORS
    # response = {
    #     "statusCode": 200,
    #     "headers": {
    #         "Access-Control-Allow-Origin": '*'
    #     },
    #     "isBase64Encoded": False
    # }

    # # Add the search results to the response
    # response['body'] = r.text
    # return response






















# from opensearchpy import OpenSearch, RequestsHttpConnection
# from requests_aws4auth import AWS4Auth
# import boto3
# import yaml

# host = 'search-restaurant-fotaselssdzhh53n5vxlqz6hga.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
# region = 'us-east-1' # e.g. us-west-1

# service = 'es'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# search = OpenSearch(
#     hosts = [{'host': host, 'port': 443}],
#     http_auth = awsauth,
#     use_ssl = True,
#     verify_certs = True,
#     connection_class = RequestsHttpConnection
# )

# index_name = 'restaurant_index'
# def create_index():
#     index_body ={
#         'settings':{
#             'index':{

#             }
#         }
#     }
#     response = search.indices.create(index_name,body=index_body)
#     print('n\Createing index')
#     print(response)

# files = ['American','Indian','Italian','Japanese','Korean']
# id = 1
# for file in files:
#     data = yaml.safe_load(open(file+'.json'))
#     for record in data: 
#         document = {
#             "restaurent_id":record['id'],
#             "cuisine":file,
#         }
#         response = search.index(
#             index = index_name,
#             body = document, 
#             id = id,
#             refresh=True,
#         )
#         id+=1
#         print(response)