

from crypt import methods
from lib2to3.pygram import python_grammar_no_print_statement
from flask import Flask, cli, jsonify, redirect, render_template, request, send_file, session, url_for
from urllib3 import HTTPResponse
from enviromentkeys import secret_key
import mysql.connector as sql
import io
import os
from DatabaseClasses import AuthenticationDetails, BankingDataBase, Branches, ConnectToMySql, Deptments, EmployeeDatabase, ExistingIds, RegisterClient, ExistingAccounts
from generateAccountNumber import GenerateAccountNumber
from loginmodule import Authenticate
from generateIds import GenerateIds
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length


from flask_login import LoginManager, UserMixin, logout_user, login_required,login_user,login_remembered, current_user


app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key

"""configuring logging in functionality with the app"""
login_manager = LoginManager()
login_manager.init_app(app)

"""image secton, ensuring that client image folder is set proparly """

UPLOAD_CLIENT_PICTURES = os.path.join("static","clientpictures")
app.config["UPLOAD_CLIENT_PICTURES"] = UPLOAD_CLIENT_PICTURES
if  not os.path.exists(UPLOAD_CLIENT_PICTURES):
    os.makedirs(UPLOAD_CLIENT_PICTURES)

"""client national id pictures"""
UPLOAD_CLIENT_NATIONALid_PICTURES = os.path.join("static","clientNationalIdPictures")
app.config["UPLOAD_CLIENT_NATIONALid_PICTURES"] = UPLOAD_CLIENT_NATIONALid_PICTURES
if not os.path.exists(UPLOAD_CLIENT_NATIONALid_PICTURES):
    os.makedirs(UPLOAD_CLIENT_NATIONALid_PICTURES)

"""client business pictures"""
UPLOAD_CLIENT_BUSINESS_PICTURES = os.path.join("static", "clientBusinessPictures")
app.config["UPLOAD_CLIENT_BUSINESS_PICTURES"] = UPLOAD_CLIENT_BUSINESS_PICTURES
if not os.path.exists(UPLOAD_CLIENT_BUSINESS_PICTURES):
    os.makedirs(UPLOAD_CLIENT_BUSINESS_PICTURES)


class User(UserMixin):
    def __init__(self,id):
        super().__init__()
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)



class LoginClass(FlaskForm):
    employeeId = StringField(label="EmployeeId",validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField(label="password",validators=[DataRequired(),Length(min=3,max=30)])
    submit = SubmitField('login')



@app.route("/")
def home():
    return render_template("home.html")

# manager section details bellow

@app.route("/loginManager", methods=["GET","POST"])
def loginManager():
    form = LoginClass()
    if request.method == "POST":
        if form.validate_on_submit():
            employee_id = form.employeeId.data
            password = form.password.data
            auth = AuthenticationDetails()
            is_employee = auth.is_authenticatedEmployee(EmployeeId=employee_id,password=password)
            if is_employee:
                employee = User(employee_id)
                login_status = login_user(employee)
                if login_status:
                    session["logged_in_manager"] = employee_id
                    return redirect(url_for('managrDashboard'))
            else:
                return redirect(url_for('wrongCredentials'))

    return render_template("loginManager.html",form = form)

@login_required
@app.route("/managrDashboard")
def managrDashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("loginManager"))
    managerId = session.get("logged_in_employee")
    
    return render_template("managerDashboard.html")


@app.route("/workersPage", methods= ["GET", "POST"])
def workersPage():
    if request.method == "GET":
        try:
            requestType = request.args.get("type")
            if requestType == "employeeDetails":
                employeeObject = EmployeeDatabase()
                data = employeeObject.fetchEmployeeDetails()
                return jsonify(data)
        except Exception as e:
            raise Exception(f"error in get request under workspage route:{e}")
        


    return render_template("workersPage.html")

