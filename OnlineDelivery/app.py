from flask import *
import sqlite3
import os
import mpu

app = Flask(__name__)
app.secret_key = "E-Commerce"

global CustomerCart
CustomerCart={}
global RetailerCart
RetailerCart={}
global OrderStatus
OrderStatus=['Order Placed','Order Dispatched','In Transit','Delivered']

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

def getlocation(rows):
    val=session.get('Id',None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT Latitude,Longitude FROM Customers  WHERE Id=?",(val,))
    row=cur.fetchall()
    distance=[]
    for i in range(0,len(rows)):
        ownerId=rows[i][5]
        cur.execute("SELECT Latitude,Longitude FROM Retailers WHERE Id=?",(ownerId,))
        r=cur.fetchall()
        lat1=float(row[0][0])
        lon1=float(row[0][1])
        lat2=float(r[0][0])
        lon2=float(r[0][1])
        dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
        dist=int(dist)
        dist=str(dist)+" "+"Kms Away From You"
        distance.append(dist)
    return distance

#WHOLESALER

@app.route('/wholesalerHome')
def wholesalerHome():
    return render_template("WholesalerHome.html")

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
            
            global CustomerCart
            customerIds=list(CustomerCart.keys())
            for i in customerIds:
                print(i)
                print(CustomerCart)
                itemIds=list(i.keys())

                for j in itemIds:
                    print(j)
                    if itemId in j:
                        del CustomerCart[i][j] 
            print(CustomerCart)
            with sqlite3.connect("Database.db") as connection:
                cur = connection.cursor()
                cur.execute("DELETE FROM Items  WHERE ItemId=?", (itemId,))
                cur.execute
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

@app.route('/addToRetailerCart',methods=['POST','GET'])
def addToRetailerCart():
    val =session.get('Id', None)
    Id = request.form['Id']
    quantity = request.form['quantity']
    global RetailerCart
    if(val not in RetailerCart):
        Items={Id:quantity}
        RetailerCart[val]=Items
    else :
        if(Id not in RetailerCart[val]):
            RetailerCart[val][Id]=quantity
        else:
            RetailerCart[val][Id]=int(RetailerCart[val][Id])+int(quantity)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT ItemQuantity FROM Items WHERE ItemId=?",(Id,))
    rows = cur.fetchall()
    newval=int(rows[0][0])-int(quantity)
    cur.execute("UPDATE Items SET ItemQuantity=? WHERE ItemId=?", (newval,Id,))
    connection.commit()
    return redirect(url_for('retailerOrderAll'))

@app.route('/removeFromRetailerCart',methods=['POST','GET'])
def removeFromRetailerCart():
    val =session.get('Id', None)
    Id = request.form['Id']
    quantity = request.form['quant']
    global RetailerCart
    del RetailerCart[val][Id]
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT ItemQuantity FROM Items WHERE ItemId=?",(Id,))
    rows = cur.fetchall()
    newval=int(rows[0][0])+int(quantity)
    cur.execute("UPDATE Items SET ItemQuantity=? WHERE ItemId=?", (newval,Id,))
    connection.commit()    
    return redirect(url_for('viewRetailerCart'))

@app.route('/viewRetailerCart',methods=['POST','GET'])
def viewRetailerCart():
    val =session.get('Id', None)
    global RetailerCart
    if (val not in RetailerCart):
        flash("Check Out Our Products And Start Adding Items To Cart")
        return redirect(url_for('retailerHome'))
    ItemIds=list(RetailerCart[val].keys())
    qt=list((RetailerCart[val]).values())
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
    return render_template("RetailerCart.html",range=range(0,len(row)),totalsum=totalsum,rows=row,totalcost=totalcost,quantity=list(RetailerCart[val].values()))

@app.route('/retailerOrder',methods=['POST','GET'])
def retailerOrder():
    val=session.get('Id',None)
    global RetailerCart
    Items=RetailerCart[val]
    key=list(Items.keys())
    item=""
    qty=""
    owner=""
    total_price=0
    cat=""
    price=""
    name=""
    for i in range(0,len(Items)):
        qt=Items.get(key[i])         
        item_id=key[i]
        qty=qty+qt+","
        item=item+str(item_id)+","        
        connection = sqlite3.connect("database.db")
        cur = connection.cursor()
        cur.execute("SELECT ItemPrice,ItemOwnerId,ItemName,ItemCategory,ItemPrice FROM Items WHERE ItemId=?",(item_id,))
        rows = cur.fetchall()
        total_price=total_price+(int(rows[0][0])*int(qt))
        owner=owner+str(rows[0][1])+","
        name=name+str(rows[0][2])+","
        cat=cat+str(rows[0][3])+","
        price=price+str(rows[0][4])+","
        connection.close()
    item=item[:-1]
    qty=qty[:-1]
    owner=owner[:-1]
    cat=cat[:-1]
    price=price[:-1]
    name=name[:-1]
    with sqlite3.connect("Database.db") as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO Orders (OrderedBy,OrderedTo,ItemsOrdered,QuantityOrdered,TotalCost,Status,ItemCategory,ItemUnitPrice,ItemName) VALUES (?,?,?,?,?,?,?,?,?);", (val,owner,item,qty,total_price,'Ordered',cat,price,name))
        connection.commit()    
    return redirect(url_for('retailerTransactions'))

@app.route('/retailerTransactions',methods=['POST','GET'])
def retailerTransactions():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Orders WHERE OrderedBy=?",(curid,))
    rows = cur.fetchall()
    return render_template("RetailerTransactions.html",rows=rows)

@app.route('/retailerCustomerTransactions',methods=['POST','GET'])
def retailerCustomerTransactions():
    curid=session.get('Id',None)
    connection=sqlite3.connect("database.db")
    cur=connection.cursor()
    cur.execute("SELECT * FROM Orders ")
    row=[]
    rows=cur.fetchall()
    for i in range(0,len(rows)):
        Retailer_list=rows[i][2].split(",")
        Item_list=rows[i][3].split(",")
        Qty_list=rows[i][4].split(",")
        
        Item_UnitPrice=rows[i][8].split(",")
        Item_Name=rows[i][9].split(",")
        temp=[]
        for j in range(0,len(Retailer_list)):
            if(Retailer_list[j]==curid):
                temp.append(rows[i][0])
                
                cur.execute("SELECT username from Customers WHERE Id =?",(rows[0][1],))
                c_name=cur.fetchall()
                temp.append(c_name[0][0])
                
                temp.append(Qty_list[j])
                cur.execute("SELECT ItemPrice FROM Items WHERE ItemId=?",(Item_list[j],))
                item_price=cur.fetchall()
                temp.append(item_price[0][0] * int(Qty_list[j]))
                temp.append(rows[i][6])
                
                temp.append(Item_UnitPrice[j])
                temp.append(Item_Name[j])
                


                row.append(tuple(temp))
                temp.clear()
            else:
                continue
    
            
    return render_template("RetailerViewCustomerTransactions.html",rows=row) 


# CUSTOMER


@app.route('/customerHome')
def customerHome():
    return render_template("CustomerHome.html")

@app.route('/customerOrderAll',methods=['POST','GET'])
def customerOrderAll():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemOwnerId LIKE 'RT%'")
    rows = cur.fetchall()
    distance=getlocation(rows)
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows),distance=distance)    

