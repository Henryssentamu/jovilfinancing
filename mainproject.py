
from flask import Flask, render_template
from enviromentkeys import secret_key


app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key




@app.route("/crediofficerDashboard")
def crediofficerDashboard():
    return render_template("creditOfficerDashboard.html")

@app.route("/makePayment")
def makePayment():
    # not yet created
    return render_template()

@app.route("/recievables")
def recievables():
     # not yet created
    return render_template()
@app.route("/collectionSheet")
def collectionSheet():
     # not yet created
    return render_template()

@app.route("/overdueAndPenalties")
def overdueAndPenalties():
    return render_template("overdue_penalty.html")

@app.route("/allClientList")
def allClientList():
    return render_template("allclientslist.html")

@app.route("/ActiveClients")
def ActiveClients():
    return render_template("activeClients.html")

@app.route("/onHoldClients")
def onHoldClients():
    return render_template("onhold.html")

@app.route("/clientProfile")
def clientProfile():
    return render_template("clientProfilePage.html")

@app.route("/clientpaymentDetails")
def clientpaymentDetails():
    return render_template("clientPaymentDetails.html")

@app.route("/clientOverdueAndPenalties")
def clientOverdueAndPenalties():
    return render_template("clients_overdue_penalties.html")







if __name__ == "__main__":
    app.run(debug=True)