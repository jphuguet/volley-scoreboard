import json
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
import os.path
import argparse

parser = argparse.ArgumentParser(description='Scripts options.')
parser.add_argument('--debug-off', dest='is_debug_on', action='store_false')
args = parser.parse_args()

is_debug_on = args.is_debug_on

GAMEDIR = "match"

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = "H4MWdBLKVT8dnn8bpd3wx6FwvV8BnZ"

socketio = SocketIO(app,debug=is_debug_on,cors_allowed_origins='*')

class Game:
    def __init__(self):
        self.filenames = self.gen_filenames()
        self.read_score_files()

    def gen_filenames(self):
        file_lst = []
        for team in ['a', 'b']:
            for set_num in range(1, 6):
                filename = u"team_{team}_set_{set_num}".format(team=team,set_num=set_num)
                file_lst.append(filename)
            name = u"team_{}_name".format(team)
            file_lst.append(name)
            logo = u"team_{}_logo".format(team)
            file_lst.append(logo)
            color = u"team_{}_color".format(team)
            file_lst.append(color)
        file_lst.append("set_num")
        return file_lst

    def read_score_files(self):
        self.create_files()
        self.score = {}
        self.set_num = int(self.read_set_num())
        for team in ['a', 'b']:
            tmp_dict = {}
            for set_num in range(1, self.set_num+1):
                tmp_dict[set_num] = int(self.read_score_file(team=team, set_num=set_num))
            tmp_dict["name"] = self.get_team_name(team)
            tmp_dict["logo"] = self.get_team_logo(team)
            tmp_dict["color"] = self.get_team_color(team)

            self.score[team] = tmp_dict
        self.score['set'] = self.set_num

    def create_files(self):
        for f in self.filenames:
            if not os.path.exists(u"{}/{}".format(GAMEDIR, f)):
                print(f + " does not exists, creating...")
                value = "0"
                if f == "set_num":
                    value = "1"
                if f.endswith("_name"):
                    value = "Team name"
                filename = u"{}/{}".format(GAMEDIR, f)
                with open(filename, 'x') as f:
                    f.write(str(value))
                    f.close()
                
    def new_game(self):
        self.delete_files()
        self.read_score_files()

    def delete_files(self):
        for f in self.filenames:
            filename = u"{}/{}".format(GAMEDIR, f)
            if os.path.exists(filename):
                if filename.endswith("_name") or filename.endswith("_logo") or filename.endswith("_color"):
                    continue
                print("deleting file {}".format(f))
                os.remove(filename)

    def read_set_num(self, ):
        filename = u"{gamedir}/set_num".format(gamedir=GAMEDIR)
        with open(filename, 'r') as f:
            val = f.read()
            f.close()
        return val

    def increase(self, team):
        val = int(self.score[team][self.set_num]) + 1
        self.update_score_file(team=team, score=val)
        self.score[team][self.set_num] = self.read_score_file(team=team,set_num=self.set_num)
        # print(u"--- Increased score from team {team} ---".format(team=team))
  
    def decrease(self, team):
        point = int(self.score[team][self.set_num])
        val = 0 if point < 1 else point - 1
        self.update_score_file(team=team, score=val)
        self.score[team][self.set_num] = self.read_score_file(team=team,set_num=self.set_num)
        # print(u"--- Decreased score from team {team} ---".format(team=team))

    def update_score_file(self, team, score):
        filename = u"{gamedir}/team_{team}_set_{set_num}".format(gamedir=GAMEDIR,team=team,set_num=self.set_num)
        with open(filename, 'w') as f:
            f.write(str(score))
            f.close()
    
    def read_score_file(self, team, set_num):
        filename = u"{gamedir}/team_{team}_set_{set_num}".format(gamedir=GAMEDIR,team=team,set_num=set_num)
        with open(filename, 'r') as f:
            score = f.read()
            f.close()
        return score

    def get_team_name(self, team):
        filename = u"{gamedir}/team_{team}_name".format(gamedir=GAMEDIR,team=team)
        with open(filename, 'r') as f:
            name = f.read()
            f.close()
        return name.upper()

    def update_team_names(self, names):
        for team in ['a', 'b']:
            filename = u"{gamedir}/team_{team}_name".format(gamedir=GAMEDIR,team=team)
            with open(filename, 'w') as f:
                f.write(names[team])
                f.close()

    def update_team_colors(self, colors):
        for team in ['a', 'b']:
            filename = u"{gamedir}/team_{team}_color".format(gamedir=GAMEDIR,team=team)
            with open(filename, 'w') as f:
                f.write(colors[team])
                f.close()

    def change_set(self, value):
        self.score['previous_set_value'] = self.set_num
        tmp_set = int(self.set_num) + value
        if tmp_set < 1:
            tmp_set = 1
        if tmp_set > 5:
            tmp_set = 5
        self.score['set'] = self.set_num = tmp_set
        # print("{}/{}".format(self.set_num, self.score['previous_set_value']))

        filename = u"{gamedir}/set_num".format(gamedir=GAMEDIR)
        with open(filename, 'w') as f:
            f.write(str(self.set_num))
            f.close()

        for team in ['a', 'b']:
            if self.set_num not in self.score[team]:
                self.score[team][self.set_num] = 0 # initialise score for new set

    def list_logos(self):
        # only jpg png and svg files accepted. dumb and simple
        img = [f for f in os.listdir("static/logos") if f.lower().endswith('jpg') or f.lower().endswith('png') or f.lower().endswith('svg')]
        return {"files": sorted(img)}

    def update_team_logos(self, data):
        for team,logo in data.items():
            filename = u"{gamedir}/team_{team}_logo".format(gamedir=GAMEDIR,team=team)
            with open(filename, 'w') as f:
                f.write(str(logo))
                f.close()            
                self.score[team]['logo'] = logo

    def get_team_logo(self, team):
        filename = u"{gamedir}/team_{team}_logo".format(gamedir=GAMEDIR,team=team)
        with open(filename, 'r') as f:
            logo = f.read()
            f.close()
        return logo

    def get_team_color(self, team):
        filename = u"{gamedir}/team_{team}_color".format(gamedir=GAMEDIR,team=team)
        with open(filename, 'r') as f:
            color = f.read()
            f.close()
        return color

    def get_score(self,team):
        return self.score[team][self.set_num]

    def get_all(self):
        return self.score