@app.route("/employeeRecrutimentForm", methods =["GET", "POST"])
def employeeRecrutimentForm():
    if request.method == "POST":
        try:
            if request.content_type.startswith("multipart/form-data"):
                firstName = request.form.get("firstName")
                lastName = request.form.get("lastName")
                age = request.form.get("age")
                phoneNumber = request.form.get("phoneNumber")
                email = request.form.get("email")
                current_address = request.form.get("current_address")
                district = request.form.get("district")
                city = request.form.get("city")
                village = request.form.get("village")
                Branch = request.form.get("Branch")
                dept = request.form.get("dept")
                employeeType = request.form.get("employeeType")
                roleAsigned = request.form.get("roleAsigned")
                salary = request.form.get("salary")
                profilePicture = request.files.get("profilePicture")
                documents = request.files.get("documents")
                branchId = request.form.get("branchId")
                deptId = request.form.get("deptId")
                # binalizing the documents
                
                document = documents.read()
                pic = profilePicture.read()
                

                try:
                    # existing accounts
                    ids = ExistingIds()
                    employeeIds = ids.fetchEmployeeIds()
                except Exception as e:
                    raise Exception(f"error while calling Existing Employee ids  in employee recrutiment route:{e}")

                try:
                    # generate employeeId
                    idobj = GenerateIds()
                    EmployeeId = idobj.employeeId(existingEmployeeIDs= employeeIds)

                except Exception as e:
                    raise Exception(f"error in calling generateId class under employee recrutiment  route:{e}")
                try:
                    employeeRegistrationDetails = {
                        "id":EmployeeId,
                        "firstName":firstName,
                        "lastName":lastName,
                        "age":int(age),
                        "phoneNumber":phoneNumber,
                        "email":email,
                        "current_address":current_address,
                        "district":district,
                        "city":city,
                        "village":village,
                        "Branch":Branch,
                        "dept":dept,
                        "deptId":deptId,
                        "employeeType":employeeType,
                        "roleAsigned":roleAsigned,
                        "salary":int(salary),
                        "documents":document,
                        "branchId":branchId,
                        "profilePicture":pic
                        
                    }
                    # insert details into employee database
                    try:
                        employeeObject = EmployeeDatabase()
                        employeeObject.insert_into_tables(employeeDetails=employeeRegistrationDetails)
                    except Exception as e:
                        raise Exception(f"error while calling insert into table methd of employee database in employee recrutiment route:{e}")

                except Exception as e:
                    raise Exception(f"error while calling employee database in employee form route:{e}")
                
                return jsonify({"response":"success"})

            elif request.content_type.startswith("application/json"):
                requesttype = request.json.get("type")
                if requesttype == "employeebranchUpdte":
                    data = request.json.get("data")
                    try:
                        employeeObj = EmployeeDatabase()
                        employeeObj.updateEmployeeBranch(detailsObject=data)
                    except Exception as e:
                        raise Exception(f"error while updating employee branch details:{e}")
                    return jsonify({"response":"successful"})
                elif requesttype == "employeeDeptmentUpdte":
                    data = request.json.get("data")
                    employeeObjct = EmployeeDatabase()
                    employeeObjct.updateEmployeeDept(detailsObject=data)
                    return jsonify({"response":"success"})

        except Exception as e:
            raise Exception(f"multi part post request error:{e} ")
    else:
        requesttype = request.args.get("type")
        if requesttype == "branchDetails":
            try:
                brachObj = Branches()
                branchDetails = brachObj.fetch_branch_details()
                return jsonify(branchDetails)
            except Exception as e:
                raise Exception(f"error while calling fetch branch details in the employee recrutiment form route:{e}")
        elif requesttype == "getDeptdetails":
            try:
                deptdetails = Deptments()
                deptdata = deptdetails.fetch_existingDeptment()
                return jsonify(deptdata)
            except Exception as e:
                raise Exception(f"error while loading deptment detail class in create dept route:{e}")
            


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

@app.route("/branches", methods=["GET","POST"])
def branches():
    """this api sends fetch and sends data to be displayed on branches route"""
    if request.method == "GET":
        requestType = request.args.get("type")
        if requestType == "branchDetails":
            branchObj = Branches()
            data = branchObj.fetch_branch_details()
            return jsonify(data)
        elif requestType == "numberOfBranches":
            branchObj = Branches()
            numberOfBranches = branchObj.numberOfBranches()
            return jsonify(numberOfBranches)
    return render_template("branches.htm")



