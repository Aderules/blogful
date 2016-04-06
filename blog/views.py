from flask import render_template,request,redirect, url_for,flash
from flask.ext.login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash

from blog import app
from .database import session, Entry, User


PAGINATE_BY =10
    

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    #Zero-indexed page
    page_index = page -1
    
    count = session.query(Entry).count()
    
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count -1) / PAGINATE_BY +1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html", 
           entries=entries,
           has_next=has_next,
           has_prev=has_prev,
           page=page,
           total_pages=total_pages
         )
    
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")
    
    
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry=Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    

@app.route("/entry/<int:id>")
@login_required
def id_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("id_entry.html", entry=entry)
    


@app.route("/entry/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_entry(id):
    entry=session.query(Entry).get(id)
    if request.method == "POST":
        if entry.author == current_user:
                entry.title = request.form["title"],
                entry.content=request.form["content"],
                entry.id= id
                entry.author==current_user
                session.add(entry)
                session.commit()
                flash("Entry has been saved", "success")
                return redirect(url_for("entries"))
        flash("You are not authorised to make changes on this entry","danger")
    return render_template("edit_entry.html", entry_title=entry.title, entry_content=entry.content)
    



#delete each entry, "Get" method in instance where value of "answer" is "no" uses default external "Get" method    
@app.route("/entry/<int:id>/delete", methods =["GET", "POST"])
@login_required
def delete_entry(id):
    entry = session.query(Entry).get(id)
    if  request.method == "POST":
        if entry.author==current_user:
                session.delete(entry)
                session.commit()
                flash("Entry has been deleted","success")
                return redirect(url_for("entries"))
        flash("You are not authorised to make changes on this entry","danger")            
    return render_template("delete_entry.html", entry=entry)
    
  
    
#@app.route("/?limit=20")
#@app.route("/page/2?limit=20")
#def limit_page():# provide default value for limit
    #print request.args.get('limit') == 20:
        #return render_template("limit_entry.html")



@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
    
@app.route("/login", methods=["POST"])
def login_post():
    email=request.form["email"]
    password=request.form["password"]
    user=session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
              flash("Incorrect username or password", "danger")
              return redirect( url_for("login_get"))
              
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

@app.route("/logout", methods=["GET"])
def logout_get():
    return redirect(url_for ("login_get"))
    

    