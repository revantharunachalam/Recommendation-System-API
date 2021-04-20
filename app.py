import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

def create_similarity():
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

def get_response(movie):
	return {
	'Movie name': movie,
	'Director': list(data[data['movie_title'] == movie]['director_name'])[0], 
	'Genere': list(data[data['movie_title'] == movie]['genres'])[0], 
	'Actors': [list(data[data['movie_title'] == movie]['actor_1_name'])[0], list(data[data['movie_title'] == movie]['actor_2_name'])[0], list(data[data['movie_title'] == movie]['actor_3_name'])[0]]
	}

data = pd.read_csv('processed_data.csv')
app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
	return render_template('index.html')

@app.route("/recommend", methods=['GET'])
def recommend():
	input_movie = request.args.get('name')
	rec_movie = rcmd(input_movie)
	response = {'Requested Movie': get_response(input_movie), 
				'Recommendations': []
				}
	for movie in rec_movie:
		response['Recommendations'].append(get_response(movie)) 

	return jsonify(response)


if __name__ == "__main__":
	app.run(debug=True)
