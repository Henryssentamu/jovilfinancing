
from ast import Pass
from crypt import methods
from flask import Flask, jsonify, render_template, request
from enviromentkeys import secret_key
import mysql.connector as sql

from DatabaseClasses import ConnectToMySql, RegisterClient, ExistingAccounts
from generateAccountNumber import GenerateAccountNumber


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

@app.route("/createBranch", methods =["GET", "POST"])
def createBranch():
    if request.method == "POST":
        requesttype = request.json.get("type")
        # print(f"here is the fa: {requesttype}")
        if requesttype  and requesttype == "branchCreation":
            data = request.json.get("data")
            print(data)
        return jsonify({"response":"success"})
    return render_template("createBranch.html")

@app.route("/branch")
def branch():
    return render_template("Abranch.html")
@app.route("/mergeBranches")
def mergeBranches():
    return render_template("mergebranches.html")
@app.route("/credit")
def credit():
    return render_template("credit.html")

@app.route("/creditCollection")
def creditCollection():
    return render_template("creditCollections.html")

@app.route("/creditbalance")
def creditbalance():
    return render_template("creditBalances.html")

@app.route("/collectionCreditOverdue")
def collectionCreditOverdue():
    return render_template("collectionCreditOverdue.html")

@app.route("/collectionCreditpenalties")
def collectionCreditpenalties():
    return render_template("collectionCreditPenalities.html")


@app.route("/savingsgeneral")
def savingsgeneral():
    return render_template("savingsgeneral.html")

@app.route("/savingCollections")
def savingCollections():
    return render_template("savingCollections.html")

@app.route("/savingAtMaturity")
def savingAtMaturity():
    return render_template("savingAcountsAtMaturity.html")


@app.route("/recievableReports")
def recievableReports():
    return render_template("recievableReports.html")
@app.route("/disburshmentReports")
def disburshmentReports():
    return render_template("disburshmentReports.html")

@app.route("/attatchEmployeeTobranch")
def attatchEmployeeTobranch():
    return render_template("attatchEmployeeTobranch.html")

@app.route("/employeeProfile")
def employeeProfile():
    return render_template("employeeProfile.html")


# credit officer dashboard section details bellow

@app.route("/crediofficerDashboard")
def crediofficerDashboard():
    return render_template("creditOfficerDashboard.html")

@app.route("/registerClient",methods =["GET","POST"])
def registerClient():
    if request.method == "POST":
        # get registered accounts
        try:
            obj = ExistingAccounts()
            existing_accounts = obj.fetchAccounts()
        except Exception as e:
            raise Exception(f"error while getting accounts: {e}")
        # generate accounts
        try:
            account = GenerateAccountNumber(existingAccounts=existing_accounts )
            account_number = account.generateNumber()
        except Exception as e:
            raise Exception(f"error while calling generate account number:{e}")
        try:                     
            if request.content_type.startswith('multipart/form-data'):
                
                # Retrieve text form fields
                firstName = request.form.get("firstName")
                sirName = request.form.get("sirName")
                dateOfBirth = request.form.get("dateOfBirth")
                religion = request.form.get("religion")
                gender = request.form.get("gender")
                ninNumber = request.form.get("ninNumber")
                phonenumber = request.form.get("phonenumber")
                address = request.form.get("address")
                city = request.form.get("city")
                state = request.form.get("state")
                nextKinFullNames = request.form.get("nextofKinName")
                nextOfKinPhone = request.form.get("nextOfKinPhone")
                nextOfKinNin = request.form.get("nextOfKinNin")
                nextOfKinLocation = request.form.get("nextOfKinLocation")
                ownerPic = request.files.get("ownerPic")
                ownerPic_binary = ownerPic.read()

                registrationObj = {
                    "AccountNumber":account_number,
                    "FirstName":firstName,
                    "Sirname":sirName,
                    "PhoneNumber":phonenumber,
                    "DateOfBirth":dateOfBirth,
                    "Gender":gender,
                    "Religion":religion,
                    "NinNumber":ninNumber,
                    "PermanentAddress_village":address,
                    "City_Devission":city,
                    "District":state,
                    "OwnerPic":ownerPic_binary,

                    "NextKinDetails": {
                    "NinNumber":nextOfKinNin ,
                    "FullName": nextKinFullNames,
                    "PhoneNumber": nextOfKinPhone,
                    "Location":nextOfKinLocation},

                    "BranchDetails":{
                        "BranchId":"bi123",
                        "OfficerId":"Ei123"
                    }
                }
                

                # store registered client
                ac = RegisterClient(dataObject = registrationObj)
                ac.create_Database()
                ac.create_tables()
                ac.insert_into_tables()

                
                
                return jsonify({"response": "success"})
            else:
                return jsonify({"response":"un surported formate"})    
        except Exception as e:
            raise  Exception("error in register post request:{e}")
        
    
    return render_template("registerClient.html")



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

@app.route("/loanApplication")
def loanApplication():
    return render_template("loanApplication.html")

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