@app.route("/createBranch", methods =["GET", "POST"])
def createBranch():
    if request.method == "POST":
        requesttype = request.json.get("type")
        if requesttype  and requesttype == "branchCreation":
            Branch_data = request.json.get("data")
            try:
                # getting existing ids
                existingIdz = ExistingIds()
                existId = existingIdz.fetchBranchIds()
            except Exception as e:
                raise Exception(f"error while calling existing ids class in create brach route:{e}")
            try:
                # generating branch Id
                idObject = GenerateIds()
                branchId = idObject.branchId(existingBranchIDs=existId)
                Branch_data["branchId"] = branchId

            except Exception as e:
                raise Exception(f" error while calling generate branch id in create branch route: {e}")
            try:
                # inserting into branch database
                obj = Branches()
                obj.insert_into_tables(branchObject=Branch_data)
                # print(Branch_data)
            except Exception as e:
                raise Exception(f"error while inserting into branch database:{e}")
            
        return jsonify({"response":"success"})
    return render_template("createBranch.html")

@app.route("/updateEmployeeDept")
def updateEmployeeDept():
    return render_template("updateEmployeeDept.html")


@app.route("/createDeptments", methods =["GET", "POST"])
def createDeptments():
    if request.method == "POST":
        requestType = request.json.get("type")
        if requestType == "deptCreation":
            data = request.json.get("data")
            try:
                # getting existing dept id
                existingDeptObj = Deptments()
                ids = existingDeptObj.existingDeptIdz()
            except Exception as e:
                raise Exception(f"error while calling existing deptm ent class in create deptment route:{e}")
            try:
                # generate dept id
                idObj = GenerateIds()
                deptIdz = idObj.deptmentId(existingDeptIds=ids)
                data["DeptId"] = deptIdz
            except Exception as e:
                raise Exception(f"error while generating dept id in create dept route:{e}")
            try:
                # insert into dept database
                DeptObj = Deptments()
                DeptObj.insert_into_tables(deptObject=data)
            except Exception as e:
                raise Exception(f"error while calling insert into dept database in create deptment:{e}")
            return jsonify({"response":"succuse"})
    else:
        pass
        
    return render_template("createDeptments.html")

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

@app.route("/underWritter", methods=["GET","POST"])
def underWritter():
    if request.method == "GET":
        requesttype = request.args.get("type")
        if requesttype == "loandetails":
            bankObj = BankingDataBase()
            data = bankObj.fetchLoanApplicationDetails()
            # print(data)
            return jsonify(data)
    elif request.method == "POST":
        requesttype = request.json.get("type")
        if requesttype == "approvedloan":
            data = request.json.get("data")
            try:
                banking = BankingDataBase()
                banking.updateLoanApplicationApprovalStatus(loanApprovalDetails=data)
                banking.loanApplicationApprovelTrigger()
                
            except Exception as e:
                raise Exception(f"eror while approving loan application in under writer's route:{e}")
            return jsonify({"response":"loan approved"})

    
    return render_template("underWritter.html")


@app.route("/recievableReports")
def recievableReports():
    return render_template("recievableReports.html")

@app.route("/disburshmentReports", methods=["GET", "POST"])
def disburshmentReports():
    if request.method == "GET":
        requestType = request.args.get("type")
        if requestType == "loanApprovedDetails":
            banking = BankingDataBase()
            data = banking.fetchApprovedLoandetails()
            return jsonify(data)
    else:
        requestType = request.json.get("type")
        if requestType == "confirmedLoan":
            loanid = request.json.get("data")
            if loanid:
                try:
                    banking = BankingDataBase()
                    banking.insert_into_disbursement_table(loanId=loanid)
                    banking.registeredLoanTriger()
                except Exception as e:
                    raise Exception(f"error while calling insert into disursement table method :{e}")
            return jsonify({"response":"LoanConfirmed"})
    return render_template("disburshmentReports.html")

@app.route("/attatchEmployeeTobranch")
def attatchEmployeeTobranch():
    return render_template("attatchEmployeeTobranch.html")

