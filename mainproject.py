
from flask import Flask, render_template
from enviromentkeys import secret_key


app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

# manager section details bellow
@app.route("/managrDashboard")
def managrDashboard():
    return render_template("managerDashboard.html")
@app.route("/workersPage")
def workersPage():
    return render_template("workersPage.html")

@app.route("/employeeRecrutimentForm")
def employeeRecrutimentForm():
    return render_template("employeeRecrutimentForm.html")

@app.route("/targets")
def targets():
    return render_template("targetsPage.html")

@app.route("/setTargets")
def setTargets():
    return render_template("settargest.html")

@app.route("/reportOnTargets")
def reportOnTargets():
    return render_template("reports.html")

@app.route("/branches")
def branches():
    return render_template("branches.htm")

@app.route("/createBranch")
def createBranch():
    return render_template("createBranch.html")

@app.route("/branch")
def branch():
    return render_template("Abranch.html")


# credit officer dashboard section details bellow

@app.route("/crediofficerDashboard")
def crediofficerDashboard():
    return render_template("creditOfficerDashboard.html")

@app.route("/makePayment")
def makePayment():
    # not yet created
    return render_template()

@app.route("/recievablesCredit")
def recievablesCredit():
    return render_template("recievablesCredit.html")

@app.route("/recievablesSavings")
def recievablesSavings():
    return render_template("recievablesSavings.html")

@app.route("/Makepayments")
def payment():
    return render_template("payments.html")



@app.route("/collectionSheet")
def collectionSheet():
    return render_template("collectionsheet.html")

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

@app.route("/loanSecurities")
def loanSecurities():
    return render_template("loanSecurities.html")

@app.route("/savings")
def savings():
    return render_template("savings.html")

@app.route("/guranteer")
def guranteer():
    return render_template("guranteerpage.html")









if __name__ == "__main__":
    app.run(debug=True)