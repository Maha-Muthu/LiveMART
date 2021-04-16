from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "E-Commerce"

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
                if rows[0][2]==password:
                    session['Id']=rows[0][0]
                    return redirect(url_for('wholesalerHome'))
                else:
                    flash('Invalid Credentials... Try Again !!')
            elif(role=="Retailer"):
                return "Retailer"
            else:
                return "Customer"
    return render_template('index.html') 

@app.route('/wholesalerHome')
def wholesalerHome():
    val =session.get('Id', None)
    connection = sqlite3.connect("database.db")
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
            itemId = request.form['itemId']
            itemName = request.form['itemName']
            itemPrice = request.form['itemPrice']
            itemQuantity = request.form['itemQuantity']
            with sqlite3.connect("Database.db") as connection:
                cur = connection.cursor()
                cur.execute("INSERT INTO Items (ItemId,ItemName,ItemPrice,ItemQuantity,ItemCategory,ItemOwnerId) VALUES (?,?,?,?,?,?);", (itemId,itemName,itemPrice,itemQuantity,itemCategory,val))
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


if __name__ == "__main__":
    app.run(debug=True)        