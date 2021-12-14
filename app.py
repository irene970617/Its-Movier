import json
from flask import Flask, render_template, request
app = Flask(__name__)

with open('data/movie5000.json') as f:
    mv = json.load(f)
with open('data/movie50000.json') as f:
    mv2 = json.load(f)

actors_movies = {}
movies_actors = {}
movies = {}
genres = {}
year = {}


def preprocess(data, actors_movies, movies_actors):
    for k, v in data.items():
        if k not in actors_movies.keys():
            actors_movies[k] = []
        for item in v:
            # actors_movies
            if item['title'] not in actors_movies[k]:
                actors_movies[k].append(item['title'])

            # movies_actors
            if item['title'] not in movies_actors.keys():
                movies_actors[item['title']] = [k]
            elif item['title'] in movies_actors[item['title']]:
                continue
            else:
                movies_actors[item['title']].append(k)

            # genres
            for genre in item['genres']:
                if genre not in genres.keys():
                    genres[genre] = [item['title']]
                else:
                    genres[genre].append(item['title'])
            # year
            if item['release_date'][:4] not in year.keys():
                year[item['release_date'][:4]] = [item['title']]
            else:
                year[item['release_date'][:4]].append(item['title'])
            # movies
            if item['title'] not in movies.keys():
                movies[item['title']] = {'vote_count': item['vote_count'], 'vote_avg': item['vote_avg'],
                                         'release_date': item['release_date'], 'poster_path': item['poster_path'],
                                         'genres': item['genres'], 'characters': [k]}
            else:
                if k not in movies[item['title']]['characters']:
                    movies[item['title']]['characters'].append(k)


preprocess(mv, actors_movies, movies_actors)
preprocess(mv2, actors_movies, movies_actors)
del year['2030']
del year['2028']
del year['2026']
del year['2024']
del year['2023']
del year['2022']

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}  # empty dictionary

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getId(self):
        return self.id

    def getConnection(self):
        return self.connectedTo.keys()


class Graph:
    def __init__(self):
        self.verList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.verList[key] = newVertex
        return newVertex

    def addEdge(self, f, t, weight=0):
        if f not in self.verList:
            nv = self.addVertex(f)
        if t not in self.verList:
            nv = self.addVertex(t)
        self.verList[f].addNeighbor(self.verList[t], weight)


def Backtrace(dic, start, end):
    res = [end]
    while 1:
        if start == end:
            break
        for k, v in dic.items():
            for i in v:
                if i == end:
                    res.append(k)
                    end = k
                    break
    return res


graph = Graph()
for actor in actors_movies.keys():
    graph.addVertex("A-"+actor)
for movie in movies_actors.keys():
    graph.addVertex("M-"+movie)

for k, v in movies_actors.items():
    for item in v:
        graph.addEdge("M-"+k, "A-"+item, 1)
        graph.addEdge("A-"+item,"M-"+k,1)




@app.route('/')
def KBGame():
    return render_template('game.jinja')


@app.route('/game/result', methods=['POST'])
def KBGame_result():
    backtrace={}
    def BFS(s, goal):
        s="A-"+s
        goal = "A-"+goal
        start = s
        visited = {}
        for key in graph.verList.keys():
            visited[key] = False
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            s = queue.pop(0)
            for i in graph.verList[s].getConnection():
                if visited[i.getId()] == False:
                    if s not in backtrace.keys():
                        backtrace[s] = [i.getId()]
                    else:
                        backtrace[s].append(i.getId())
                    queue.append(i.getId())
                    visited[i.getId()] = True
                if i == graph.verList[goal]:
                    return Backtrace(backtrace, start, goal)
    actor1 = request.form['actor1']
    actor2 = request.form['actor2']
    noactor1 = ""
    noactor2 =""
    if "A-"+actor1 not in graph.verList:
        noactor1 = 'There is no result for ' + actor1
    if "A-"+actor2 not in graph.verList:
        noactor2 = 'There is no result for ' + actor2
    if len(noactor1)!=0 or len(noactor2)!=0:
        return render_template('game-result.jinja', noactor1=noactor1, noactor2=noactor2)

    result = BFS(actor2, actor1)

    return render_template('game-result.jinja', actor1=actor1, actor2=actor2, result=result)