@app.route('/customerOrderCategory/<string:category>',methods=['GET'])
def customerOrderCategory(category):
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Items WHERE ItemCategory=? AND ItemOwnerId LIKE 'RT%'",(category,))
    rows = cur.fetchall()
    distance=getlocation(rows)
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows),distance=distance)

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
    return redirect(url_for('customerOrderAll'))
    

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
    return redirect(url_for('viewCustomerCart'))

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
    global OrderStatus
    Items=CustomerCart[val]
    key=list(Items.keys())
    item=""
    qty=""
    owner=""
    total_price=0
    cat=""
    price=""
    name=""
    details="Mahesh,+91 9123456780,26/04/2020"    
    for i in range(0,len(Items)):
        qt=Items.get(key[i])         
        item_id=key[i]
        qty=qty+qt+","
        item=item+str(item_id)+","        
        connection = sqlite3.connect("database.db")
        cur = connection.cursor()
        cur.execute("SELECT ItemPrice,ItemOwnerId,ItemName,ItemCategory,ItemPrice FROM Items WHERE ItemId=?",(item_id,))
        rows = cur.fetchall()
        total_price=total_price+(int(rows[0][0])*int(qt))
        owner=owner+str(rows[0][1])+","
        name=name+str(rows[0][2])+","
        cat=cat+str(rows[0][3])+","
        price=price+str(rows[0][4])+","
        connection.close()
    item=item[:-1]
    qty=qty[:-1]
    owner=owner[:-1]
    cat=cat[:-1]
    price=price[:-1]
    name=name[:-1]    
    with sqlite3.connect("Database.db") as connection:
        cur = connection.cursor()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        cur.execute("INSERT INTO Orders (OrderedBy,OrderedTo,ItemsOrdered,QuantityOrdered,TotalCost,Status,ItemCategory,ItemUnitPrice,ItemName,DeliveryDetails) VALUES (?,?,?,?,?,?,?,?,?,?);", (val,owner,item,qty,total_price,OrderStatus[0],cat,price,name,details))
        connection.commit()
    CustomerCart[val]={}
    return redirect(url_for('customerTransactions'))

