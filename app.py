import flask
import requests
import random

app = flask.Flask(__name__)

# Comments for dogs and cats
dog_comments = [
    "Look at this adorable dog! 🐕💖",
    "Who’s a good boy? 😍🐾",
    "Such a fluffy friend! 🐶✨",
    "Can you handle this cuteness? 🥰🐾",
    "Big puppy eyes incoming! 🐕👀",
    "This doggo just made my day! 🌟🐶",
    "Too cute to handle! 😭🐾",
    "Smiles all around with this pup! 😄🐕",
    "Look at that shiny coat! ✨🐶",
    "I need this dog in my life! 🐾❤️"
]

cat_comments = [
    "Look at this adorable cat! 🐱💖",
    "Meow-some cuteness alert! 😺✨",
    "Purr-fect little friend! 🐾😻",
    "Can you handle this fluff? 😻💫",
    "Cuteness overload! 🐱💛",
    "Those eyes though! 😺👀",
    "This kitty just stole my heart! ❤️🐾",
    "Paws-itively adorable! 🐾😻",
    "So soft, so cute! 🐱✨",
    "Cat nap vibes only 😸💤"
]

def getRandomComment(animal_type="dog"):
    return random.choice(dog_comments if animal_type == "dog" else cat_comments)

# API configuration
baseUrlDog = "https://api.thedogapi.com/v1"
baseUrlCat = "https://api.thecatapi.com/v1"
API_KEY = "live_gu43vtrWpxPT9jK2a3OYTtmvKZgiVe0bnGVGwyk24z9il5MZKdXHnDROmFgB33NC"
headers = {"x-api-key": API_KEY}

# Helper to safely fetch data from API
def fetch_data(url):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            print(f"API error: {response.status_code} - {response.text}")
            return None
        data = response.json()
        if not data:
            print("Empty JSON response")
            return None
        return data[0]
    except (requests.RequestException, ValueError) as e:
        print(f"Exception fetching data: {e}")
        return None

def getRandomDogData():
    url = f"{baseUrlDog}/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"
    return fetch_data(url)

def getRandomCatData():
    url = f"{baseUrlCat}/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"
    return fetch_data(url)

# Routes
@app.route('/')
def index():
    return flask.render_template("home.html")

@app.route('/dog')
def dog():
    dogData = getRandomDogData()
    if not dogData:
        return flask.render_template("error.html", message="Failed to fetch dog data. Please try again later.")

    imageUrl = dogData.get("url", "")
    dogBreeds = dogData.get("breeds", [])
    breed = dogBreeds[0] if dogBreeds else {}

    return flask.render_template(
        "dog.html",
        img=imageUrl,
        breed=breed.get("name", "Unknown"),
        breedGroup=breed.get("breed_group", "Unknown"),
        temperament=breed.get("temperament", "Unknown"),
        life_span=breed.get("life_span", "Unknown"),
        weight_imperial=breed.get("weight", {}).get("imperial", "N/A"),
        height_imperial=breed.get("height", {}).get("imperial", "N/A"),
        comment=getRandomComment("dog")
    )

@app.route('/cat')
def cat():
    catData = getRandomCatData()
    if not catData:
        return flask.render_template("error.html", message="Failed to fetch cat data. Please try again later.")

    imageUrl = catData.get("url", "")
    catBreeds = catData.get("breeds", [])
    breed = catBreeds[0] if catBreeds else {}

    return flask.render_template(
        "cat.html",
        img=imageUrl,
        breed=breed.get("name", "Unknown"),
        breedGroup=breed.get("breed_group", "Unknown"),
        temperament=breed.get("temperament", "Unknown"),
        life_span=breed.get("life_span", "Unknown"),
        weight_imperial=breed.get("weight", {}).get("imperial", "N/A"),
        height_imperial=breed.get("height", {}).get("imperial", "N/A"),
        comment=getRandomComment("cat")
    )

@app.route('/<path>')
def default(path):
    return flask.render_template("home.html")

if __name__ == "__main__":
    app.run()