# WebSockets
@socketio.on('connect')
def on_connect():
    print('Connected to the server')
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)
    emit('setup', json.dumps(scoreboard.list_logos()), broadcast=True)

@socketio.on('increment')
def handle_increment(team):
    scoreboard.increase(team)
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('decrement')
def handle_decrement(team):
    scoreboard.decrease(team)
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('increment_set')
def handle_increment_set():
    scoreboard.change_set(1)
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('decrement_set')
def handle_idecrement_set():
    scoreboard.change_set(-1)
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('team_names')
def handle_team_names(names):
    scoreboard.update_team_names(names)
    scoreboard.read_score_files()
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('team_colors')
def handle_team_colors(colors):
    scoreboard.update_team_colors(colors)
    scoreboard.read_score_files()
    emit('logos_colors', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('team_logos')
def team_logos(data):
    scoreboard.update_team_logos(data)
    emit('logos_colors', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('new_game')
def handle_new_game():
    scoreboard.new_game()
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)

@socketio.on('reload')
def handle_reload():
    scoreboard.read_score_files()
    emit('all', json.dumps(scoreboard.get_all()), broadcast=True)


scoreboard = Game()


# FLASK Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/remote')
def remote():
    return render_template('remote.html')

@app.route('/score')
def score():
    # print(request.headers.get('User-Agent'))
    return render_template('score.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    socketio.run(app.run(debug=is_debug_on, host="0.0.0.0", port=3000))
