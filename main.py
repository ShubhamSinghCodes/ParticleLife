from uuid import uuid4
from time import time
from math import sqrt
from random import randint
from base64 import b64encode,b64decode

from flask import Flask, session, request, copy_current_request_context

app = Flask(__name__,static_url_path='')
app.secret_key = "randomsecretkeyidk"
global Data
Data = {}
Height = 480
Width = 640
colournames = ["red",
               "blue",
               "green",
               "white",
               "yellow",
               "orange"]
preset = {"still":"MHwwfDB8MHwwfDAKMHwwfDB8MHwwfDAKMHwwfDB8MHwwfDAKMHwwfDB8MHwwfDAKMHwwfDB8MHwwfDAKMHwwfDB8MHwwfDA=",
          "repelmax":"LTEwfC0xMHwtMTB8LTEwfC0xMHwtMTAKLTEwfC0xMHwtMTB8LTEwfC0xMHwtMTAKLTEwfC0xMHwtMTB8LTEwfC0xMHwtMTAKLTEwfC0xMHwtMTB8LTEwfC0xMHwtMTAKLTEwfC0xMHwtMTB8LTEwfC0xMHwtMTAKLTEwfC0xMHwtMTB8LTEwfC0xMHwtMTA=",
          "attractmax":"MTB8MTB8MTB8MTB8MTB8MTAKMTB8MTB8MTB8MTB8MTB8MTAKMTB8MTB8MTB8MTB8MTB8MTAKMTB8MTB8MTB8MTB8MTB8MTAKMTB8MTB8MTB8MTB8MTB8MTAKMTB8MTB8MTB8MTB8MTB8MTA=",
          "repelmid":"LTV8LTV8LTV8LTV8LTV8LTUKLTV8LTV8LTV8LTV8LTV8LTUKLTV8LTV8LTV8LTV8LTV8LTUKLTV8LTV8LTV8LTV8LTV8LTUKLTV8LTV8LTV8LTV8LTV8LTUKLTV8LTV8LTV8LTV8LTV8LTU=",
          "attractmid":"NXw1fDV8NXw1fDUKNXw1fDV8NXw1fDUKNXw1fDV8NXw1fDUKNXw1fDV8NXw1fDUKNXw1fDV8NXw1fDUKNXw1fDV8NXw1fDU=",
          "cell":"LTd8MHw2fDB8MHwtNwowfC05fDF8MHwwfDAKMHwwfDB8OXwwfDAKMHw2fDB8MHwtN3wwCjB8NnwwfC04fDB8MAowfDB8MnwwfDB8LTg=",
          "ring":"LTEwMHwwfDB8MXwwfDAKMHwtMTAwfDB8MXwwfDAKMHwwfC0xMDB8MXwwfDAKMTB8MTB8MTB8LTF8MTB8MTAKMHwwfDB8MXwtMTAwfDAKMHwwfDB8MXwwfC0xMDA=",
}



@app.route('/video_feed')
def video_feed():
    @copy_current_request_context
    def update_data():
        def get_g(c1,c2,allg):
            if allg:
                return 0 if allg[c1+c2] == 0 else 1/allg[c1+c2]
            else:
                return 0
        Data[session['uid']]["Time"] = time()
        for i,particle in enumerate(Data[session['uid']].get("Particles")):
            fx = 0
            fy = 0
            for other in Data[session['uid']].get("Particles"):
                if abs(other[0]-particle[0]) < abs(Width-max(particle[0],other[0])+min(particle[0],other[0])):
                    dx = other[0]-particle[0]
                else:
                    dx = Width-max(particle[0],other[0])+min(particle[0],other[0]) * (1 if particle[0] > other[0] else -1)
                if abs(other[1]-particle[1]) < abs(Width-max(particle[1],other[1])+min(particle[1],other[1])):
                    dy = other[1]-particle[1]
                else:
                    dy = Width-max(particle[1],other[1])+min(particle[1],other[1]) * (1 if particle[1] > other[1] else -1)
                d = sqrt(dx*dx+dy*dy)
                if d > 0 and d < 150:
                    if d < 10:
                        g = -1/10
                    else:
                        g = get_g(particle[2],other[2],Data[session['uid']].get("allg"))
                    f = g * (1/d)
                    fx += f * dx
                    fy += f * dy
            particle[3] += fx
            particle[4] += fy
            particle[3] *= 0.9
            particle[4] *= 0.9
        for i,particle in enumerate(Data[session['uid']].get("Particles")):
            Data[session['uid']]["Particles"][i][0] += particle[3]
            Data[session['uid']]["Particles"][i][1] += particle[4]
            Data[session['uid']]["Particles"][i][0] %= Width
            Data[session['uid']]["Particles"][i][1] %= Height
    if session.get("uid"):
        for _ in range(5):
            update_data()
        return str([[round(p[0]),round(p[1]),colournames[int(p[2])]] for p in Data[session['uid']]["Particles"]]).replace("'",'"')
    else:
        return '[]'

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    x = data['x']
    y = data['y']
    c = data['color']
    Data[session['uid']]["Particles"].append([x,y,c,0.,0.])
    return ''