@app.route("/employeeProfile", methods=["GET", "POST"])
def employeeProfile():
    if request.method == "POST":
        requestType = request.json.get("type")
        if requestType == "employeeId":
            employeeId = request.json.get("data")
            session["employeeDetailsToLoad"] = employeeId
            return jsonify({"response":"success"})
        elif requestType == "resetpassword":
            resetDetails = request.json.get("data")
            Eid = resetDetails["employeeId"]
            pwd = resetDetails['password']
            authent_obj = AuthenticationDetails()
            authent_obj.update_EmployeePassword(employeeId=Eid, password=pwd)
            return jsonify({"message":"successfuly"})
    elif request.method == "GET":
        requestType = request.args.get("type")
        if requestType == "employeeDetails":
            try:
                employeeId = session.get("employeeDetailsToLoad")
                employeeObject = EmployeeDatabase()
                details = employeeObject.fetchSpecificEmployeeDetails(employeeId=employeeId)
                return jsonify(details)
            except Exception as e:
                raise Exception(f"error while calling specified employee methode :{e}")
        elif requestType == "employeePic":
            try:
                employeeId = session.get("employeeDetailsToLoad")
                employeeobject = EmployeeDatabase()
                picInBinary = employeeobject.fetchSpecificEmployeeMataDataPictures(employeeId=employeeId)
                return send_file(
                    io.BytesIO(picInBinary),
                    mimetype="image/jpeg",
                    as_attachment=False
                )

                # print(filepic)
            except Exception as e:
                raise Exception(f" error while calling employee pic method: {e}")
        elif requestType == "accademicDocument":
            try:
                employeeId = session.get("employeeDetailsToLoad")
                employeeobject = EmployeeDatabase()
                document = employeeobject.fetchSpecificEmployeeMataDataDocument(employeeId=employeeId)
                return send_file(
                    io.BytesIO(document),
                    mimetype="application/pdf",
                    as_attachment=False
                )
            except Exception as e:
                raise Exception(f"error while calling fetchSpecificEmployeeMataDataDocument method:{e}")

    return render_template("employeeProfile.html")


@app.route("/authenticationSetting",methods=["GET","POST"])
def authenticationSetting():
    if request.method == "POST":
        data = request.json
        try:
            obj = AuthenticationDetails()
            obj.insert_into_employeeLoginCridentials(loginDetails=data)
            return jsonify({"response":"details recieved"})
        except Exception as e:
            raise Exception(f"error while calling insert into employee login crediential methode in authentication route:{e}")
    return render_template("authenticationSetting.html")



# credit officer dashboard section details bellow

@app.route("/loginEmployess", methods=["GET","POST"])
def loginEmployess():
    form = LoginClass()
    if request.method == "POST":
        if form.validate_on_submit():
            employee_id = form.employeeId.data
            password = form.password.data
            auth = AuthenticationDetails()
            is_employee = auth.is_authenticatedEmployee(EmployeeId=employee_id,password=password)
            if is_employee:
                employee = User(employee_id)
                login_status = login_user(employee)
                if login_status:
                    session["logged_in_employee"] = employee_id
                    return redirect(url_for('crediofficerDashboard'))
            else:
                return redirect(url_for('wrongCredentials'))

    return render_template("login.html",form = form)

@app.route("/wrongCredentials")
def wrongCredentials():
    return render_template("wrongCredentials.html")

@app.route("/resetpassword")
def resetpassword():
    return render_template("resetpassword.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@login_required
@app.route("/crediofficerDashboard", methods=["GET"])
def crediofficerDashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('loginEmployess'))
    
    officerId = current_user.id
    if request.method == "GET":
        Bank = BankingDataBase()
        requestType = request.args.get("type")
        if requestType == "ForSpecificEmployee":
                collectionSheetDetails = Bank.fetchCollectionSheetDetails(employeeId=officerId)
                return jsonify(collectionSheetDetails)
        elif requestType == "portifolio":
            portifolio = Bank.fetch_officerCurrentPortifolio(officerID=officerId)
            return jsonify(portifolio)
        elif requestType == "credit":
            data = Bank.fetchDebtedLoanAccountDetailForSpecificOfficer(officerId=officerId)
            
            return jsonify(data)
        if requestType== "savings":
            data = Bank.fetch_ClientsInvestmentDetailsForSpecficEmployee(EmployeeId=officerId)
            
            return jsonify(data)
        
    
    return render_template("creditOfficerDashboard.html")

