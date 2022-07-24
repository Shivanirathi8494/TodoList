from flask import Flask,render_template,request,session,redirect
import sqlite3

DATABASE = 'todolist.db'

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def home():
    try:
        username=session['user']
        return  redirect('/todolist')
    except KeyError:
        return render_template('home.html')   
    return render_template('home.html')

@app.route('/inprogress',methods = ['POST']) 
def markAsInprogress():
    if request.method == 'POST':
        todoitemid = request.form['todo_item_id']
        userid = session['user_id']
        isSuccess = updateTodoItemInDB(userid,todoitemid,'INPROGRESS') 
        if isSuccess:
            return  'markAsInprogress: is Success'
    return 'markAsInprogress: is Failure'

@app.route('/done',methods = ['POST']) 
def markAsDone():
    if request.method == 'POST':
        todoitemid = request.form['todo_item_id']
        userid = session['user_id']
        isSuccess = updateTodoItemInDB(userid,todoitemid,'DONE') 
        if isSuccess:
            return  'markAsDone: is Success'
    return 'markAsDone: is Failure'

@app.route('/remove',methods = ['POST']) 
def removeTodoItem():
    if request.method == 'POST':
        todoitemid = request.form['todo_item_id']
        userid = session['user_id']
        isSuccess = deleteTodoItemFromDB(userid,todoitemid) 
        if isSuccess:
            return  'removeTodoItem: is Success'
    return 'removeTodoItem: is Failure'

@app.route('/register',methods = ['POST', 'GET']) 
def userRegistration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['pwd']
        isSuccess = saveUserToDB(username,email,pwd) 
        if isSuccess:
            return  render_template('login.html')
    try:
        username=session['user']
        return  redirect('/todolist')
    except KeyError:
        return render_template('userregistration.html') 
    return render_template('userregistration.html')

@app.route('/login',methods = ['POST', 'GET']) 
def userLogin():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['pwd']
        isSuccess = verifyUserCred(username,pwd) 
        if isSuccess[0]:
            session['user'] = username
            session['user_id'] = isSuccess[1]
            return  redirect('/todolist')
    try:
        username=session['user']
        return  redirect('/todolist')
    except KeyError:
        return render_template('login.html')       
    return render_template('login.html')

@app.route('/todolist') 
def todolist():
    userid = session['user_id']
    todolist = fetchTodoList(userid)
    return render_template('Todolist.html',todolist = todolist)

@app.route('/add',methods=['POST'])
def additem():
    if request.method == 'POST':
        todoitem = request.form['todoitem']
        userid = session['user_id']
        isSuccess = saveTodoItemToDB(userid,todoitem) 
        if isSuccess:
            return  redirect('/todolist')
    return  redirect('/todolist')

def saveUserToDB(username,email,password):
    print("Saving userdetails to DB : "+username + " " + email +" " + password)
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO user(user_name,password,email) VALUES (?,?,?)",(username,password,email) )
        con.commit()
        success = True
        print("userdetails DB Success :) ")
    except:
        con.rollback()
        success = False
        print("userdetails DB Failure !!!! ")
    finally:
        con.close()
    return success

def updateTodoItemInDB(userid,todoitemid,status):
    print("update updateTodoItem in DB : "+userid + " " + todoitemid +" " + status)
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("UPDATE todolist SET status = ? where user_id = ? AND todo_item_id = ?",(status,userid,todoitemid) )
        con.commit()
        success = True
        print("updateTodoItem DB Success :) ")
    except:
        con.rollback()
        success = False
        print("updateTodoItem DB Failure !!!! ")
    finally:
        con.close()
    return success

def deleteTodoItemFromDB(userid,todoitemid):
    print("Delete TodoItemFromDB in DB : "+userid + " " + todoitemid )
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("DELETE from todolist where user_id = ? AND todo_item_id = ?",(userid,todoitemid) )
        con.commit()
        success = True
        print("deleteTodoItemFromDB DB Success :) ")
    except:
        con.rollback()
        success = False
        print("deleteTodoItemFromDB DB Failure !!!! ")
    finally:
        con.close()
    return success

def verifyUserCred(username, password):
    print("Verify userdetails from DB : "+username +" " + password)
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("Select user_id,password from user where user_name=?",(username,))
        row = cur.fetchall()
        print(row)
        if len(row)==0:
            print("User doesn't exist.")
            return (0,"User doesn't exist.")
        elif row[0][1]!=password:
            print("Password is incorrect.")
            return (0,"Password is incorrect.")
        else:
            return (1,str(row[0][0]))  
    except:
        con.rollback()
        success = False
        print("userdetails DB Failure !!!! ")
    finally:
        con.close()
    print("Unable to login.")
    return (0,"Unable to login.") 

def saveTodoItemToDB(userid,todoitem):
    print("Saving todoitem to DB : "+userid + " " + todoitem )
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO todolist(user_id,todo_item,status) VALUES (?,?,?)",(userid,todoitem,'PENDING') )
            con.commit()
            success = True
            print("todoitem DB Success :) ")
    except:
        con.rollback()
        success = False
        print("todoitem DB Failure !!!! ")
    finally:
        con.close()
    return success

def fetchTodoList(userid):
    print("Fetch todoitem from DB : ")
    todolist = []
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("Select todo_item_id,todo_item,status from todolist where user_id=?",(userid,))
        todolist = cur.fetchall()
        print(todolist)
        return todolist  
    except:
        con.rollback()
        success = False
        print("Fetch todoitem DB Failure !!!! ")
    finally:
        con.close()
    print("Unable to fetch todoitem.")
    return todolist


@app.route('/logout') 
def userLogout():
    session.pop('user',None)
    return render_template('login.html')

if __name__ =='__main__':  
    app.run(debug = True) 