@app.route('/clear', methods=['GET'])
def clear():
    Data[session['uid']] = {"Time": time(), "Particles": []}
    return ''

@app.route('/random', methods=['GET'])
def addrand():
    for _ in range(25):
        Data[session['uid']]["Particles"].append([randint(0,Width), randint(0,Height), str(randint(0,5)), 0., 0.])
    return ''

@app.route('/randomrules', methods=['GET'])
def randrules():
    allg = {"00": randint(-10, 10),
            "01": randint(-10, 10),
            "02": randint(-10, 10),
            "03": randint(-10, 10),
            "04": randint(-10, 10),
            "05": randint(-10, 10),
            "10": randint(-10, 10),
            "11": randint(-10, 10),
            "12": randint(-10, 10),
            "13": randint(-10, 10),
            "14": randint(-10, 10),
            "15": randint(-10, 10),
            "20": randint(-10, 10),
            "21": randint(-10, 10),
            "22": randint(-10, 10),
            "23": randint(-10, 10),
            "24": randint(-10, 10),
            "25": randint(-10, 10),
            "30": randint(-10, 10),
            "31": randint(-10, 10),
            "32": randint(-10, 10),
            "33": randint(-10, 10),
            "34": randint(-10, 10),
            "35": randint(-10, 10),
            "40": randint(-10, 10),
            "41": randint(-10, 10),
            "42": randint(-10, 10),
            "43": randint(-10, 10),
            "44": randint(-10, 10),
            "45": randint(-10, 10),
            "50": randint(-10, 10),
            "51": randint(-10, 10),
            "52": randint(-10, 10),
            "53": randint(-10, 10),
            "54": randint(-10, 10),
            "55": randint(-10, 10), }
    combined = getstr(allg)
    Data[session['uid']]["allg"] = allg
    return combined

@app.route('/load', methods=['POST'])
def load():
    data = request.get_json()
    combined = data['allg']
    if combined in preset:
        combined = preset[combined]
    try:
        allg_new_v = "|".join(b64decode(combined.encode("ascii")).decode("ascii").split("\n")).split("|")
        allg_new_k = [str(k).rjust(2, "0") for k in range(0, 56) if k % 10 < 6]
        allg_new = {allg_new_k[i]: int(allg_new_v[i]) for i in range(36)}
    except:
        allg = Data[session['uid']]['allg']
        return getstr(allg)
    Data[session['uid']]["allg"] = allg_new
    return combined

