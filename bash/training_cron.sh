#!/bin/bash
# Cronjob script to update training models with new available data.
# Author: Luis A Garnica
# dependencies: curl and jq for linux bash

# authentication
username=$RECOMMADMIN
password=$RECOMMADMINKEY

# training options
implicit="true"
explicit="true"
content="false"

# endpoints
auth_endpoint="https://myrecommender.com/swim-recommender/auth" # change this to swim-api auth
training_endpoint="https://myrecommender.com/swim-recommender/recommender/train/" # change this to train endpoint
models_endpoint="https://myrecommender.com/swim-recommender/recommender/db/model/" # change this to models endpoint

# get authentication token
echo 'Obtaining authorization token...'
auth_response=$(curl -X POST -H 'Content-Type: application/json' -i 'https://myrecommender.com/swim-recommender/auth' --data '{
"username" : "'$username'",
"password" : "'$password'"
}');

# parse response for token value
echo 'Extracting token value'
auth_response=${auth_response:100}
token=$(echo $auth_response | jq  -r '.access_token')

# get available models and check if trained
echo 'Getting list of trained models'
models_response=$(curl -X GET $models_endpoint -H  "accept: application/json" -H  "Authorization: Bearer "$token"" -H  "Content-Type: application/json" -k);
model_list=$(echo $models_response | jq  -r '.data')

# extract model ids and assign to array
model_ids=$(echo $model_list | jq -r '.[].id')
array=($model_ids)

# train models from current saved point (foreach)
# TODO: update for new parameters
for i in "${array[@]}"
do
	echo 'Updating Training...'
	echo $i
	train_response=$(curl -X POST $training_endpoint -H  "accept: application/json" -H  "Authorization: Bearer "$token"" -H  "Content-Type: application/json" -d "{  \"model_id\": \""$i"\",  \"epochs\": 5200,  \"new\": false,  \"implicit\": "$implicit",  \"explicit\": "$explicit",  \"content\": "$content"}" -k);

	# log result status
	echo 'Logging result status'
	status=$(echo $train_response | jq  -r '.status')
	printf '%s %s %s\n' "$status" "$(date)" "$line" >> trainlog.txt
done


echo 'Finished!'
