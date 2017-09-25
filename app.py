from __future__ import print_function  # In python 2.
import sys
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template
import indeed as ind
import JaccardSimilarity as mal
import linkedin as lik

app = Flask(__name__.split('.')[0])   # create the application instance


def connect_db():
    """Connect to the specific database."""
    rv = sqlite3.connect('linked_deed.db')
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Open a new database connection.

    If there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT DISTINCT WHAT, URL, DESCRIPTION FROM jobs_indeed order by ACCURACY desc')
    entries = cur.fetchall()
    return render_template('jobs.html', entries=entries)


@app.route('/index', methods=['POST'])
def login():
    url = request.form['url']
    em = request.form['email']
    pwd = request.form['password']
    lik.main(em, pwd, url)
    db = get_db()
    cur = db.execute('SELECT LOCATION, DESIGNATIONS FROM linkedin_skills WHERE ID=1')
    entry = cur.fetchone()
    # print(entry[1].split(", "), file=sys.stderr)
    return render_template('form.html', jobs=entry[1].split(", "), location=entry[0].split(", "))


@app.route('/form', methods=['POST'])
def form():
    what = request.form['what']
    city = request.form['city']
    state = request.form['state']
    location = city + ", " + state
    db = get_db()
    db.execute('UPDATE linkedin_skills SET DESIGNATIONS = ? WHERE ID = 1', (what, ))
    db.commit()
    db.execute('UPDATE linkedin_skills SET LOCATION = ? WHERE ID = 1', (location, ))
    db.commit()
    ind.indeed_jobs(job=what, location=location)
    mal.main()
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
