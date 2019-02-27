from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8888/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key= 'fut214202fx'

# class for the database, stores blog entries

class Entry(db.Model):

    # data that should go into columns, primary ID below
    id = db.Column(db.Integer, primary_key=True)
    # set to Text so there is not a character limit
    title = db.Column(db.Text) # this is the title
    body = db.Column(db.Text) # this is the post
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


# display individual blog entries or all blog posts

@app.route('/blog')
def display_blog_entries():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template('single_entry.html', title="Blog Post", entry=entry)
    else:
        # display every existing blog entry
        sort = request.args.get('sort')
        # displays newest first
        if (sort=="newest"):
            all_entries = Entry.query.order_by(Entry.created.desc()).all()
        else:
        # just shows all entries
            all_entries = Entry.query.all()
        return render_template('all_entries.html', title= "All Blog Posts", all_entries=all_entries)


# validation for empty post

def empty_val(x):
    if x:
        return True
    else:
        return False

# redirect and error messages

@app.route('/new_entry', methods=['GET', 'POST'])
# form for new blog entry with get, create new entry or redisplay if invalid with post
def add_entry():
    if request.method == 'POST':
        #create empty string for errors
        title_error = ""
        entry_error = ""

        # assigning variable to blog title
        entry_title = request.form['blog_title']
        # assigning variable to blog body
        entry_body = request.form['blog_body']
        # new blog post variable from title and entry
        entry_new = Entry(entry_title, entry_body)

        # entry will be added if title and body have inputs in them
        if empty_val(entry_title) and empty_val(entry_body):
            # adds new post
            db.session.add(entry_new)
            # adds to database
            db.session.commit()
            post_link = "blog?id=" + str(entry_new.id)
            return redirect(post_link)
        else:
            if not empty_val(entry_title) and not empty_val(entry_body):
                title_error = "Please enter your blog title."
                entry_error = "Please enter the body of your blog entry."
                return render_template('new_post.hmtl', entry_error=entry_error, title_error=title_error)
            elif not empty_val(entry_title):
                title_error = "Please enter your blog title."
                return render_template('new_post.hmtl', title_error=title_error, entry_body=entry_body)
            elif not empty_val(entry_body):
                entry_error = "Please enter the body of your blog entry."
                return render_template('new_post.hmtl', entry_error=entry_error, entry_title=entry_title)
    
    # display new blog entry form
    else:
        return render_template('new_post.html')

# runs when main.py file runs

if __name__ == "__main__":
    app.run()


