from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "E-Commerce"

CustomerCart=[]

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/logged',methods=['POST','GET'])
def logged():
    if request.method=='POST':
        role=request.form['Role']
        uname=request.form['Username']
        password=request.form['Password']
        with sqlite3.connect('Database.db') as connection:
            cur = connection.cursor()
            if(role=="Wholesaler"):
                cur.execute("SELECT * FROM  Wholesalers WHERE username=?", (uname,))
                rows=cur.fetchall()
                if len(rows)>=1:
                    if rows[0][2]==password:
                        session['Id']=rows[0][0]
                        return redirect(url_for('wholesalerHome'))
                    else:
                        flash('Password Incorrect ... Try Again !!')
                else :
                    flash('Username Incorrect ... Try Again !!')                
            elif(role=="Retailer"):
                cur.execute("SELECT * FROM  Retailers WHERE username=?", (uname,))
                rows=cur.fetchall()
                if len(rows)>=1:
                    if rows[0][2]==password:
                        session['Id']=rows[0][0]
                        return redirect(url_for('retailerOrder'))
                    else:
                        flash('Password Incorrect ... Try Again !!')
                else :
                    flash('Username Incorrect ... Try Again !!')                
            else:
                cur.execute("SELECT * FROM  Customers WHERE username=?", (uname,))
                rows=cur.fetchall()
                if len(rows)>=1:
                    if rows[0][2]==password:
                        session['Id']=rows[0][0]
                        return redirect(url_for('customerHome'))
                    else:
                        flash('Password Incorrect ... Try Again !!')
                else :
                    flash('Username Incorrect ... Try Again !!')
    return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    return render_template("SignUp.html") 

@app.route('/signed',methods=['POST','GET'])
def signed():
    if request.method=='POST':
        try:
            uname=request.form['uname']
            password=request.form['password']
            phone_num=request.form['phone_num']
            email=request.form['email']
            roles= request.form.getlist('roles')
            latitude=request.form['latitude']
            longitude=request.form['longitude']
            with sqlite3.connect('Database.db') as connection:
                cur = connection.cursor()
                for role in roles:
                    if role=="Wholesaler":
                        cur.execute("INSERT INTO Wholesalers (username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?);", (uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
                    elif role=="Retailer":
                        cur.execute("INSERT INTO Retailers (username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?);", (uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
                    elif role=="Customer":
                        cur.execute("INSERT INTO Customers (username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?);", (uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
        except:
            connection.rollback()
            return "Failed"
        finally:
            connection.close()
    return render_template('index.html')

@app.route('/wholesalerHome')
def wholesalerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerHome.html")

@app.route('/retailerHome')
def retailerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("RetailerHome.html")

@app.route('/customerHome')
def customerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("CustomerHome.html")
    
@app.route('/wholesalerAddItem',methods=['POST','GET'])
def wholesalerAddItem():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerUpload.html")


@app.route('/wholesalerUpdateItem',methods=['POST','GET'])
def wholesalerUpdateItem():
    if request.method == 'POST':
        try:
            val =session.get('Id', None)
            itemCategory = request.form['itemCategory']
            itemName = request.form['itemName']
            itemPrice = request.form['itemPrice']
            itemQuantity = request.form['itemQuantity']
            itemImage = request.form['itemImage']
            with sqlite3.connect("Database.db") as connection:
                cur = connection.cursor()
                cur.execute("INSERT INTO Items (ItemName,ItemPrice,ItemQuantity,ItemCategory,ItemOwnerId,ItemImageLink) VALUES (?,?,?,?,?,?);", (itemName,itemPrice,itemQuantity,itemCategory,val,itemImage))
                connection.commit()
                return "Inserted"
        except:
            connection.rollback()
            return "Failed"
        finally:
            connection.close()
    return "EXIT"

@app.route('/wholesalerDeleteItem',methods=['POST','GET'])
def wholesalerDeleteItem():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemOwnerId=?", (curid,))
    rows = cur.fetchall()
    return render_template("WholesalerRemove.html",rows=rows)


@app.route('/wholesalerRemoveItem',methods=['POST','GET'])
def wholesalerRemoveItem():
    if request.method == 'POST':
        try:
            itemId = request.form['itemId']
            with sqlite3.connect("Database.db") as connection:
                cur = connection.cursor()
                cur.execute("DELETE FROM Items  WHERE ItemId=?", (itemId,))
                connection.commit()
                return "Deleted"
        except:
            connection.rollback()
            return "Failed"
        finally:
            connection.close()
    return "EXIT"

@app.route('/retailerOrderAll',methods=['POST','GET'])
def retailerOrderAll():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items ")
    rows = cur.fetchall()
    return render_template("RetailerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

@app.route('/customerOrderAll',methods=['POST','GET'])
def customerOrderAll():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items ")
    rows = cur.fetchall()
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

@app.route('/addToCustomerCart',methods=['POST','GET'])
def addToCustomerCart():
    val =session.get('Id', None)
    Id = request.form['Id']
    quantity = request.form['quantity']
    print(val,Id,quantity)
    global CustomerCart
    return "Added To Cart"
    

if __name__ == "__main__":
    app.run(debug=True)        