# -*- coding: UTF-8 -*-
from flask import Flask
#from redis import Redis
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import os
import requests
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#redis = Redis(host='redis',port=6379)

now = datetime.datetime.now()
@app.route('/')
def hello():
	#redis.incr('counter')
	return 'TV programa %s/%s/%s.' % (now.year, now.month, now.day)

tv_db = [
	{
		'id' : 1,
		'television' : 'LRT TELEVIZIJA',
		'type' : 'Vaidybinis serialas',
		'title' : 'Seserys',
		'start_time' : '05:00',
		'description' : '',
		'release_year' : '2016',
		'legal_age' : 'N-7',
		'football_teams' : [
			{'id' : 1},
			{'id' : 2}
		]
	},
	{
		'id' : 2,
		'television': 'LRT TELEVIZIJA',
		'type' : 'Žinios',
		'title' : 'Žinios',
		'start_time' : '06:30',
		'description' : '',
		'release_year' : '',
		'legal_age' : '',
		'football_teams' : [
			{'id' : 5},
			{'id' : 6}
		]
	},
	{
		'id' : 3,
		'television': 'LNK',
		'type' : 'Animacinis serialas',
		'title' : "Tomas ir Džeris",
		'start_time' : '15:30',
		'description' : '',
		'release_year' : '1980',
		'legal_age' : '',
		'football_teams' : []

	},
        {
                'id' : 4,
                'television': 'TV3',
                'type' : 'Kriminalinė drama',
                'title' : 'Specialioji jūrų policijos tarnyba',
                'start_time' : '01:20',
                'description' : '',
                'release_year' : '2011',
                'legal_age' : 'N-7',
		'football_teams' : []

        },
        {
                'id' : 5,
                'television': 'Viasat Sport Baltic',
                'type' : 'Krepšinio rungtynės',
                'title' : 'Baskonia-Žalgiris',
                'start_time' : '21:30',
                'description' : 'Eurolygos rungtynės',
                'release_year' : '',
                'legal_age' : '',
		'football_teams' : []

        },
        {
                'id' : 6,
                'television': 'BTV',
                'type' : 'Kriminalinė drama',
                'title' : 'Sunkūs laikai',
                'start_time' : '21:00',
                'description' : 'Vaidina Charles Bronson, James Cpburn',
                'release_year' : '1975',
                'legal_age' : '',
		'football_teams' : []

        }
]
#404 and 400 error handling
@app.errorhandler(404)
def not_found(error):
    	return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

#GET
#curl -i http://localhost:80/tv_program
@app.route('/tv_programs', methods=['GET'])
def programs():
    tv_programs = []
    television = request.args.get('television')
    embed = request.args.get('embedded','')
    if embed == 'football_teams':
        tv_programs = copy.deepcopy(tv_db)
        for i in range(0,len(tv_programs)):
            if len(tv_programs[i]["football_teams"])!=0:
                for j in range(0,len(tv_programs[i]["football_teams"])):
                    try:
                        identif = tv_programs[i]["football_teams"][j]['id']
                        url = 'http://web2:81/football_teams/'+str(identif) 		
                        r = requests.get(url).text
                        r = json.loads(r)
                        tv_programs[i]["football_teams"][j]=r
                    except requests.exceptions.RequestException as err:
                        print(err)
			r = "null"
			r = json.loads(r)
                        tv_programs[i]["football_teams"][j] = r
	return jsonify(tv_programs)
    if television is None and embed is None:
        return jsonify(tv_db)
    if television is not None:
        for i in tv_db:
            if television in i['television']:
                tv_programs.append(i)
        return jsonify(tv_programs)
    else:
        return jsonify(tv_db)

#GET/<OPTION>
#curl -i http://localhost:80/tv_programs/<id>
@app.route('/tv_programs/<int:id>', methods=['GET'])
def tv_program_by_id(id):
	program = {}
	for i in tv_db:
		if i['id'] == id:
			program = i
	if len(program) == 0:
		abort(404)
	embed = request.args.get('embedded','')
	if embed == 'football_teams':
            program2 = copy.deepcopy(program)
            if len(program2["football_teams"])!=0:
                for j in range(0,len(program2["football_teams"])):
                    try:
                        identif = program2["football_teams"][j]['id']
                        url = 'http://web2:81/football_teams/'+str(identif) 		
                        r = requests.get(url).text
                        r = json.loads(r)
                        r = r[0]
                        program2["football_teams"][j]=r
                    except requests.exceptions.RequestException as err:
                        print(err)
			r = "null"
			r = json.loads(r)
                        program2["football_teams"][j] = r
                       # return str(err), 503
	    return jsonify(program2)
	return jsonify(program)

#POST
#curl -i -H "Content-Type: application/json" - X POST -d '{"title":"<>", "television":"<>","start_time":"<>", etc <optional>}' https://localhost:80/tv_programs 

