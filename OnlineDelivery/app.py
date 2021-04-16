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
                if rows[0][1]==password:
                    session['username']=request.form['Username']
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
    val =session.get('username', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerHome.html")

@app.route('/wholesalerAddItem',methods=['POST','GET'])
def wholesalerAddItem():
    val =session.get('username', None)
    connection = sqlite3.connect("database.db")
    return render_template("WholesalerUpload.html")


@app.route('/wholesalerUpdateItem',methods=['POST','GET'])
def wholesalerUpdateItem():
    if request.method == 'POST':
        try:
            itemCategory = request.form['itemCategory']
            itemId = request.form['itemId']
            itemName = request.form['itemName']
            itemPrice = request.form['itemPrice']
            itemQuantity = request.form['itemQuantity']
            with sqlite3.connect("Database.db") as connection:
                cur = connection.cursor()
                cur.execute("INSERT INTO Items (ItemId,ItemName,ItemPrice,ItemQuantity,ItemCategory) VALUES (?,?,?,?,?);", (itemId,itemName,itemPrice,itemQuantity,itemCategory))
                connection.commit()
                return "Inserted"
        except:
            connection.rollback()
            return "Failed"
        finally:
            connection.close()
    return "EXIT"


if __name__ == "__main__":
    app.run(debug=True)        