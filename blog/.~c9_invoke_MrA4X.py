from flask import render_template,request,redirect, url_for

from blog import app
from .database import session, Entry


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
def add_entry_get():
    return render_template("add_entry.html")
    
    
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry=Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
@app.route("/entry/<int:id>")
def id_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("id_entry.html", entry=entry)
    
@app.route("/entry/<int:id>/edit", methods=["GET", "POST"])
def edit_entry(id):
    entry = session.query(Entry).get(id)
    entry_new=Entry(
         title=request.form["title"],
         content=request.form["content"],
         )
    if entry_new != entry:
       session.add(entry_new)
       session.commit()
       return redirect(url_for("entries"))
    else:
        return render_template("add_entry.html", entry=entry)
       
       
      
    