@app.route('/tv_programs', methods=['POST'])
def new_program2():
    if not request.json or not 'title' in request.json  or not 'television' in request.json or not 'start_time' in request.json:
       abort(400)
    id = tv_db[-1]['id'] + 1
    program = {
        'id': id,
	'television': request.json['television'],
	'type': request.json.get('type',""),
	'title': request.json['title'],
        'description': request.json.get('description', ""),
	'release_year': request.json.get('release_year', ""),
	'legal_age': request.json.get('legal_age', ""),
	'start_time': request.json['start_time'],
	'football_teams': []
	}
    tv_db.append(program)
    if request.json["football_teams"]:
        for i in range(0,len(request.json["football_teams"])):
            if not 'Captain' in request.json["football_teams"][i] or not 'Name' in request.json["football_teams"][i] or not 'Stadium' in request.json["football_teams"][i] or not 'Attendance' in request.json["football_teams"][i] or not 'Country' in request.json["football_teams"][i]:
				abort(400)
    	    name = request.json["football_teams"][i]['Name']
    	    country = request.json["football_teams"][i]['Country']
    	    stadium = request.json["football_teams"][i]['Stadium']
    	    attendance = request.json["football_teams"][i]['Attendance']
    	    captain = request.json["football_teams"][i]['Captain']
    	    url = 'http://web2:81/football_teams'
    	    new_football_team = {
	       'Name': name,
	       'Country': country,
	       'Stadium': stadium,
	       'Attendance': attendance,
	       'Captain': captain,
	    }
            try:
    	        r = requests.post(url, json=new_football_team)
    	        r = json.loads(r.text)
            except requests.exceptions.RequestException as err:
                print(err)
                return str(err), 503
    	    for i in tv_db:
                if i['id'] == id:
                    i['football_teams'].append({'id':r['ID']})
    response = jsonify({'CREATED':'true'})
    response.status_code = 201
    response.headers['location'] = '/tv_programs/%s' %id
    return response

#PUT
#curl -i -H "Content-Type: application/json" - X PUT -d '{"<>":"<>"}' https://localhost:80/tv_programs/<program_id>
@app.route('/tv_programs/<int:id>', methods=['PUT'])
def update_program(id):
	program = []
	for i in tv_db:
        	if i['id'] == id:
                        program = i
	if len(program) == 0:
		abort(404)
	if not request.json:
		abort(400)
	program['title'] = request.json.get('title', program['title'])
	program['description'] = request.json.get('description', program['description'])
	program['television'] = request.json.get('television', program['television'])
	program['type'] = request.json.get('type', program['type'])
	program['start_time'] = request.json.get('start_time', program['start_time'])
	program['release_year'] = request.json.get('release_year', program['release_year'])
	program['legal_age'] = request.json.get('legal_age', program['legal_age'])
	if len(program['football_teams']) != 0:
            for i in range(0,len(request.json["football_teams"])):
                if not 'Captain' in request.json["football_teams"][i] or not 'Name' in request.json["football_teams"][i] or not 'Stadium' in request.json["football_teams"][i] or not 'Attendance' in request.json["football_teams"][i] or not 'Country' in request.json["football_teams"][i]:
		    abort(400)
                try:
    	            name = request.json["football_teams"][i]['Name']
    	            country = request.json["football_teams"][i]['Country']
    	            stadium = request.json["football_teams"][i]['Stadium']
    	            attendance = request.json["football_teams"][i]['Attendance']
    	            captain = request.json["football_teams"][i]['Captain']
    	            url = 'http://web2:81/football_teams/'+str(program['football_teams'][i]['id'])
    	            new_football_team = {
	                'Name': name,
	                'Country': country,
	                'Stadium': stadium,
	                'Attendance': attendance,
	                'Captain': captain,
	            }
    	            r = requests.put(url, json=new_football_team)
                except requests.exceptions.RequestException as err:
                    print(err)
                    return str(err), 503
	return jsonify({'UPDATED':'true'}), 200
#DELETE
#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:80/tv_program/<program_id>
@app.route('/tv_programs/<int:id>', methods=['DELETE'])
def delete_program(id):
    program = {}
    for i in tv_db:
       if i['id'] == id:
           program = i
    if len(program) == 0:
        abort(404)
    if len(program['football_teams']) != 0:
        for i in range(0, len(program['football_teams'])):
            try:
                url = 'http://web2:81/football_teams/'+str(program["football_teams"][i]["id"])
                r = requests.delete(url)
            except requests.exceptions.RequestException as err:
                print(err)
                return str(err), 503
    tv_db.remove(program)
    return jsonify(program)

@app.route('/football_teams', methods=['GET'])
def get_all_teams():
        try:
	    r = requests.get('http://web2:81/football_teams').text
	    r = json.loads(r)
            return jsonify(r), 200
        except requests.exceptions.RequestException as err:
            print(err)
            return str(err), 503

@app.route('/tv_programs/<int:id>/football_teams', methods=['GET'])
def get_football_team(id):
        program = []
        for i in tv_db:
                if i['id'] == id:
                        program = i
        if len(program) == 0:
                abort(404)
        try:
	    url = 'http://web2:81/football_teams'
	    r = requests.get(url).text
	    r = json.loads(r)
	except requests.exceptions.RequestException as err:
            print(err)
            return str(err), 503
	program_by_team = []
	for i in r:
		for j in program['football_teams']:
			if j['id'] == i['ID']:
				program_by_team.append(i)
	return jsonify(program_by_team)

@app.route('/tv_programs/<int:id>/football_teams/<int:f_id>', methods=['DELETE'])
def delete_football_team(id, f_id):
    url = 'http://web2:81/football_teams/'+str(f_id)
    r = requests.delete(url)
    team = []
    for i in tv_db:
        if i['id'] == id:
            i['football_teams'].remove({'id':f_id})
	    break
  #  if len(program) == 0:
   #         abort(404) id?? f_id+
    response = jsonify({'DELETED':'true'})
    response.status_code = 200
    return response


if __name__== "__main__":
	app.run(host="0.0.0.0",debug=True, port=5000)
