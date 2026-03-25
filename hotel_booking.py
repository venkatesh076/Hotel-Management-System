from flask import Flask,render_template_string,request,redirect,session
import sqlite3
import random
import datetime

app=Flask(__name__)
app.secret_key="hotel"

def db():
    return sqlite3.connect("hotel.db")

# DATABASE
con=db()

con.execute("""

CREATE TABLE IF NOT EXISTS customers(

id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone TEXT,
address TEXT,
checkin TEXT,
checkout TEXT,
room TEXT,
price INTEGER,
days INTEGER,
roomno INTEGER,
restaurant INTEGER DEFAULT 0,
status TEXT DEFAULT 'active'

)

""")

con.commit()
con.close()

rooms={
"Standard Non AC":3500,
"Standard AC":4000,
"3 Bed Non AC":4500,
"3 Bed AC":5000
}

# LOGIN
@app.route('/',methods=['GET','POST'])
def login():

    if request.method=="POST":

        if request.form['user']=="admin" and request.form['pass']=="venkatesh@7":

            session['login']=True

            return redirect('/dashboard')

    return render_template_string("""

<style>

body{

background:linear-gradient(135deg,#667eea,#764ba2);
font-family:Segoe UI;
color:white;
text-align:center;
padding-top:150px;

}

.box{

background:rgba(255,255,255,0.1);
backdrop-filter:blur(20px);
width:400px;
margin:auto;
padding:40px;
border-radius:20px;

}

input{

width:100%;
padding:15px;
margin:12px 0;
border-radius:10px;
border:none;

}

button{

width:100%;
padding:15px;
background:#00ffd5;
border:none;
border-radius:10px;
font-weight:bold;

}

</style>

<div class="box">

<h1>HOTEL OS</h1>

<form method="post">

<input name="user" placeholder="Username">

<input type="password"
name="pass"
placeholder="Password">

<button>Login</button>

</form>

</div>

""")

# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'login' not in session:
        return redirect('/')

    con=db()

    total=con.execute(
"SELECT COUNT(*) FROM customers"
).fetchone()[0]

    active=con.execute(
"SELECT COUNT(*) FROM customers WHERE status='active'"
).fetchone()[0]

    revenue=con.execute(
"SELECT SUM(price*days)+SUM(restaurant) FROM customers"
).fetchone()[0]

    if revenue is None:
        revenue=0

    con.close()

    return render_template_string("""

<style>

body{
margin:0;
font-family:Segoe UI;
background:linear-gradient(135deg,#1f4037,#99f2c8);
}

.sidebar{

width:260px;
height:100vh;
background:linear-gradient(#141e30,#243b55);
position:fixed;
color:white;

}

.logo{

font-size:26px;
text-align:center;
padding:30px;

}

.sidebar a{

display:block;
padding:18px;
color:white;
text-decoration:none;

}

.sidebar a:hover{

background:#00ffd5;
color:black;

}

.main{

margin-left:260px;
padding:40px;

}

.cards{

display:grid;
grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
gap:30px;

}

.card{

background:white;
padding:40px;
border-radius:20px;
text-align:center;
box-shadow:0 10px 25px rgba(0,0,0,0.2);

}

.number{

font-size:45px;
color:#6a11cb;

}

</style>

<div class="sidebar">

<div class="logo">
HOTEL OS
</div>

<a href="/dashboard">Dashboard</a>
<a href="/booking">Booking</a>
<a href="/records">Records</a>
<a href="/active">Active Guests</a>
<a href="/customers">Total Customers</a>
<a href="/logout">Logout</a>

</div>

<div class="main">

<h1>Dashboard</h1>

<div class="cards">

<a href="/customers">

<div class="card">

<div class="number">
{{total}}
</div>

Total Customers

</div>

</a>

<a href="/active">

<div class="card">

<div class="number">
{{active}}
</div>

Active Guests

</div>

</a>

<div class="card">

<div class="number">

₹ {{revenue}}

</div>

Revenue

</div>

</div>

</div>

""",total=total,
active=active,
revenue=revenue)

# BOOKING UI
@app.route('/booking')
def booking():

    return render_template_string("""

<style>

body{

background:linear-gradient(135deg,#ff9a9e,#fad0c4);
font-family:Segoe UI;

}

.form{

width:500px;
margin:auto;
background:white;
padding:40px;
border-radius:20px;
margin-top:50px;

}

input,select{

width:100%;
padding:14px;
margin:10px;
border-radius:10px;
border:1px solid grey;

}

button{

padding:14px;
width:100%;
background:#ff758c;
border:none;
border-radius:10px;
color:white;

}

</style>

<div class="form">

<h1>Room Booking</h1>

<form action="/book" method="post">

<input name="name" placeholder="Name">

<input name="phone" placeholder="Phone">

<input name="address" placeholder="Address">

<input type="date" name="checkin">

<input type="date" name="checkout">

<select name="room">

<option>Standard Non AC</option>
<option>Standard AC</option>
<option>3 Bed Non AC</option>
<option>3 Bed AC</option>

</select>

<button>Book Room</button>

</form>

<a href="/dashboard">
Back
</a>

</div>

""")

