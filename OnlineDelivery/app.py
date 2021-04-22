from flask import *
import sqlite3
import os


app = Flask(__name__)
app.secret_key = "E-Commerce"

global CustomerCart
CustomerCart={}

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
                        return redirect(url_for('retailerHome'))
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

def IdIncrement(role):
    if(role=="Customer"):
        cusid=0
        if not os.path.exists('CustomerId.txt'):
            with open('CustomerId.txt','w') as f:
                f.write('0')
        with open('CustomerId.txt','r') as f:
            cusid = int(f.read())
            cusid+=1 
        with open('CustomerId.txt','w') as f:
            f.write(str(cusid)) 
        return cusid
    elif(role=="Retailer"):
        rid=0
        if not os.path.exists('RetailerId.txt'):
            with open('RetailerId.txt','w') as f:
                f.write('0')
        with open('RetailerId.txt','r') as f:
            rid = int(f.read())
            rid+=1 
        with open('RetailerId.txt','w') as f:
            f.write(str(rid)) 
        return rid
    else :
        whid=0
        if not os.path.exists('WholesalerId.txt'):
            with open('WholesalerId.txt','w') as f:
                f.write('0')
        with open('WholesalerId.txt','r') as f:
            whid = int(f.read())
            whid+=1 
        with open('WholesalerId.txt','w') as f:
            f.write(str(whid)) 
        return whid

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
                        wid="WS"+str(IdIncrement("Wholesaler"))
                        cur.execute("INSERT INTO Wholesalers (Id,username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?,?);", (wid,uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
                    elif role=="Retailer":
                        rid="RT"+str(IdIncrement("Retailer"))
                        cur.execute("INSERT INTO Retailers (Id,username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?,?);", (rid,uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
                    elif role=="Customer":
                        cid="CS"+str(IdIncrement("Customer"))
                        cur.execute("INSERT INTO Customers (Id,username,password,eMailId,PhoneNumber,Latitude,Longitude) VALUES (?,?,?,?,?,?,?);", (cid,uname,password,email,phone_num,latitude,longitude))
                        connection.commit()
        except:
            connection.rollback()
            flash("Sign Up Failed")
        finally:
            connection.close()
    return render_template('index.html')

@app.route('/wholesalerHome')
def wholesalerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerHome.html")
   
#WHOLESALER

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
        except:
            connection.rollback()
            flash("Add Item Failed")
        finally:
            connection.close()
    return redirect(url_for('wholesalerHome'))

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
        except:
            connection.rollback()
            flash("Delete Item Failed")
        finally:
            connection.close()
    return redirect(url_for('wholesalerHome'))

@app.route('/viewRetailers',methods=['POST','GET'])
def viewRetailers():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerViewRetailers.html")

@app.route('/removeRetailers',methods=['POST','GET'])
def removeRetailers():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerRemoveRetailers.html")

# RETAILER

@app.route('/retailerHome')
def retailerHome():
    return render_template("RetailerHome.html")

@app.route('/retailerAddItem',methods=['POST','GET'])
def retailerAddItem():
    return render_template("RetailerUpload.html")

@app.route('/retailerUpdateItem',methods=['POST','GET'])
def retailerUpdateItem():
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
        except:
            connection.rollback()
            flash("Add Item Failed")
        finally:
            connection.close()
    return redirect(url_for('retailerHome'))

@app.route('/retailerDeleteItem',methods=['POST','GET'])
def retailerDeleteItem():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemOwnerId=?", (curid,))
    rows = cur.fetchall()
    return render_template("RetailerRemoveItem.html",rows=rows)

@app.route('/retailerOrderAll',methods=['POST','GET'])
def retailerOrderAll():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemOwnerId LIKE 'WS%'")
    rows = cur.fetchall()
    return render_template("RetailerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

@app.route('/retailerOrderCategory/<string:category>',methods=['GET'])
def retailerOrderCategory(category):
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemCategory=? AND ItemOwnerId LIKE 'WS%'",(category,))
    rows = cur.fetchall()
    return render_template("RetailerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

# CUSTOMER

@app.route('/customerHome')
def customerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    return render_template("CustomerHome.html")

@app.route('/customerOrderAll',methods=['POST','GET'])
def customerOrderAll():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemOwnerId LIKE 'RT%'")
    rows = cur.fetchall()
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

@app.route('/customerOrderCategory/<string:category>',methods=['GET'])
def customerOrderCategory(category):
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemCategory=? AND ItemOwnerId LIKE 'RT%'",(category,))
    rows = cur.fetchall()
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows))

@app.route('/addToCustomerCart',methods=['POST','GET'])
def addToCustomerCart():
    val =session.get('Id', None)
    Id = request.form['Id']
    quantity = request.form['quantity']
    global CustomerCart
    if(val not in CustomerCart):
        Items={Id:quantity}
        CustomerCart[val]=Items
    else :
        if(Id not in CustomerCart[val]):
            CustomerCart[val][Id]=quantity
        else:
            CustomerCart[val][Id]=int(CustomerCart[val][Id])+int(quantity)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT ItemQuantity FROM Items WHERE ItemId=?",(Id,))
    rows = cur.fetchall()
    newval=int(rows[0][0])-int(quantity)
    cur.execute("UPDATE Items SET ItemQuantity=? WHERE ItemId=?", (newval,Id,))
    connection.commit()
    return redirect(url_for('customerHome'))

@app.route('/removeFromCustomerCart',methods=['POST','GET'])
def removeFromCustomerCart():
    val =session.get('Id', None)
    Id = request.form['Id']
    quantity = request.form['quant']
    global CustomerCart
    del CustomerCart[val][Id]
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT ItemQuantity FROM Items WHERE ItemId=?",(Id,))
    rows = cur.fetchall()
    newval=int(rows[0][0])+int(quantity)
    cur.execute("UPDATE Items SET ItemQuantity=? WHERE ItemId=?", (newval,Id,))
    connection.commit()
    return redirect(url_for('customerHome'))

@app.route('/viewCustomerCart',methods=['POST','GET'])
def viewCustomerCart():
    val =session.get('Id', None)
    global CustomerCart
    if (val not in CustomerCart):
        flash("Check Out Our Products And Start Adding Items To Cart")
        return redirect(url_for('customerHome'))
    ItemIds=list(CustomerCart[val].keys())
    qt=list((CustomerCart[val]).values())
    totalcost=[]
    row=[]
    for i in range(0,len(ItemIds)):
        temp=[]
        connection = sqlite3.connect("database.db")
        cur = connection.cursor()
        cur.execute('SELECT ItemId,ItemName,ItemPrice FROM Items WHERE ItemId=?',(ItemIds[i],))
        rows = cur.fetchall()
        temp.append(rows[0][0])
        temp.append(rows[0][1])
        temp.append(rows[0][2])
        row.append(tuple(temp))
        totalcost.append(int(qt[i])*int(rows[0][2]))        
    totalsum=sum(totalcost)    
    return render_template("CustomerCart.html",range=range(0,len(row)),totalsum=totalsum,rows=row,totalcost=totalcost,quantity=list(CustomerCart[val].values()))

@app.route('/placeOrderOnline',methods=['POST','GET'])
def placeOrderOnline():
    val=session.get('Id',None)
    global CustomerCart
    Items=CustomerCart[val]
    key=list(Items.keys())
    item=""
    qty=""
    owner=""
    total_price=0
    for i in range(0,len(Items)):
        qt=Items.get(key[i])         
        item_id=key[i]
        qty=qty+qt+","
        item=item+str(item_id)+","        
        connection = sqlite3.connect("database.db")
        cur = connection.cursor()
        #Instead Of Querry By Id , Query By Name If More Than One Recored Returned Then Return Closest , https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude#:~:text=Install%20it%20via%20pip%20install,were%20looking%20for%20dist%20%3D%20mpu
        cur.execute("SELECT ItemPrice,ItemOwnerId,ItemName FROM Items WHERE ItemId=?",(item_id,))
        rows = cur.fetchall()
        total_price=total_price+(int(rows[0][0])*int(qt))
        owner=owner+str(rows[0][1])+","
        connection.close()
    with sqlite3.connect("Database.db") as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO Orders (OrderedBy,OrderedTo,ItemsOrdered,QuantityOrdered,TotalCost,Status) VALUES (?,?,?,?,?,?);", (val,owner,item,qty,total_price,'Ordered'))
        connection.commit()
    
    return "Success"

@app.route('/logout')
def logout():
    val = session.get('Id', None)
    session.pop(val, None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)        