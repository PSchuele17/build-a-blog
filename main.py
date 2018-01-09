from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('blog.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()
    user_id = request.args.get('id')
    return render_template('blog.html', blogs=blogs)

@app.route('/entry', methods=['POST', 'GET'])
def entry():
    user_id = request.args.get('id')
    blogs = Blog.query.filter_by(id=user_id)
    return render_template('entry.html', blogs=blogs)


@app.route('/newpost')
def display_newpost():
    
    return render_template("new-blog.html")


@app.route('/newpost', methods=['POST','GET'])
def newpost():
    title = request.form['title']
    body = request.form['body']
    title_error = ''
    body_error = ''

    if len(title) <= 0:
        title_error = 'please enter a valid title'

    elif len(body)<= 0:
        body_error = 'please enter a valid body'
    
    if request.method == 'POST' and not title_error and not body_error:
        
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        return render_template('post.html',
        title=title,
        body=body)
    
    else:
        return render_template("new-blog.html",
        title=title,
        body=body,
        title_error=title_error,
        body_error=body_error
        )

  
    

    
    

    
    
    


if __name__ == '__main__':
    app.run()