@app.route("/registerClient",methods =["GET","POST"])
def registerClient():
    if request.method == "POST":
        officer_id = current_user.id
        branchDetails = EmployeeDatabase()
        branchDetails = branchDetails.fetchEmployeeBranchdetails(employeeId=officer_id)
        branchId = branchDetails[0]
            
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
                
                # next of kin details
                nextOfKinFirstName = request.form.get("nextOfKinFirstName")
                nextOfKinSirName = request.form.get("nextOfKinSirName")
                nextOfKinPhone = request.form.get("nextOfKinPhone")
                nextOfKinLocation = request.form.get("nextOfKinLocation")
                # pictures
                ownerPic = request.files.get("ownerPic")
                NationalIdpic = request.files.get("idpic")
                if ownerPic:
                    extension = os.path.splitext(ownerPic.filename)[1]
                    filename = f"{account_number}{extension}"
                    filePath = os.path.join(app.config["UPLOAD_CLIENT_PICTURES"],filename)
                    ownerPic.save(filePath)
                    ownerpic_relative_file_path = os.path.join("clientpictures",filename)
                if NationalIdpic:
                    id_extension = os.path.splitext(NationalIdpic.filename)[1]
                    idFilename = f"{account_number}{id_extension}"
                    idfilePath = os.path.join(app.config["UPLOAD_CLIENT_NATIONALid_PICTURES"], idFilename)
                    NationalIdpic.save(idfilePath)
                    ownernatioanlID_relative_file_path = os.path.join("clientNationalIdPictures", idFilename)


                AccountDetailsObj = {
                    "AccountNumber":account_number,
                    "FirstName":firstName,
                    "Sirname":sirName,
                    "PhoneNumber":phonenumber,
                    "DateOfBirth":dateOfBirth,
                    "Gender":gender,
                    "Religion":religion,
                    "NinNumber":ninNumber,
                    "CurrentAddress":address,
                    "CityDivision":city,
                    "District":state,
                    "OwnerPic":ownerpic_relative_file_path,
                    "NationalIdPic":ownernatioanlID_relative_file_path,

                    "NextKinDetails": {
                    "nextOfKinFirstName":nextOfKinFirstName,
                    "nextOfKinSirName": nextOfKinSirName,
                    "PhoneNumber": nextOfKinPhone,
                    "Location":nextOfKinLocation},

                    "BranchDetails":{
                        "BranchId":branchId,
                        "OfficerId":officer_id
                    }
                }
                

                registerAccount = BankingDataBase()
                registerAccount.insert_into_accountTable(accountObject=AccountDetailsObj)

                
                
                return jsonify({"response": "success"})
            else:
                return jsonify({"response":"un surported formate"})    
        except Exception as e:
            raise  Exception(f"error in register post request:{e}")
        
    
    return render_template("registerClient.html")




@app.route("/recievablesCredit", methods=["GET","POST"])
def recievablesCredit():
    if request.method == "GET":
        officerId = current_user.id
        bank = BankingDataBase()
        requesttype = request.args.get("type")
        if requesttype == "credit":
            data = bank.fetchDebtedLoanAccountDetailForSpecificOfficer(officerId=officerId)
            return jsonify(data)
    return render_template("recievablesCredit.html")

@app.route("/recievablesSavings", methods=["GET","POST"])
def recievablesSavings():
    if request.method == "GET":
        officerId = current_user.id
        bank = BankingDataBase()
        requesttype = request.args.get("type")
        if requesttype == "savings":
            data = bank.fetch_ClientsInvestmentDetailsForSpecficEmployee(EmployeeId=officerId)
            return jsonify(data)

    return render_template("recievablesSavings.html")

