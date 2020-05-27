from flask import Flask, render_template,redirect,request,url_for,session, json, jsonify, flash
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from locator import locate
import pymysql
from plots import dataindia
from dist import district
import math
from india_stats import current_stats
from plots_call import plot_day
from india_pred import pred_list
from ml_model import pred_maha
import os, time

app = Flask(__name__)
app.secret_key = "qazsedcft"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
app.config['SQLALCHEMY_DATABASE_URI'] = "db2+ibm_db://gjs08791:7g6bbx8s9l9%5Egpjg@dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net:50000/BLUDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
DATA FOR LINE, BAR, PIE CHART
'''
def roundup(x):
    return int(math.ceil(x / 1000.0)) * 1000


# Array of india
deaths,cases,Dates=dataindia()

#array of district
dates,mumbai,pune,nashik,nagpur,thane  =district()

district_data=[mumbai,pune,nashik,nagpur,thane]
district_name=["Mumbai","Pune","Nashik","Nagpur","Thane" ]
no_of_dis=len(district_data)
max_of_dis=[roundup(max(mumbai)),roundup(max(pune)),roundup(max(nashik)),roundup(max(nagpur)),roundup(max(thane))]

labels = [
    'Cases', 'Deaths',"Recovery"]

values = [
    cases[-1],deaths[-1],45900
    
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C"]
'''
END OF LINE, BAR, PIE CHART
'''



class adminregister(db.Model):
    
    username = db.Column(db.String(20), nullable=False,primary_key=True)
    password1 = db.Column(db.String(20), nullable=False)

class users(db.Model):
    
    username = db.Column(db.String(20), nullable=False,primary_key=True)
    phone=db.Column(db.String(20), nullable=False)
    password1 = db.Column(db.String(20), nullable=False)

class volunteerlist(db.Model):
        
    username = db.Column(db.String(20), nullable=True)
    email=db.Column(db.String(20), nullable=False)
    address=db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False,primary_key=True)
    choice1=db.Column(db.String(20), nullable=False)
    choice2 = db.Column(db.String(20), nullable=False)
    choice3=db.Column(db.String(20), nullable=False)
    field = db.Column(db.String(20), nullable=False)
    idcard=db.Column(db.String(20), nullable=False)
    morning=db.Column(db.String(10), nullable=False)
    afternoon=db.Column(db.String(10), nullable=False)
    evening=db.Column(db.String(10), nullable=False)


class donors(db.Model):
        
    username = db.Column(db.String(20), nullable=True)
    age=db.Column(db.String(20), nullable=False)
    address=db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False,primary_key=True)
    bloodgroup=db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(20), nullable=False)

class contactus(db.Model):
    email = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(12), nullable=False)
    query = db.Column(db.String(120), nullable=False)

class item(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    description = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    value1 = db.Column(db.Integer)
    total = db.Column(db.Integer)
    
    



@app.route("/")
def home():
    dt = datetime.now()
    datestring=str(dt.day)+str(dt.month)
    folder_path='static/img/plots/'+datestring
        
    t, r,d, a, nc, nr, nd=current_stats()                                             
    f=plot_day()
    pc, pd, pr, gr=pred_list()
    predictions, growth_rate=pred_maha()
    
    if not os.path.exists(folder_path):
        time.sleep(10)
    
    return render_template('index.html',tot=t, dea=d, rec=r, act=a, newcases=nc, newrec=nc, newdea=nd, folder=f, pred_c=pc, pred_d=pd,
                           pred_r=pr, growth=gr, pm=predictions[0], pp=predictions[1], pt=predictions[2],pnag=predictions[3],pnas=predictions[4],
                           gm=(growth_rate[0]),gp=growth_rate[1],gt=growth_rate[2],gnag=growth_rate[3],gnas=growth_rate[4])

    
@app.route("/index")
def index():
    t, r,d, a, nc, nr, nd=current_stats()                                             
    f=plot_day()
    pc, pd, pr, gr=pred_list()
    predictions, growth_rate=pred_maha()
    
    return render_template('index.html',tot=t, dea=d, rec=r, act=a, newcases=nc, newrec=nc, newdea=nd, folder=f, pred_c=pc, pred_d=pd,
                           pred_r=pr, growth=gr, pm=predictions[0], pp=predictions[1], pt=predictions[2],pnag=predictions[3],pnas=predictions[4],
                           gm=growth_rate[0],gp=growth_rate[1],gt=growth_rate[2],gnag=growth_rate[3],gnas=growth_rate[4])


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        flash('Already Logged In')
        return redirect(url_for('total'))
    if "admin" in session:
        flash('Please Logout First')
        return redirect('admin')
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form['password']
        login = users.query.filter_by(username=username, password1=password1).first()
        if login is not None:
            session['user'] = username
            return redirect(url_for("total"))
        else:
            return render_template("user_login.html", error = 1)
    return render_template("user_login.html", error = 0)

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
    if "admin" in session:
        session.pop("admin", None)
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])

def register():
    if 'user' in session:
        flash('Please Logout First')
        return redirect(url_for('total'))
    if 'admin' in session:
        flash('Please Logout First')
        return redirect(url_for('admin'))

    addr=locate()

    if request.method == "POST":
        username = request.form['username']
        phone = request.form['phone']
        password1 = request.form['password']
        register = users(username = username, phone=phone, password1 = password1)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html",addr=addr)



@app.route('/medical')
def medical(): 
    return render_template("medical.html")


@app.route('/sealeduser')
def sealeduser(): 
    if "admin" in session:
        data = item.query.all()
        usernames = set()
        for i in range(len(data)):
            usernames.add(data[i].username)
        return render_template("sealedUserStatus.html", data = data, usernames = usernames)

@app.route('/addList', methods=['POST'])
def addList():
    if request.method == "POST":
        name = session['user']
        desc = (request.form['desc']).upper()
        amt = int(request.form['amt'])
        val = int(request.form['val'])
        total = amt * val
        query = item(username = name, description = desc, amount = amt, value1 = val, total = total)
        db.session.add(query)
        db.session.commit()
        return redirect(url_for('total'))
    return redirect(url_for('total'))


@app.route('/adminlogin')
def adminlogin(): 
    if "user" in session:
        flash('Please Logout First')
        return redirect("total")
    if "admin" in session:
        flash('Already Logged In')
        return redirect(url_for('admin'))
    
    return render_template("admin_login.html")


@app.route('/admin')
def admin():  
    if "admin" in session:
        bar_labels=labels
        bar_values=values
        return render_template('adminPageNew.html', title='Cases in India', max=17000, labels=bar_labels, values=bar_values,max_of_dis=max_of_dis,dates=dates,district_data=district_data,district_name=district_name,no_of_dis=no_of_dis, which_ = 'bar')
    return redirect('admin')

@app.route('/adminPageNew_line')
def adminPageNew_line():
    if "admin" in session:
        flash('Already Logged In')
        return render_template('adminPageNew_line.html', title='Cases in India',max_of_dis=max_of_dis,dates=dates,district_data=district_data,district_name=district_name,no_of_dis=no_of_dis, len=len(Dates))
    return redirect('admin')

@app.route('/adminPageNew_pie')
def adminPageNew_pie():
    pie_labels = labels
    pie_values = values
    return render_template('adminPageNew_pie.html', title='Indian Pie Chart', max=17000, set=zip(values, labels, colors))

@app.route('/mumbai')
def mumbai():
    if 'admin' in session:
        query1 = volunteerlist.query.filter_by(choice1 = 'mumbai', morning = '1').all()
        query2 = volunteerlist.query.filter_by(choice1 = 'mumbai', afternoon = '1').all()
        query3 = volunteerlist.query.filter_by(choice1 = 'mumbai', evening = '1').all()

        return render_template('mumbai.html', morning = query1, afternoon = query2, evening = query3)

    '''
    # db.session.commit()
    # print(query1)
    # l1 = [i for i in query1]
    # q = len(l1) 
    # if q<2:
    #     query2 = volunteerlist.query.filter_by(choice2 = 'Mumbai').limit(2-q).all()
    #     l2 = [i for i in query2]
    #     for i in l2:
    #         l1.append(i)

    # if len(l1) < 2:
    #     query3 = volunteerlist.query.filter_by(choice3 = 'Mumbai').limit(2-len(l1)).all()
    #     l3 = [i for i in query3]
    #     for i in l3:
    #         l1.append(i)
            
    # avg = len(l1) / 3
    # out = []
    # last = 0.0
    # while last < len(l1):
    #     out.append(l1[int(last):int(last + avg)])
    #     last += avg

    # morning = out[0] #slot1
    # afternoon = out[1] #slot2
    # evening = out[2] #slot3 
    # # print(json.dumps)
    # # print(morning)
    # # print(afternoon)
    # # print(evening)
    # # print("s")
    # res1=res2=res3=[]
    # for i in morning:
    #     ph=str(i)
    #     ph=(ph[15:-1] )
    #     userdetail=volunteerlist.query.filter_by(phone=ph).first()
    #     result=userdetail.__dict__
    #     username=(result['username'])
    #     phone=(result['phone'])
    #     email=(result['email'])
       
    #     res1.append((username+" "+phone+" "+email))
    #     print(res1)

    # for i in afternoon:
    #     ph=str(i)
    #     ph=(ph[15:-1] )
    #     userdetail=volunteerlist.query.filter_by(phone=ph).first()
    #     result=userdetail.__dict__
    #     username=(result['username'])
    #     phone=(result['phone'])
    #     email=(result['email'])
     
       
    #     res2.append((username+" "+phone+" "+email))
        
    #     print(res2)

    # for i in evening:
    #     ph=str(i)
    #     ph=(ph[15:-1] )
    #     userdetail=volunteerlist.query.filter_by(phone=ph).first()
    #     result=userdetail.__dict__
    #     username=(result['username'])
    #     phone=(result['phone'])
    #     email=(result['email'])
       
    #     print(res3)

    #     res3.append((username+" "+phone+" "+email))

    # return render_template("mumbai.html",morning=res1[:5],afternoon=res2[5:],evening=res3[4:])
    '''



@app.route('/hospitals')
def hospitals(): 
    return render_template("hospitals.html")



@app.route('/yodhaloggedin')
def yodhaloggedins(): 
    if 'admin' in session:
        flash('Please Logout first')
        return redirect(url_for('admin'))
    return render_template("yodhaloggedin.html")

@app.route("/checkadmin",methods = ['GET', 'POST'])
def checkadmin():
    if "admin" in session:
        
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form["username"]
        password1 = request.form['password']
        login = adminregister.query.filter_by(username=username, password1=password1).first()
        if login is not None:
            session["admin"] = username
            return redirect(url_for("admin"))
        else:
            return render_template('admin_login.html', error = 1)
    return render_template('admin_login.html')

	# if request.method == 'POST':
    #     username = request.form["username"]
    #     password1 = request.form['password']
    #     login = adminregister.query.filter_by(username=username, password1=password1).first()
    #     if login is not None:
    #         return redirect(url_for("admin"))
    # return render_template('admin_login.html')


@app.route("/crosslist")
def crosslist():
    return render_template('crosslist.html')

@app.route("/total", methods=["POST", "GET"])
def total():
    if "user" in session:
        user = session['user']
        data = item.query.filter_by(username = user).all()
        length = len(data)
        sumTotal = 0
        for i in range(len(data)):
            sumTotal += data[i].total
        # sumTotal = item.query(func.sum(item.total).label('total')).fetchall()
        return render_template('total.html', user = user, data = data, sumTotal = sumTotal, length = length)
    else:
        return redirect(url_for("login"))


@app.route("/yodha")
def yodha():
    if "user" in session:
        flash('Please Logout First')
        return redirect(url_for('total'))
    if "admin" in session:
        flash('Please Logout First')
        return redirect('admin')
    return render_template('yodha.html')

@app.route("/vol")
def volunteerform():
    return render_template('vol.html')



@app.route("/reg_volunteer",methods = ['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        address=request.form["address"]
        phone = request.form["phone"]
        choice1=request.form["choice1"]
        choice2 = request.form["choice2"]
        choice3=request.form["choice3"]
        field = request.form["field"]
        idcard=request.files["idcard"]
        slot=request.form.getlist('slot')
        morning=afternoon=evening=0
        print(slot)
        if '1' in slot:
            morning=1   
        if '2' in slot:
            afternoon=1
        if '3' in slot:
            evening=1

        
        print(morning,afternoon,evening)
        register = volunteerlist(username=username,email=email,address=address,phone=phone,choice1=choice1,choice2=choice2,choice3=choice3,field=field,idcard=idcard.read(),morning=morning,afternoon=afternoon,evening=evening)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("yodhaloggedins"))

    return render_template("vol.html")

@app.route("/reg_donor",methods = ['GET', 'POST'])
def blooddonor():
    if request.method == 'POST':
        username = request.form["username"]
        age = request.form["age"]
        address=request.form["address"]
        phone = request.form["phone"]
        weight=request.form["weight"]
        bloodgroup = request.form["bloodgroup"]
        # gender=request.form["gender"]
        
        register = donors(username=username,age=age,address=address,phone=phone,weight=weight,bloodgroup=bloodgroup)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("bloodform.html")



@app.route("/bloodform")
def bloodform():
    return render_template('blood.html')
@app.route("/donate")
def donate():
    return render_template('donate.html')


@app.route("/contactus", methods = ['GET', 'POST'])
def contactUs():
    if(request.method=='POST'):
        query = request.form['query']
        email = request.form['email']
        username = request.form['username']
        subject = request.form['subject']
        entry = contactus(username=username,query=query,subject =subject,email=email)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("contact.html")





app.run(debug=True)