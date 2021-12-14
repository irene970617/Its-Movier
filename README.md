# It's Movier
This is a Flask application related to movies. It includes some games and movie recommendations. 
This documentation will show you the instructions for running the code with data structure and getting start with the application. 

## Packages
  If user wants to run the api to get the data, user needs to register https://www.themoviedb.org/ and get your personal api        
  To fetch data from API, user needs to "import requests" .        
  This is a flask app, so user needs to install Flask in order to use the application. 
 
## How to run the code
 1. First download the folder to your computer 
 2. Get in the terminal and open the folder
 3. Type "python3 app.py" to run the server
 4. Open this link:  http://127.0.0.1:5000/
 
## Page Introductions
 1. Kevin Bacon Game     
 The object of the game is to start with any actor who has been in a movie and connect them to Kevin Bacon in the smallest number of links possible.
 Two people are linked if they've been in a movie together.For instance, if Mary Pickford is the targeted actor. Louise Beavers has been in the Coquette with her, 
 then Louise Beavers is in the first degree.    
 I created a graph to link every movie and every actor who played in that movie.    
 I used BFS to search the link between two actors. In this program, I did not search the whole graph. In other words, the program stops and displays the result
 when it reaches the the goal.

 2. Score     
 In this page, user can enter an actor's name and the program will use BFS and run through the graph to search for all degrees. 
 It will show user how many actors in each degree and calculate the popular score. The lower the score, the more centered the actor is. 
 And it also shows the number of movies the actor has starred in. 
 
 3. Recommendation    
 User can enter the genres, years, and actors name to get the recommendation of movies. It is sorted from high voted to low voted. And it will show maximum 20 movies. 
 
 4. Contact     
 If user has any recommendation, please send message from contact page.
