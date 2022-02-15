from flask import Flask, render_template, redirect, url_for
from redis import Redis, RedisError
import os
import socket
import logging
from probemaker import Hero
from flask import request

if "settings.py" in os.listdir():
    from settings import *
else:
    # fallback if no custom settings are provided
    from settings_template import *

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

logger = logging.getLogger("Basic Logger")

# Create Hero objects
hfiles = dict()  # Dict for heros' .json files
group = dict()  # Dict to collect all Hero objects
names = list()  # List to collect all names of heros in group

# Create total path to hero files
for hero in heros:
    hfiles[hero] = (data_folder / hero).resolve()
for h in hfiles:
    Digga = Hero(hfiles[h], logger, show_values)
    names.append(Digga.name)
    group[Digga.name] = Digga
    logger.info(f'{Digga.name} loaded')

heroes = group
possible_probes = []
for h in group.values():
    possible_probes += h.possible_probes
actions = list(set(possible_probes))
actions.sort()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        print("getting here...")
        print(request.form)
        hero = request.form['hero_name']
        talent = request.form['action_name']
        modifier = int(request.form['modifier'])
        hero_instance = group[hero]
        passed = hero_instance.perform_action(user_action=talent, modifier=modifier)
        rolls = hero_instance.rolls

        print(f"Hero {hero} performing probe on talent {talent}.")
        print(heroes)
        return render_template('index.html', hero=hero, talent=talent, passed=passed, heroes=heroes, actions=actions, rolls=rolls)
    #form = ActionEnteringForm()
    #if form.validate_on_submit():

        # Check the password and log the user in
        # [...]

    #return redirect(url_for('hello'))
    #print(request.form['hero_name'])
    return render_template('index.html', heroes=heroes, actions=actions)

@app.route("/hello")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"

    logging.basicConfig(filename='probe.log',
                        # encoding='utf-8',
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S;', level=logging.DEBUG)
    logger = logging.getLogger("Basic Logger")
    logger.info('Probemaker started')
    if False:
        hfiles = dict()  # Dict for heros' .json files
        group = dict()  # Dict to collect all Hero objects
        names = list()  # List to collect all names of heros in group

        # Create total path to hero files
        for hero in heros:
            hfiles[hero] = (data_folder / hero).resolve()

        if debug:
            print(heros)
            print("Data folder", data_folder)
            print(hfiles)

        # Create Hero objects
        for h in hfiles:
            Digga = Hero(hfiles[h], logger, show_values)
            names.append(Digga.name)
            group[Digga.name] = Digga
            logger.info(f'{Digga.name} loaded')

        run(group)

    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