@app.route('/placeOrderOffline',methods=['POST','GET'])
def placeOrderOffline():
    val=session.get('Id',None)
    global CustomerCart
    global OrderStatus
    Items=CustomerCart[val]
    key=list(Items.keys())
    item=""
    qty=""
    owner=""
    total_price=0
    cat=""
    price=""
    name=""
    details="Self PickUp"
    status="Offline Order"   
    for i in range(0,len(Items)):
        qt=Items.get(key[i])         
        item_id=key[i]
        qty=qty+qt+","
        item=item+str(item_id)+","        
        connection = sqlite3.connect("database.db")
        cur = connection.cursor()
        cur.execute("SELECT ItemPrice,ItemOwnerId,ItemName,ItemCategory,ItemPrice FROM Items WHERE ItemId=?",(item_id,))
        rows = cur.fetchall()
        total_price=total_price+(int(rows[0][0])*int(qt))
        owner=owner+str(rows[0][1])+","
        name=name+str(rows[0][2])+","
        cat=cat+str(rows[0][3])+","
        price=price+str(rows[0][4])+","
        connection.close()
    item=item[:-1]
    qty=qty[:-1]
    owner=owner[:-1]
    cat=cat[:-1]
    price=price[:-1]
    name=name[:-1]    
    with sqlite3.connect("Database.db") as connection:
        cur = connection.cursor()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        cur.execute("INSERT INTO Orders (OrderedBy,OrderedTo,ItemsOrdered,QuantityOrdered,TotalCost,Status,ItemCategory,ItemUnitPrice,ItemName,DeliveryDetails) VALUES (?,?,?,?,?,?,?,?,?,?);", (val,owner,item,qty,total_price,status,cat,price,name,details))
        connection.commit()
    CustomerCart[val]={}
    return redirect(url_for('customerTransactions'))

@app.route('/customerTransactions',methods=['POST','GET'])
def customerTransactions():
    curid =session.get('Id', None)
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute("SELECT OrderId,Status FROM Orders WHERE OrderedBy=?",(curid,))
    global OrderStatus
    rows = cur.fetchall()
    for i in range(0,len(rows)):
        status=rows[i][1]
        if(status=="Offline Order"):
            continue
        index1=OrderStatus.index(str(status))
        if(index1==len(OrderStatus)-1):
            continue
        else:
            index1+=1
            cur.execute("UPDATE Orders SET Status=? WHERE OrderId=?", (OrderStatus[index1],rows[i][0],))
            connection.commit()
    cur.execute("SELECT * FROM Orders WHERE OrderedBy=?",(curid,))
    rows = cur.fetchall()
    return render_template("CustomerTransactions.html",rows=rows) 

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form['searchvalue']
    with sqlite3.connect("Database.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM Items WHERE ItemName=?", (searchbox,))
        rows = cur.fetchall()
    distance=getlocation(rows)
    return render_template("CustomerOrder.html",rows=rows,range=range(0,len(rows),4),len=len(rows),distance=distance)

@app.route('/logout')
def logout():
    val = session.get('Id', None)
    session.pop(val, None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)        