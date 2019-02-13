# import appropriate modules

# bottle is the module which will manage our API routes/requests
from bottle import route, run, static_file

# requests handles external API calls
import requests

# mysql connector allows us to connect to a mysql database
import mysql.connector

# allows us to utilize our config file
import json

# load our config json file into a python dictionary
config = json.loads(open('config.json').read())

# establish mysql connection
db = mysql.connector.connect(
    host=config['mysqlHost'],
    user=config['mysqlUser'],
    passwd=config['mysqlPassword'],
    database=config['mysqlDatabase']
)

print('Connection established')

# the cursor is used to query the database
cursor = db.cursor()

# bottle routes follow this syntax:
# @route is a decorator, saying the following function should be called
# when we make a request to the specified string.
# this route matches the index request (i.e. www.google.com/)
@route('/')
def index():
    # serve a static file, which is hosted in the subdirectory public
    return static_file('index.html', root='public')

# you can add a parameter to the path with <PARAM>
# so this route will match yourUrl/exampleRoute, yourUrl/anotherRoute
# but it will not match with yourUrl/exampleIsBad/becauseHasTwoParams
# note the name of the parameter is then passed into the handler function
# this route sends our linked js/css files to the client
@route('/<filename>')
def static(filename):
    return static_file(filename, root='public')

# route to match requests to get an existing or create a new blackjack game
@route('/game/<gameName>/getOrCreate')
def getOrCreate(gameName):
    # create our sql query, using %s for query parameters
    qString = "SELECT gameName, deckId, gamesWon, gamesLost FROM games WHERE gameName = %s"
    
    # values is our parameter tuple. we use a comma to force values to be a tuple even though we only have one parameter
    values = (gameName, )
    
    # execute the query with parameters
    cursor.execute(qString, values)

    # capture the result of the query
    result = cursor.fetchall()
    
    # no items in result means we need to make a new game in the API and new mysql entry
    if len(result) == 0:
        # make an API call to request a new deck
        res = requests.get('{}/new/shuffle/?deck_count=1'.format(config['apiEndpoint']))
        # convert the request body to a python dictionary
        data = res.json()

        qString = 'INSERT INTO games (gameName, deckId) VALUES (%s, %s)'
        values = (gameName, data['deck_id'])
        # insert the record of our new game series to the database
        cursor.execute(qString, values)

        # we must commit so that database insertions are carried out
        db.commit()
        
        # draw cards
        drawCardToHand(data['deck_id'], 'player')
        drawCardToHand(data['deck_id'], 'dealer')
        drawCardToHand(data['deck_id'], 'player')
        drawCardToHand(data['deck_id'], 'dealer')

        # figure out who has which cards
        playerPileData = getPileData(data['deck_id'], 'player')
        dealerPileData = getPileData(data['deck_id'], 'dealer')

        # return game configuration to the client
        # note scores are empty since they are computed by the client
        return {
            "gameName": gameName,
            "deckId": data['deck_id'],
            "gamesWon": 0,
            "gamesLost": 0,
            "dealerPile": dealerPileData,
            "playerPile": playerPileData,
            "scores": {}
        }
    else:
        # game already exists in the database, so load it
        # note that fetchall returns a list of tuples, so we must use numeric access
        deck_id = result[0][1]

        playerPileData = getPileData(deck_id, 'player')
        dealerPileData = getPileData(deck_id, 'dealer')
        
        return {
            "gameName": gameName,
            "deckId": deck_id,
            "gamesWon": result[0][2],
            "gamesLost": result[0][3],
            "dealerPile": dealerPileData,
            "playerPile": playerPileData,
            "scores": {}
        }

# respond to request to draw a card
@route('/game/<deckId>/draw/<player>')
def draw(deckId, player):
    # draw the card
    drawCardToHand(deckId, player)
    # return the appropriate player pile
    return getPileData(deckId, player)

# respond to the end of a game
@route('/game/<gameName>/endGame/<winner>')
def endGame(gameName, winner):
    # get new deck
    res = requests.get('{}/new/shuffle/?deck_count=1'.format(config['apiEndpoint']))
    data = res.json()

    # generate query so that appropriate database cells are updated
    qString = ''
    if winner == 'player':
        qString = 'UPDATE games SET deckId = %s, gamesWon = gamesWon + 1 WHERE gameName = %s'
    else:
        qString = 'UPDATE games SET deckId = %s, gamesLost = gamesLost + 1 WHERE gameName = %s'
    values = (data['deck_id'], gameName)
    cursor.execute(qString, values)
    db.commit()

    drawCardToHand(data['deck_id'], 'player')
    drawCardToHand(data['deck_id'], 'dealer')
    drawCardToHand(data['deck_id'], 'player')
    drawCardToHand(data['deck_id'], 'dealer')

    playerPileData = getPileData(data['deck_id'], 'player')
    dealerPileData = getPileData(data['deck_id'], 'dealer')

    # get updated game data from DB
    qString = 'SELECT gameName, deckId, gamesWon, gamesLost FROM games WHERE gameName = %s'
    values = (gameName, )
    cursor.execute(qString, values)

    # fetchone is like fetchall but returns a single tuple
    result = cursor.fetchone()

    return {
        "gameName": gameName,
        "deckId": data['deck_id'],
        "gamesWon": result[2],
        "gamesLost": result[3],
        "dealerPile": dealerPileData,
        "playerPile": playerPileData,
        "scores": {}
    }

# helper function to draw a card to the appropriate hand
def drawCardToHand(deckId, hand):
    # draw card from deck
    res = requests.get('{}/{}/draw/?count=1'.format(config['apiEndpoint'],deckId))
    data = res.json()
    # move card to appropriate pile (hand)
    requests.get('{}/{}/pile/{}/add/?cards={}'.format(config['apiEndpoint'],deckId, hand, data['cards'][0]['code']))
    return

# helper function to get specified hand data
def getPileData(deckId, hand):
    res = requests.get('{}/{}/pile/{}/list'.format(config['apiEndpoint'], deckId, hand))
    data = res.json()
    return data['piles'][hand]

# run the bottle API server
run(host='localhost', port=config['PORT'])