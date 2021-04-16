from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "Project"

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/logged',methods=['POST','GET'])

def logged():
    if request.method=='POST':
        uname=request.form['Username']
        password=request.form['pass']
        with sqlite3.connect('Database.db') as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM  Wholesalers WHERE username=?", (uname,))
            rows=cur.fetchall();
            if rows[0][1]==password:
                session['username']=request.form['Username']
                return "Hello World"

            else:
                flash('* Invalid Credentials... Try Again !!')
                return "Bye World"
    else:
        return render_template('index.html')

@app.route('/WholesalerUpdateItem',methods=['POST','GET'])

def WholesalerUpdateItem():
    if request.method == 'POST':
        try:
            itemCategory = request.form['itemCategory']
            itemId = request.form['itemId']
            itemName = request.form['itemName']
            itemPrice = request.form['itemPrice']
            itemQuantity = request.form['itemQuantity']
            with sqlite3.connect("Database.db") as connection:
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