# BOOK LOGIC
@app.route('/book',methods=['POST'])
def book():

    d=request.form

    ci=datetime.datetime.strptime(
d['checkin'],"%Y-%m-%d")

    co=datetime.datetime.strptime(
d['checkout'],"%Y-%m-%d")

    days=(co-ci).days

    price=rooms[d['room']]

    roomno=random.randint(100,999)

    con=db()

    con.execute("""

INSERT INTO customers

(name,phone,address,
checkin,checkout,
room,price,days,roomno)

VALUES(?,?,?,?,?,?,?,?,?)

""",(d['name'],d['phone'],
d['address'],
d['checkin'],
d['checkout'],
d['room'],
price,
days,
roomno))

    con.commit()
    con.close()

    return redirect('/records')

# RECORDS UI
@app.route('/records')
def records():

    con=db()

    data=con.execute(
"SELECT * FROM customers WHERE status='active'"
).fetchall()

    con.close()

    return render_template_string("""

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#43cea2,#185a9d);
}

table{

width:90%;
margin:auto;
background:white;
border-radius:15px;

}

th{

background:#6a11cb;
color:white;
padding:15px;

}

td{

padding:15px;
text-align:center;

}

button{

padding:10px 20px;
border:none;
border-radius:8px;
background:#00c9ff;
color:white;

}

</style>

<h1 style="text-align:center">
Active Records
</h1>

<table>

<tr>

<th>Name</th>
<th>Room</th>
<th>Food</th>
<th>Add</th>
<th>Bill</th>
<th>Checkout</th>

</tr>

{% for i in data %}

<tr>

<td>{{i[1]}}</td>
<td>{{i[6]}}</td>
<td>₹ {{i[10]}}</td>

<td>

<form action="/addfood" method="post">

<input type="hidden"
name="id"
value="{{i[0]}}">

<input name="food"
placeholder="Amount">

<button>Add</button>

</form>

</td>

<td>

<a href="/bill/{{i[0]}}">
<button>Bill</button>
</a>

</td>

<td>

<a href="/delete/{{i[0]}}">
<button>Checkout</button>
</a>

</td>

</tr>

{% endfor %}

</table>

<a href="/dashboard">
Back
</a>

""",data=data)

# ACTIVE GUEST UI
@app.route('/active')
def active():

    con=db()

    data=con.execute(
"SELECT * FROM customers WHERE status='active'"
).fetchall()

    con.close()

    return render_template_string("""

<style>

body{

background:linear-gradient(135deg,#30cfd0,#330867);
font-family:Segoe UI;

}

.card{

background:white;
width:300px;
padding:25px;
border-radius:15px;
margin:20px;
display:inline-block;

}

</style>

<h1 style="text-align:center;color:white">
Active Guests
</h1>

{% for i in data %}

<div class="card">

<h3>{{i[1]}}</h3>

<p>Room {{i[9]}}</p>

<p>{{i[6]}}</p>

</div>

{% endfor %}

<a href="/dashboard">
Back
</a>

""",data=data)

# TOTAL CUSTOMERS UI
@app.route('/customers')
def customers():

    con=db()

    data=con.execute(
"SELECT * FROM customers"
).fetchall()

    con.close()

    return render_template_string("""

<style>

body{

background:linear-gradient(135deg,#f7971e,#ffd200);
font-family:Segoe UI;

}

table{

width:80%;
margin:auto;
background:white;
border-radius:15px;

}

th{

background:#ff512f;
color:white;
padding:15px;

}

td{

padding:15px;
text-align:center;

}

</style>

<h1 style="text-align:center">

Customer History

</h1>

<table>

<tr>

<th>Name</th>
<th>Room</th>
<th>Status</th>

</tr>

{% for i in data %}

<tr>

<td>{{i[1]}}</td>
<td>{{i[6]}}</td>
<td>{{i[11]}}</td>

</tr>

{% endfor %}

</table>

<a href="/dashboard">
Back
</a>

""",data=data)

# FOOD
@app.route('/addfood',methods=['POST'])
def addfood():

    id=request.form['id']

    price=int(request.form['food'])

    con=db()

    con.execute("""

UPDATE customers

SET restaurant=restaurant+?

WHERE id=?

""",(price,id))

    con.commit()
    con.close()

    return redirect('/records')

# BILL UI
@app.route('/bill/<id>')
def bill(id):

    con=db()

    d=con.execute(
"SELECT * FROM customers WHERE id=?",
(id,)
).fetchone()

    con.close()

    room=d[7]*d[8]

    food=d[10]

    gst=(room+food)*.18

    total=room+food+gst

    return render_template_string("""

<style>

body{

font-family:Segoe UI;
background:linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;

}

.bill{

background:white;
color:black;
width:400px;
margin:auto;
padding:30px;
border-radius:20px;

}

</style>

<div class="bill">

<h1>Invoice</h1>

<p>{{d[1]}}</p>

<p>Room ₹ {{room}}</p>

<p>Food ₹ {{food}}</p>

<p>GST ₹ {{gst}}</p>

<h2>Total ₹ {{total}}</h2>

<button onclick="window.print()">
Print
</button>

</div>

<a href="/records">
Back
</a>

""",d=d,
room=room,
food=food,
gst=gst,
total=total)

# CHECKOUT
@app.route('/delete/<id>')
def delete(id):

    con=db()

    con.execute("""

UPDATE customers

SET status='checkedout'

WHERE id=?

""",(id,))

    con.commit()
    con.close()

    return redirect('/records')

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

if __name__=="__main__":

    app.run(debug=True)