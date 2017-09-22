## HW 2 
## SI 364 F17
## Due: September 24, 2017
## 500 points

#####

## [PROBLEM 1]

## Edit the following Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number. Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import json
app = Flask(__name__)
app.debug = True

def processing():
	raw_data = requests.get("http://archiveofourown.org/media/")
	soup = BeautifulSoup(raw_data.text.encode("utf-8"), "html.parser")
	order_of_cat = soup.find_all("h3", class_ = "heading")[1:-1]
	headings = soup.find_all("ol", class_ = "index group")
	if len(order_of_cat) == len(headings):
		raw_info_dict = {}
		for position in range(len(order_of_cat)):
			raw_info_dict[order_of_cat[position].string] = headings[position].find_all("li")
		return(raw_info_dict)
	else:
		return "There has been an error in the retrieval, sorry :("

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route("/question", methods=["POST", "GET"])
def question_form():
	F = """<!DOCTYPE html>
	<html>
	<body>

	<form action="http://localhost:5000/result" method="GET">
  	Favorite Number:<br>
  	<input type="text" name="favoritenumber">
  	<br>
  	<input type="submit" value="Submit">
	</form> 

	</body>
	</html>"""
	return F

@app.route("/result", methods=["POST", "GET"])
def result_page():
	if request.method == "GET":
		args = request.args
		number = args.get("favoritenumber")
		doubled = int(number)*2
		return "Double your favorite number is {}.".format(str(doubled))

@app.route("/radioform", methods= ["POST", "GET"])
def radio():
	s= """<form action="http://localhost:5000/topfandoms" method="GET">
	<h1>Which category would you like to see the top fandoms in?</h1>
  	<input type="radio" name="category" value="Anime & Manga" checked>Anime and Manga<br>
  	<input type="radio" name="category" value="Cartoons & Comics & Graphic Novels">Cartoons, Comics, and Graphic Novels<br>
  	<input type="radio" name="category" value="Books & Literature">Books and Literature<br>
  	<input type="radio" name="category" value="Celebrities & Real People">Celebrities and Real People<br>
  	<input type="radio" name="category" value="Movies">Movies <br>
  	<input type="radio" name="category" value="Music & Bands">Music and Bands<br>
  	<input type="radio" name="category" value="Theater">Theatre<br>
  	<input type="radio" name="category" value="TV Shows">TV Shows<br>
  	<input type="submit" value="Submit">
	</form>"""
	return s
fandom_dict = processing()
@app.route("/topfandoms", methods = ["POST", "GET"])
def fandoms():
	if request.method == "GET":
		args = request.args
		fandom = args.get("category")
		try:
			raw_fandoms = fandom_dict[fandom]
		except:
			return "whoops, looks like your category couldn't be retrieved."
		cleaned_up = {}
		for result in raw_fandoms:
			cleaned_up[result.a.string]= result.get_text().split("\n")[2].strip()[1:-1]
		presentable_version = "Fandom Name - " + json.dumps(cleaned_up)[1:-1].replace(",", "<br>Fandom Name - ").replace(":", "&nbsp;&nbsp;| Number of Fics - ").replace('"', "")
		return presentable_version

if __name__ == '__main__':
    app.run()


## [PROBLEM 2]

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application. It should:
# - not be an exact repeat of something you did in class, but it can be similar
# - should include an HTML form (of any kind: text entry, radio button, checkbox... feel free to try out whatever you want)
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form (text entered, radio button selected, etc). So if a user has to enter a number, it should do an operation on that number. If a user has to select a radio button representing a song name, it should do a search for that song in an API.
# You should feel free to be creative and do something fun for you -- 
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)