@app.route('/')
@app.route('/action')
def index():
    if not "uid" in session:
        session['uid'] = str(uuid4())
    if not session['uid'] in Data:
        session['uid'] = str(uuid4())
        allg = {"00": randint(-10, 10),
                "01": randint(-10, 10),
                "02": randint(-10, 10),
                "03": randint(-10, 10),
                "04": randint(-10, 10),
                "05": randint(-10, 10),
                "10": randint(-10, 10),
                "11": randint(-10, 10),
                "12": randint(-10, 10),
                "13": randint(-10, 10),
                "14": randint(-10, 10),
                "15": randint(-10, 10),
                "20": randint(-10, 10),
                "21": randint(-10, 10),
                "22": randint(-10, 10),
                "23": randint(-10, 10),
                "24": randint(-10, 10),
                "25": randint(-10, 10),
                "30": randint(-10, 10),
                "31": randint(-10, 10),
                "32": randint(-10, 10),
                "33": randint(-10, 10),
                "34": randint(-10, 10),
                "35": randint(-10, 10),
                "40": randint(-10, 10),
                "41": randint(-10, 10),
                "42": randint(-10, 10),
                "43": randint(-10, 10),
                "44": randint(-10, 10),
                "45": randint(-10, 10),
                "50": randint(-10, 10),
                "51": randint(-10, 10),
                "52": randint(-10, 10),
                "53": randint(-10, 10),
                "54": randint(-10, 10),
                "55": randint(-10, 10), }
        combined = getstr(allg)
        Data[session['uid']] = {"Time": time(), "Particles": [], "allg": allg}
    else:
        allg = Data[session['uid']]['allg']
        combined = getstr(allg)
    for k,v in list(Data.items()):
        if time() - v["Time"] > 300:
            print(f"Cleaned up {k}")
            del Data[k]
    html = f"""
    <body bgcolor="#202020">
    <div style="text-align: center;">
    <h3 id="header" style="color: white;text-align: center;">Particle Life<br>Rulestring: {combined}</h3>
    <canvas id="canvas" style="width: {Width};height: {Height};">
    Your browser does not support the canvas element.
    </canvas>
    <div style="color: white;text-align: center;">
        <p>Colour:</p>
        <div style="width: 50%;height: -webkit-fill-available;float: left;">
            <input type="radio" id="red" name="selcor" value="0">
            <label for="red">Red</label><br>
            <input type="radio" id="blue" name="selcor" value="1">
            <label for="blue">Blue</label><br>
            <input type="radio" id="green" name="selcor" value="2">
            <label for="green">Green</label>
        </div>
        <div style="width: 50%;height: -webkit-fill-available;float: left;">
            <input type="radio" id="white" name="selcor" value="3">
            <label for="white">White</label><br>
            <input type="radio" id="yellow" name="selcor" value="4">
            <label for="yellow">Yellow</label><br>
            <input type="radio" id="orange" name="selcor" value="5">
            <label for="orange">Orange</label>
        </div>
    </div>
    <div style="color: white;text-align: center;">
        <button id="clearbutton">Clear</button>
        <button id="rand">Randomly Populate</button>
        <button id="randrules">New Random Rule</button><br>
        <input type="text" id="newrule" name="newrule" hint="Rulestring for new rule">
        <button id="loadrule">Load Rule</button>
    </div>
    <script>
    var canvas = document.getElementById("canvas");
    canvas.setAttribute("width", {Width});
    canvas.setAttribute("height", {Height});
    canvas.addEventListener("click", function(event) {{
        var x = event.offsetX;
        var y = event.offsetY;
        var c = document.querySelector('input[name="selcor"]:checked').value;
        // Send coordinates to Flask route via AJAX request
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/click", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({{'x': x, 'y': y, 'color': c}}));

    }});
    var lbutton = document.getElementById("loadrule");
    lbutton.addEventListener("click", function() {{
        var allg = document.getElementById("newrule").value;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/load", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({{'allg': allg}}));
        xhr.onload = function(combined) {{
            document.getElementById("header").innerHTML = "Particle Life<br>Rulestring: "+combined.currentTarget.responseText;
        }}

    }});
    var cbutton = document.getElementById("clearbutton");
    cbutton.addEventListener("click", function() {{
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/clear", true);
        xhr.send();

    }});
    var rbutton = document.getElementById("rand");
    rbutton.addEventListener("click", function() {{
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/random", true);
        xhr.send();

    }});
    var rrbutton = document.getElementById("randrules");
    rrbutton.addEventListener("click", function() {{
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/randomrules", true);
        xhr.send();
        xhr.onload = function(combined) {{
            document.getElementById("header").innerHTML = "Particle Life<br>Rulestring: "+combined.currentTarget.responseText;
        }}

    }});
    function getdata() {{
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/video_feed", true);
        xhr.send();
        xhr.onload = function(data) {{
            draw(JSON.parse(data.currentTarget.responseText));
        }}
    }}
    function draw(particles) {{
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, {Width}, {Height});
        for (i=0;i<particles.length;i++) {{
            ctx.fillStyle = particles[i][2];
            ctx.fillRect(particles[i][0],particles[i][1],3,3);
        }}
    }}
    setInterval(getdata, 250);
    </script>
    </div>
    </body>
    """
    return html


def getstr(allg):
    return b64encode("\n".join(["|".join([str(allg[str(k).rjust(2,"0")]) for k in range(0,56) if str(k).rjust(2,"0") in allg][i:i+6]) for i in [0,6,12,18,24,30]]).encode("ascii")).decode("ascii")
if __name__ == "__main__":
    app.run()
