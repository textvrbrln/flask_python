 from flask import Flask
 from flask import render_template
 from flask_bootstrap import Bootstrap

 app = Flask(__name__)
 Bootstrap(app)

 @app.route('/')
 def hello_world():
     return 'Hello World!'

 @app.route('/hello.html')
 def hello():
     nachricht = "Hallo Welt!"
     return render_template('hello.html', nachricht=nachricht)

 if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8080, debug=True)