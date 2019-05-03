# -*- coding: utf-8 -*-
'''Flask file for Raspberry Pi'''

import platform
import datetime
import os
import subprocess
import socket

from flask import render_template, redirect, request
from flask import Flask
from flask_bootstrap import Bootstrap

APP = Flask(__name__)
Bootstrap(APP)

@APP.route('/')
@APP.route('/main.html')
def mainhtml():
    return render_template('main.html')

@APP.route('/stats.html')
def stats():
    today = datetime.date.today()
    system = platform.system()
    node = platform.node()
    arch = platform.machine()
    user = os.getlogin()

    space = os.statvfs('/home/'+user)
    freespace = (space.f_frsize * space.f_bavail)/1024/1024

    get_uptime = subprocess.Popen('uptime', stdout=subprocess.PIPE)
    uptime = get_uptime.stdout.read()

    return render_template('stats.html', today=today, system= \
                            system, node=node, arch=arch, user=user, \
                            freespace=freespace, uptime=uptime)


@APP.route('/dienste.html')
def vnc():
    user = os.getlogin()
    node = platform.node()
    try:
        myip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        myip.connect(('8.8.8.8', 80))
        getip = myip.getsockname()[0]
        myip.close()
    except StandardError:
        getip = "IP nicht erkannt"

    showbutton = True
    if os.path.exists('/home/'+user+'/.vnc/'+node+':1.pid'):
        showbutton = None
    return render_template('dienste.html', showbutton=showbutton, getip=getip)

@APP.route('/<vncstatus>', methods=['POST'])
def vncsteer(vncstatus):
    if vncstatus == "startserver":
        try:
            server_up = ["tightvncserver", ":1", "-geometry", \
                        "1024x768", "-depth", "24"]
            subprocess.call(server_up)
        except StandardError:
            print "Server startet nicht oder läuft bereits."
    if vncstatus == "stoppserver":
        try:
            server_down = ["tightvncserver", "-kill", ":1"]
            subprocess.call(server_down)
        except StandardError:
            print "Server läuft nicht oder lässt sich nicht beenden."
    return redirect('/dienste.html')


@APP.route('/reboot', methods=['POST'])
def reboot():
    passwd = request.form['password']
    rbt1 = subprocess.Popen(["echo", passwd], stdout=subprocess.PIPE)
    rbt2 = subprocess.Popen(["sudo", "-S", "reboot"], stdin=rbt1.
                            stdout, stdout=subprocess.PIPE)
    print rbt2.communicate()[0]
    return redirect('/dienste.html')

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8080, debug=True)