@app.route('/popular')
def popular():
    return render_template('popular.jinja',)


@app.route('/popular/result', methods=['POST'])
def popular_res():
    def BFS_all(s):
        s="A-"+s
        if s not in graph.verList.keys():
            return []
        visited = {}
        for key in graph.verList.keys():
            visited[key] = False
        queue = []

        queue.append(s)
        visited[s] = True
        
        result={}
        inner = []
        count = 0.5
        while queue:
            s = queue.pop(0)

    
            for i in graph.verList[s].getConnection():

                if visited[i.getId()] == False:
                    
                    inner.append(i.getId())
                    visited[i.getId()] = True
                    
        
            if len(queue) == 0:
                result[count]=inner
                count+=0.5
                queue+=inner
                inner = []
            if count == 7.5:
                break
        return result

    actor = request.form['actor']
    all_degree = BFS_all(actor)
    star = len(actors_movies[actor])
    if len(all_degree)==0:
        r = "No Search. Please enter again."
        return render_template('popular-result.jinja', nosearch=r, star=star)
    score = []
    for i in range(1, 8):
        try:
            if all_degree[i]:
                score.append(len(all_degree[i]))
        except:
            score.append(0)

    if len(score)==5:
        score.append(0)
    if len(score)==6:
        score.append(0)

    popular_score = (1*score[0]+2*score[1]+3*score[2]+4*score[3]+5*score[4]+6*score[5] +
                     7*score[6])/(score[0]+score[1]+score[2]+score[3]+score[4]+score[5]+score[6])
    

    return render_template('popular-result.jinja', actor=actor, popular=round(popular_score,2), score=score, star=star)


@app.route('/recommend')
def recommend_page():
    all_genre = list(genres.keys())

    all_year = list(sorted(year.keys()))
    all_year.reverse()

    return render_template('recommend.jinja',all_genre=all_genre, all_year = all_year)


@app.route('/recommend/result', methods=['POST'])
def recommend_res():
    def Diff(li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    def listToString(s): 
        str1 = " " 
        separator = ', '
        return (separator.join(s))
    actor=request.form['actor']
    genre = request.form['genre']
    from_year = request.form['from_year']
    to_year = request.form['to_year']

    def recommend(genre, actor=None, from_year=None, to_year=None):
        movie = []
        delete = []
        if genre == 'Science':
            genre = 'Science Fiction'
        if genre == 'TV':
            genre=='TV Movie'
        movie = genres[genre]
        for m in movie:
            if actor:
                if actor not in movies_actors[m]:
                    delete.append(m)
            if from_year:
                if movies[m]['release_date'][:4] < from_year:
                    delete.append(m)
            if to_year:
                if movies[m]['release_date'][:4] >to_year:
                    delete.append(m)
            if movies[m]['vote_count']<1000:
                delete.append(m)
        result = Diff(movie, delete)
        sorting = {}
        for res in result:
            sorting[res] = movies[res]['vote_avg']
        sorting = dict(sorted(sorting.items(), key=lambda item: item[1], reverse=True))
        top20 = {}
        count=1
        for item in list(sorting.keys()):
            if item not in top20.keys():
                top20[item]=movies[item]
        
            count+=1
            if count==20:break
        
        return top20

    
    result= recommend(genre, actor=actor,from_year=from_year, to_year=to_year)
    
    title=[]
    for k in result.keys():
        title.append(k)
    vote_count = []
    vote_avg =[]
    year_list = []
    photo=[]
    genres_list=[]
    for item in result.values():
        vote_count.append(item['vote_count'])
        vote_avg.append(item['vote_avg'])
        year_list.append(item['release_date'][:4])
        photo.append(item['poster_path'])
        genres_list.append(item['genres'])
    r = []
    for i in range(len(title)):
        r.append([title[i],year_list[i],vote_count[i],vote_avg[i],genres_list[i],\
          'https://image.tmdb.org/t/p/w500/'+photo[i]]) 
    if len(r) == 0:
        r = "No Search. Please enter again."
        return render_template('recommend-result.jinja', nosearch = r)
        
    return render_template('recommend-result.jinja', result = r)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
