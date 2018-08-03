# Mastermind Server

This reposiroty contains a Flask application (in Python3) that will setup a game 
of Mastermind. The aim of the game is to guess the correct colour and position 
of four pegs that the server has randomly selected. 

The colours being used Red, Green, Blue, Yellow, Magenta, and Cyan (represented 
by the first letter of the colours name in uppercase). 

## Protocol

We're using HTTP to interact with the API. POST to /game/ and you'll get a 
unique game instance. PUT your guesses to /game/<id>/ in a variable 
called 'guess' and you'll get a response back from the server containing the 
number of exact colours, the number of near guesses, and whether the game 
has been solved (as a boolean).

## Example

```
-> POST /game/ HTTP/1.1
-> Host: fierce-forest-59715.herokuapp.com
-> 
<- HTTP/1.1 201 CREATED
<- Connection: keep-alive
<- Server: gunicorn/19.9.0
<- Date: Fri, 03 Aug 2018 04:36:36 GMT
<- Content-Type: text/plain; charset=utf-8
<- Content-Length: 5
<- Via: 1.1 vegur
<- 
<- ELEY
Created Game ELEY
guess YYYY
-> PUT /game/ELEY/ HTTP/1.1
-> Host: fierce-forest-59715.herokuapp.com
-> Content-Type: application/x-www-form-urlencoded
-> Content-Length: 10
-> 
-> guess=YYYY
<- HTTP/1.1 201 CREATED
<- Connection: keep-alive
<- Server: gunicorn/19.9.0
<- Date: Fri, 03 Aug 2018 04:36:43 GMT
<- Content-Type: text/plain; charset=utf-8
<- Content-Length: 30
<- Via: 1.1 vegur
<- 
<- exact: 2	near: 2	solved: False
exact: 2	near: 2	solved: False
```