@app.route("/Makepayments", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        paymenttype = request.json.get("type")
        if paymenttype == "loanpayment":
            session["loanId"] = request.json.get("loanId")
            return jsonify({"response":"recieved"})
        elif paymenttype == "amount":
            amount = request.json.get("amount")
            loanId = session.get("loanId")
            paymentDetails = {"loanId":loanId,"amount":amount}
            bank = BankingDataBase()
            bank.insert_into_ClientsLOANpaymentDETAILS(paymentDetails=paymentDetails)
            bank.loanPaymenttrigger()
            # changing activate status from a default unfinshed to finshed if current portifolio is 0
            bank.changeLoanRegistrationStatusTrigger()
            return jsonify({"response":"recieved"})
            


    return render_template("payments.html")


@app.route("/Investmentpayments", methods=["GET", "POST"])
def Investmentpayments():
    if request.method == "POST":
        banking = BankingDataBase()
        postType = request.json.get("type")
        if postType == "investment":
            accountNumber = request.json.get("accountnumber")
            session["client_Account_Number"] = accountNumber
            return jsonify({"response":"recieved"})
        elif postType == "amount":
            accountNumber = session.get("client_Account_Number")
            amount = request.json.get("amount")
            banking.insert_into_ClientsInvestmentPaymentDetails(AccountNumber=accountNumber,amount=amount)
            return jsonify({"response":"recieved"})
    
    return render_template("investmentPayment.html")

@app.route("/succefulpayments")
def successfulpayment():
    return render_template("successfulPayment.html")


@app.route("/loanApplication", methods=["GET", "POST"])
def loanApplication():
    if request.method == "POST":
        if request.content_type.startswith("multipart/form-data"):
            officer_id = current_user.id
            branchDetails = EmployeeDatabase()
            branchDetails = branchDetails.fetchEmployeeBranchdetails(employeeId=officer_id)
            branchId = branchDetails[0]
            
            # get loan application details
            try:
                clientId = request.form.get("clientId")
                loanAmount = request.form.get("loanAmount")
                interesRate = request.form.get("interestRate")
                loanPeriod = request.form.get("loanPeriod")
                clientCurrentaddress = request.form.get("clientCurrentaddress")
                devisioncity = request.form.get("devisioncity")
                state = request.form.get("state")
                Occuption = request.form.get("Occuption")
                workArea = request.form.get("workArea")
                businessLoaction = request.form.get("businessLoaction")
                contact = request.form.get("contact")
                businessPic = request.files.get("businessPic")

                if businessPic:
                    pic_fullName = os.path.splitext(businessPic.filename)
                    imagename = pic_fullName[0]
                    extension = pic_fullName[1]
                    pictureName = f"{clientId}{imagename}{extension}"
                    businessPicPath = os.path.join(app.config["UPLOAD_CLIENT_BUSINESS_PICTURES"],pictureName)
                    businessPic.save(businessPicPath)

                    businessPictureRelativePath = os.path.join("clientBusinessPictures",pictureName)

                # accessing existing 
                try:

                    loanIdObject = ExistingIds()
                    existingLoanIds = loanIdObject.fetchLoanIds()
                    
                except Exception as e:
                    raise Exception(f"error while calling existing loan ids in loan application route:{e}")

                try:
                    idObj = GenerateIds()
                    loanId = idObj.loanId(existingLoanIds=existingLoanIds)
                except Exception as e:
                    raise Exception(f"error while calling generate loanId method in loanapplication route:{e}")

                
                # data object
                loanApplicationObject ={
                    "loanID":loanId,
                    "clientId":clientId,
                    "loanAmount":loanAmount,
                    "interestRate":interesRate,
                    "loanPeriod":loanPeriod,
                    "clientCurrentaddress":clientCurrentaddress,
                    "devisioncity":devisioncity,
                    "state":state,
                    "Occuption":Occuption,
                    "workArea":workArea,
                    "businessLoaction":businessLoaction,
                    "contact":contact,
                    "businessPictureRelativePath":businessPictureRelativePath,
                    "BranchDetails":{
                        "BranchId":branchId,
                        "OfficerId":officer_id
                    }
                }
                loan = BankingDataBase()
                loan.insert_into_loanApplicationTAbles(loanApplicationDetails=loanApplicationObject)
                return jsonify({"response":"loan application recieved"})
            except Exception as e:
                raise Exception(f"error while recieving loan application details in loanapplication route:{e}")
        else:
            pass
    else:
        pass   

    return render_template("loanApplication.html")

@app.route("/collectionSheet", methods =["GET"])
def collectionSheet():
    if request.method == "GET":
        officerId = current_user.id
        Bank = BankingDataBase()
        requestType = request.args.get("type")
        if requestType == "ForSpecificEmployee":
            collectionSheetDetails = Bank.fetchCollectionSheetDetails(employeeId=officerId)
            return jsonify(collectionSheetDetails)
    return render_template("collectionsheet.html")

@app.route("/overdueAndPenalties")
def overdueAndPenalties():
    return render_template("overdue_penalty.html")

@app.route("/allClientList", methods=["GET","POST"])
def allClientList():
    if request.method == "GET":
        officer_id = current_user.id
        requesttype = request.args.get("type")
        if requesttype == "allclientslist":
            try:
                clientObject = BankingDataBase()
                data = clientObject.fetchAllClientAccountDetailsForSpecificEmployee(employeeId=officer_id)
                return jsonify(data)
            except Exception as e:
                raise Exception(f"error while calling fetchEmployeeDetails method in allclient route:{e}")

    return render_template("allclientslist.html")

@app.route("/ActiveClients", methods=["GET","POST"])
def ActiveClients():
    if request.method ==  "GET":
        bank = BankingDataBase()
        employeeId = current_user.id
        requestType = request.args.get("type")
        if requestType == "activeLoan":
            data = bank.fetchClientAccountDetailsWithActivateLoanForSpecificEmployee(employeeId=employeeId)
            return jsonify(data)
            
    return render_template("activeClients.html")

@app.route("/onHoldClients",methods=["GET","POST"])
def onHoldClients():
    if request.method == "GET":
        bank = BankingDataBase()
        employeeId = current_user.id
        requestTyep = request.args.get("type")
        if requestTyep == "finshedLoans":
            data = bank.fetchClientAccountDetailsWithFinshedLoanForSpecificEmployee(employeeId=employeeId)
            return jsonify(data)

    return render_template("onhold.html")

@app.route("/clientProfile",methods=["GET","POST"])
def clientProfile():
    if request.method == "POST":
        requesttype = request.json.get("type")
        if requesttype == "clientID":
            id = request.json.get("data")
            session["lorded_account"] = id
            return jsonify({"response":"clientId"})
    elif request.method == "GET":
        bank = BankingDataBase()
        client_id = session.get("lorded_account")
        requesttype = request.args.get("type")
        if requesttype == "clientDetails":
            """fetching clients personal details"""
            clientDetails = bank.fetchSpecificClientAccountDetails(clientId=client_id)
            return clientDetails
        elif requesttype == "clientCreditdetails":
            """fetching clients credit details"""
            creditDetails = bank.fetchClientCreditDetails(clientId=client_id)
            return creditDetails 
        elif requesttype == "clientPortifolio":
            """fetching client's current portifolio"""
            portifolio = bank.fetch_clientsCurrentPortifolio(clientId=client_id)
            return jsonify({"portifolio":portifolio})
        elif requesttype == "clientLoanSecurity":
            """fetch client's loan security"""
            loan_security = bank.fetchClientLoanSecurityDetails(clientId=client_id)
            return jsonify(loan_security)
        elif requesttype == "investments":
            investments = bank.fetch_ClientsInvestmentDetails(AccountNumber=client_id)
            return jsonify(investments)

            
            
    return render_template("clientProfilePage.html")

@app.route("/clientpaymentDetails", methods =["GET","POST"])
def clientpaymentDetails():
    if request.method == "GET":
        clientId = session.get("lorded_account")
        requesttype = request.args.get("type")
        if requesttype == "payementDetails":
            bank = BankingDataBase()
            data = bank.fetchClientCurrentLoanPaymentDetails(clientId=clientId)
            
            return jsonify(data)
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