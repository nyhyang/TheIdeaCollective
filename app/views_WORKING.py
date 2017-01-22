from flask import render_template, redirect, request, session, url_for, g, flash, escape
from flask_login import login_user, logout_user, login_required
from flask.ext.login import current_user
from app import app, db, models, login_manager, auth
from .forms import LoginForm, ProfileForm, IdeaForm, CommentForm
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return models.lm_get_user_id(user_id)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        print('went to annonymous')
        return redirect(url_for('index'))
    oauth = auth.OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    print("provider oauth_callb", provider)
    print("current_user", current_user)
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = auth.OAuthSignIn.get_provider(provider)
    name, email, code = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        print('Authentication failed.')
        return redirect(url_for('index'))

    # Look if the user already exists
    session['name'] = name
    session['email'] = email
    session['code'] = code
    user_id = models.get_user_id(name, email, code)
    session['user_id'] = user_id

    # user_data = authenticate(username, password)
    # user_obj = user(user_data[0], user_data[1])
    # login_user(user_obj)

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if g.user is not None and type(g.user) == 'int':
        print("session['user_id'] A", session['user_id'])
        return redirect(url_for('editprofile'))
    form = LoginForm()
    if form.validate_on_submit():
        print("session['user_id'] B", session['user_id'])
        session['remember_me'] = form.remember_me.data
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/")
def index():
    email = ''
    if 'email' in session:
        email = escape(session['email'])
        name = escape(session['name'])
        print("session['user_id'] 2", session['user_id'])
        return redirect('/editprofile')
    else:
        return redirect('/editprofile')

@app.route('/logout')
def logout():
    g.user = None
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('code', None)
    session.pop('remember_me', None)
    # print("LOGOUT - session['user_id']", session['user_id'])
    return redirect(url_for('login'))

@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    form = ProfileForm()
    available_skills = models.get_available_skills()
    if 'user_id' in session:
        user = models.get_user(session['user_id'])
        bio = user[0][4]

    if request.method=='POST':
        name = request.form.get("name")
        email = session['email']
        code = session['code']
        bio = request.form.get("bio")
        personal_skill = request.form.get("personal_skill")
        skills = request.form.getlist('skills')
        models.add_user_profile(session['user_id'], name, bio, skills, personal_skill)
        return redirect('/ideafeed')
    return render_template('editprofile.html', form=form, user_id=session['user_id'], bio=bio, name=session['name'], email=session['email'], available_skills=available_skills)

@app.route('/ideafeed', methods=['GET', 'POST'])
def ideafeed():
    ideas = models.get_all_ideas()
    tags = models.get_all_tags()
    general_tags = models.get_gral_tags()

    tag_dict = {}
    for idx, r in enumerate(tags):
        tag_dict[r[0]] = []
    for idx, r in enumerate(tags):
        tag_dict[r[0]].append(r[1])
    # print(tag_dict)
    return render_template('ideafeed.html', user_id=session['user_id'], ideas=ideas, tags=tag_dict, general_tags=general_tags)


@app.route('/dashboard/<user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    # user_id = 1 # TODO: get from Google API
    user = models.get_user(user_id)
    skills = models.get_user_skills(user_id)
    ideas = models.get_user_ideas(user_id)
    tags = models.get_all_tags()
    tag_dict = {}
    for idx, r in enumerate(tags):
        tag_dict[r[0]] = []
    for idx, r in enumerate(tags):
        tag_dict[r[0]].append(r[1])
    return render_template('dashboard.html', user=user, skills=skills, ideas=ideas, tags=tag_dict)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    pass

@app.route('/createidea', methods=['GET', 'POST'])
def createidea():
    form = IdeaForm()
    available_skills = models.get_available_skills() 
    tagetories = models.get_available_tagetories()
    if request.method=='POST':
        user_id = 1
        name = request.form.get("name")
        description = request.form.get("description")
        # ownership = request.form.getlist("ownership-grp")
        ownership = request.form['ownership-grp']
        print("ownership", ownership)
        skills = request.form.getlist('skills')
        personal_skills = request.form.get("personal_skill")
        tagetories = request.form.getlist('tags')
        personal_tagetories = request.form.get("personal_tagetories")
        # Users
        models.add_idea(user_id, name, description, ownership, skills, personal_skills, tagetories, personal_tagetories)
        return redirect('/ideafeed')
    return render_template('createidea.html', form=form, user_id=session['user_id'], available_skills=available_skills, tagetories=tagetories)

@app.route('/ideapage/<idea_id>', methods=['GET', 'POST'])
def ideapage(idea_id):
    # TODO: Likes and Dislikes
    # print(idea_id)
    ideas = models.get_idea(idea_id)
    idea_creator = models.get_idea_creator(idea_id)
    # print(idea_creator)
    form = CommentForm()
    comments = models.get_comment(idea_id)
    tagetories = models.get_idea_tag(idea_id)
    skills = models.get_skills(idea_id)
    ownership = models.get_ownership(idea_id)
    if request.method=='POST': # Adds comments
        user_id = 1 # TODO: user_id or email (from session)? Or change comment table to include name?
        # idea_id = idea_id
        pub_priv = 'Public' # TODO: get this from database.
        comment = request.form.get("comment")
        date_time = datetime.now()
        models.add_comment(user_id, idea_id, comment, pub_priv, date_time)
        # return redirect('/ideafeed')

    # idea_dict = {} # Dictionary of users and passwords
    # idea_dict_keyList = ['id', 'idea_name', 'username', 'desc']
    # for idx, ida in enumerate(idea):
    #     idea_dict[idea_dict_keyList[idx]] = idea[idx]  
    # print(idea_dict)
    # print(idea)
    # return render_template('ideapage.html', idea_detail=idea_dict)
    return render_template('ideapage.html', ideas=ideas, form=form, user_id=session['user_id'], comments=comments, tagetories=tagetories, skills=skills, idea_creator=idea_creator, ownership=ownership)

