
from datetime import datetime,time
from pickle import TRUE
import mysql.connector as sql
from generateIds import GenerateIds




class ConnectToMySql:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection  = sql.connect(
                host= "localhost",
                user="root",
                password="Hen#@3030"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            else:
                raise Exception("Failed to establish connection to MySQL.")
        except sql.Error as err:
            raise Exception(f"Error while connecting to MySQL: {err}")
        
    def reconnect_if_needed(self):
        if not self.connection.is_connected():
            self.connect()
            
       
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    

class RegisterClient(ConnectToMySql):
    def __init__(self, dataObject):
        super().__init__()
        self.data = dataObject
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")

    def create_Database(self):
        try:
            if self.cursor:
                self.cursor.execute("""
                    CREATE DATABASE IF NOT EXISTS AccountsVault
                """)
            else:
                raise Exception("Cursor is not available.")
        except Exception as e:
            raise Exception(f"Error in create_Database: {e}")

    def create_tables(self):
        if self.cursor:
            try:
                # selecting database to querry 
                self.cursor.execute("USE AccountsVault")

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS AccountOwner(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) PRIMARY KEY,
                        FirstName VARCHAR(500),
                        Sirname VARCHAR(500)              
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ContactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        PhoneNumber VARCHAR(200),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL              
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS socialDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        DateOfBirth  VARCHAR(100),
                        Gender VARCHAR(50),
                        Religion VARCHAR(200),
                        NinNumber VARCHAR(500),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)  ON DELETE SET NULL     
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS AddressDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        PermanentAddress_village TEXT,
                        City_Devission TEXT,
                        District TEXT,  
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        NinNumber VARCHAR(500),
                        FullName VARCHAR(500),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)  ON DELETE SET NULL                                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinContactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        PhoneNumber VARCHAR(100),
                        Location VARCHAR(200),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL              
                    )
                """)

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pictures(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        OwnerPic LONGBLOB NOT NULL,
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL
                        
                    )   
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS branchDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500) NULL,
                        BranchId VARCHAR(500),
                        OfficerId VARCHAR(500),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL
                                                
                    )
                """)
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while creating tables in Account class table: {e} ")
            finally:
                self.close_connection()
        else:
            raise Exception("Cursor is not available to create tables.")
        
    def insert_into_tables(self):
        self.AccountNumber = self.data["AccountNumber"]
        self.FirstName = self.data["FirstName"]
        self.Sirname = self.data["Sirname"]
        self.PhoneNumber = self.data["PhoneNumber"]
        self.DateOfBirth = self.data["DateOfBirth"]
        self.Gender = self.data["Gender"]
        self.Religion = self.data["Religion"]
        self.Ninnumber = self.data["NinNumber"]
        self.PermanentAddress_village = self.data["PermanentAddress_village"]
        self.City_Devission = self.data["City_Devission"]
        self.District = self.data["District"]
        self.OwnerPic = self.data["OwnerPic"]

        """ next of kin details """
        self.nextKin_details = self.data["NextKinDetails"]
        self.nextKinNinNumber = self.nextKin_details["NinNumber"]
        self.nextkinFullName = self.nextKin_details["FullName"]
        self.nextKinPhoneNumber = self.nextKin_details["PhoneNumber"]
        self.nextKinLocation  = self.nextKin_details["Location"]
        

        """ Branch details """
        self.branchDetails = self.data["BranchDetails"]
        self.BranchId = self.branchDetails["BranchId"]
        self.OfficerId = self.branchDetails["OfficerId"]


        # reconnecting to database 
        self.reconnect_if_needed()

        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")

                self.cursor.execute("""
                    INSERT INTO AccountOwner(
                        AccountNumber,
                        FirstName,
                        Sirname
                        ) VALUES(%s,%s,%s)
                """,(self.AccountNumber,self.FirstName,self.Sirname))

                self.cursor.execute("""
                    INSERT INTO ContactDetails(
                        AccountNumber,
                        PhoneNumber
                        ) VALUES (%s, %s)
                """,(self.AccountNumber,self.PhoneNumber))
                self.cursor.execute("""
                    INSERT INTO socialDetails(
                        AccountNumber,
                        DateOfBirth,
                        Gender,
                        Religion,
                        NinNumber
                    ) VALUES(%s,%s,%s,%s,%s)
                """,(self.AccountNumber,self.DateOfBirth, self.Gender,self.Religion,self.Ninnumber))
                self.cursor.execute("""
                    INSERT INTO AddressDetails(
                        AccountNumber,
                        PermanentAddress_village,
                        City_Devission,
                        District                
                    ) VALUES(%s,%s,%s,%s)
                """,(self.AccountNumber,self.PermanentAddress_village,self.City_Devission,self.District))
                self.cursor.execute("""
                    INSERT INTO NextOfKinDetails(
                        AccountNumber,
                        NinNumber,
                        FullName                
                    ) VALUES (%s,%s,%s)
                """,(self.AccountNumber,self.nextKinNinNumber,self.nextkinFullName ))
                self.cursor.execute("""
                    INSERT INTO NextOfKinContactDetails(
                        AccountNumber,
                        PhoneNumber,
                        Location                    
                    ) VALUES(%s,%s,%s)
                """,(self.AccountNumber,self.nextKinPhoneNumber,self.nextKinLocation))

                self.cursor.execute("""
                    INSERT INTO pictures(
                        AccountNumber,
                        OwnerPic              
                    ) VALUES(%s,%s)
                """,(self.AccountNumber,self.OwnerPic ))
                self.cursor.execute("""
                    INSERT INTO branchDetails(
                        AccountNumber,
                        BranchId,
                        OfficerId                   
                    )VALUES(%s,%s,%s)
                """,(self.AccountNumber, self.BranchId, self.OfficerId))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while inserting into specified table: {e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor is not available to insert into tables")

        
    def update_phoneNumber(self):

        self.accountNumber = self.data["accountNumber"]
        self.phoneNumber = self.data["phoneNumber"]

        # reconnect to database 
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                update_query = """
                        UPDATE ContactDetails
                        SET PhoneNumber = %s
                        WHERE AccountNumber = %s
                    """
                self.cursor.execute(update_query, (self.phoneNumber ,self.accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating phone numer:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not availabe to update phone number:")
        
    def update_AddressDetails(self):

        self.accountNumber = self.data["accountNumber"]
        self.PermanentAddress = self.data["PermanentAddress"]
        self.CityDevission = self.data["CityDevission"]
        self.District = self.data["District"]

        # reconnect to database 
        self.reconnect_if_needed()

        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                update_query = """
                        UPDATE AddressDetails
                        SET PermanentAddress_village = %s,City_Devission = %s,District = %s
                        WHERE AccountNumber = %s

                    """
                self.cursor.execute(update_query, (self.PermanentAddress,self.CityDevission, self.District, self.accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating address details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not availabe to update phone number:")
        
    def update_nextOfKin(self):
        self.fullname  = self.data["fullname"]
        self.Ninnumber = self.data["Ninnumber"]
        self.PhoneNumber = self.data[" PhoneNumber"]
        self.Location = self.data["Location"]
        self.accountNumber = self.data["accountNumber"]

        # reconnect to database 
        self.reconnect_if_needed()

        if self.cursor:
            try:
                self.cursor.execute(" USE AccountsVault")
                name_querry = """
                    UPDATE NextOfKinDetails
                    SET FullName  = %s, NinNumber = %s
                    WHERE
                        AccountNumber = %s
                """

                contact_querry = """
                    UPDATE NextOfKinContactDetails
                    SET  PhoneNumber = %s,Location = %s
                    WHERE
                        AccountNumber = %s

                """
                self.cursor.execute(name_querry,(self.fullname,self.Ninnumber, self.accountNumber))
                self.cursor.execute(contact_querry,(self.PhoneNumber,self.Location,self.accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f" error while updating next of kin details : {e}")
        else:
            raise Exception("cursor not availabe to update next of kin")
    def delete_account(self):

        self.accountNumber = self.data["accountNumber"]

        # reconnect to database 
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                delet_querry = " DELETE FROM AccountOwner  WHERE AccountNumber =%s"
                self.cursor.execute(delet_querry,(self.accountNumber,))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while deleting account:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not available to delete account number")





class ExistingAccounts(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")

    def fetchAccounts(self):
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT AccountNumber FROM BankAccount
                """)
                accounts = self.cursor.fetchall()
                self.close_connection()
            except Exception as e:
                raise Exception(f"error while fetching existing accounts: {e}")
            return { accountObj[0] for accountObj in accounts}
        

        
class ExistingIds(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")
        
    def fetchBranchIds(self):
        if self.cursor:
            try:
                self.cursor.execute(" USE NisaBranches")
                self.cursor.execute("""
                    SELECT BranchId  FROM Branches
                """)
                idList  = self.cursor.fetchall()
                self.close_connection()
                return {id[0] for id in idList }
            except Exception as e:
                raise Exception(f"error while fetching branch ids:{e}")
        else:
            raise Exception("cursor not initialized in the ExistingIds class")
        
    def fetchEmployeeIds(self):
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute(" USE employeeDatabase")
                self.cursor.execute("""
                    SELECT EmployeeId FROM employeeDetails
                """)
                idList  = self.cursor.fetchall()
                self.close_connection()
                return {id[0] for id in idList }
            except Exception as e:
                raise Exception(f"error while fetching branch ids:{e}")
        else:
            raise Exception("cursor not initialized in the ExistingIds class")
    def fetchLoanIds(self):
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT LoanId FROM LoanDetails
                """)
                data = self.cursor.fetchall()
                self.close_connection()
                return {idz[0] for idz in data }
            except Exception as e:
                raise Exception(f"error while fetching existing loanid: {e}")
        else:
            raise Exception("cursor not initailized while fetching loan idz")


        

class Branches(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")
    def createDatabase(self):
        if self.cursor:
            try:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS NisaBranches")
            except Exception as e:
                raise Exception(f"error while creating branches database: {e}")
            try:
                self.cursor.execute("USE NisaBranches")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Branches(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        BranchId VARCHAR(300) PRIMARY KEY,
                        BranchName VARCHAR(500)                
                    )
                """)

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS BranchDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        BranchId VARCHAR(300) NULL,
                        BranchManager VARCHAR(500),
                        Location VARCHAR(500),
                        FOREIGN KEY (BranchId) REFERENCES Branches(BranchId) ON DELETE SET NULL               
                    )
                """)
            except Exception as e:
                raise Exception("error while creating tables in beanch database:{e}")
        else:
            raise Exception("cursor not avialable")
    def insert_into_tables(self, branchObject):
        """
            _This methode inserts new branch details in the branch database_ 
            Args:
                branchObject (_dic_): _with the following keys,  branchName,BranchManager,ie employeeId_
        """
        self.BranchId = branchObject["branchId"]
        self.BranchName = branchObject["branchName"]
        self.BranchManager = branchObject["branchManager"]
        self.Location = branchObject["Location"]

        # reconnect cursor
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE NisaBranches")
                self.cursor.execute("""
                    INSERT INTO Branches(
                        BranchId,
                        BranchName              
                    ) VALUES(%s,%s)
                """,(self.BranchId, self.BranchName))
                self.cursor.execute("""
                    INSERT INTO BranchDetails(
                        BranchId,
                        BranchManager,
                        Location                
                    ) VALUES(%s,%s,%s)
                """,(self.BranchId, self.BranchManager, self.Location))
                self.connection.commit()
            except Exception as e:
                raise Exception(f" error while inserting into NiceBranches tables:{e}")
            finally:
                self.close_connection()
            
    def update_branchManager(self, employeeId, branchId):
        """
            _This methode update branch manager_
            Arg:
                _employeeId: (str), branchId: (str)_
            Return:
                _None_
        """
        self.employeeId = employeeId
        self.branchId = branchId

        # reconnect cursor
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE NisaBranches")
                self.cursor.execute("""
                    UPDATE BranchDetails
                    SET BranchManager = %s
                    WHERE
                        BranchId == %s   
                """,(self.employeeId,self.branchId))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating branch manager:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initialized while updating branchManager")
            

    def DeleteBranch(self,branchId):
        """
            _this methode deletes a branch_
            Arg:
                _branchId (str)_
            Return:
                _None_
        """
        self.branchId = branchId
        # reconnect cursor
        self.reconnect_if_needed()

        if self.cursor:
            try:
                self.cursor.execute("USE NisaBranches")
                self.cursor.execute("""
                    DELETE FROM Branches
                    WHERE
                        BranchId == %s
                """,(self.branchId,))
            except Exception as e:
                raise Exception(f"error while deleting branch from Nisa branches database:{e}")
            
    def fetch_branch_details(self):
        """_This methode fetches branch details_

        Returns:
            Branch Details: _object of branch details_
            
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                try:
                    self.cursor.execute("USE NisaBranches")
                    self.cursor.execute("""
                        SELECT
                            B.BranchId ,
                            B.BranchName,
                            D.BranchManager,
                            D.Location
                                        
                        FROM
                            Branches AS B
                        JOIN
                            BranchDetails AS D ON B.BranchId = D.BranchId
                    """)
                    branch_data = self.cursor.fetchall()
                    return [{"branchId":data[0], "branchName": data[1],"branchManager":data[2],"officeLocation":data[3]} for data in branch_data ]
                except Exception as e:
                    raise Exception(f"error while connecting to NisaBranches database as fetching branch details: {e}")
                
                finally:
                    self.close_connection()
            else:
                raise Exception("cursor is not initialized while fetching branch details")
        except Exception as e:
            raise Exception(f"error in fetching branch details: {e}")
        
    def numberOfBranches(self):
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE NisaBranches")
                self.cursor.execute("""
                    SELECT 
                        COUNT(*) AS numberOfBranches
                    FROM
                        Branches
                """)
                data = self.cursor.fetchone()
                if data is None:
                    raise Exception("No data returned from the query.")
            except Exception as e:
                raise Exception(f"error while fetching number of branches:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initialized while fetching number of branches")
        return {"branches":data[0] if data else 0}
        






class Deptments(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")
    def createDatabase(self):
        if self.cursor:
            try:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS NisaDeptments")
            except Exception as e:
                raise Exception(f"error while creating deptments database: {e}")
            try:
                self.cursor.execute("USE NisaDeptments")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Deptments(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        DeptId VARCHAR(500) PRIMARY KEY,
                        DeptName VARCHAR(500)                
                    )
                """)

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS DeptDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        DeptId VARCHAR(500) NULL,
                        DeptHead VARCHAR(500),
                        FOREIGN KEY (DeptId) REFERENCES Deptments(DeptId) ON DELETE SET NULL               
                    )
                """)
            except Exception as e:
                raise Exception(f"error while creating tables in deptment database:{e}")
        else:
            raise Exception("cursor not avialable in  deptment database")
    def insert_into_tables(self,deptObject):
        """_This methods inserts  dept details into database_

        Args:
            deptObject (_dic_): _deptId, headOfDept_
        """
        self.DeptId = deptObject["DeptId"]
        self.DeptName = deptObject["deptName"]
        self.DeptHead = deptObject["headOfDept"]

        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE NisaDeptments")
                self.cursor.execute("""
                    INSERT INTO Deptments(
                        DeptId,
                        DeptName                
                    )VALUES(%s,%s)
                """,(self.DeptId, self.DeptName))
                self.cursor.execute("""
                    INSERT INTO DeptDetails(
                        DeptId,
                        DeptHead              
                    )VALUES(%s,%s)
                """,(self.DeptId, self.DeptHead))
                self.connection.commit()
            else:
                raise Exception("cursor not initialized in inserting into dept database")
        except Exception as e:
            raise Exception(f"error in inserting into dept database:{e}")
        finally:
            self.close_connection()
    def fetch_existingDeptment(self):
        """_This methods fetches existing deptment details_

        Arg:
            none_
        Return:
            DeptDetails(set)
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE NisaDeptments")
                self.cursor.execute("""
                    SELECT
                        d.DeptId,
                        d.DeptName,
                        B.DeptHead 
                    FROM
                        Deptments AS d
                    JOIN
                        DeptDetails AS B ON B.DeptId = d.DeptId 
                """)
                data = self.cursor.fetchall()
                return [{"deptId":obj[0],"deptName":obj[1], "headOfDept":obj[2]} for obj in data]
        except Exception as e:
            raise Exception(f"error while fetching deptment details:{e}")
        finally:
            self.close_connection()

    def existingDeptIdz(self):
        """_This methods fetches existing deptment idz_

        Arg:
            none_
        Return:
            DeptId(set)_
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE NisaDeptments")
                self.cursor.execute("""
                    SELECT
                        DeptId
                    FROM
                        Deptments
                """)
                data = self.cursor.fetchall()
                return { obj[0] for obj in data}
        except Exception as e:
            raise Exception(f"error while fetching deptment details:{e}")
        finally:
            self.close_connection()



class ManagersDatabase(ConnectToMySql):
    def __init__(self):
        super().__init__()
        self.workStatus = "Activate"
    def creat_database(self):
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS ManagersDatabase")
                self.cursor.execute("""
                    USE  ManagersDatabase;
                    CREATE TABLE IF NOT EXISTS ManagersDetails (
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(100) PRIMARY KEY,
                        Mac VARCHAR(500) UNIQUE NOT NULL,
                        WorkStatus VARCHAR(100)
                    )  
                """)
            except Exception as e:
                raise Exception(f"error while manager database:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initialised while creating ManagersDatabase")
        
    
        
    def insert_into_database(self, managerDatils):
        self.reconnect_if_needed()
        self.EmployeeId = managerDatils["employeeId"]
        self.Mac = managerDatils["mac"]
        if self.cursor:
            try:
                self.cursor.execute("USE ManagersDatabase")
                self.cursor.execute("""
                    INSERT INTO ManagersDetails(
                        EmployeeId,
                        Mac,
                        WorkStatus                
                    )VALUES(%s,%s,%s)
                """,(self.EmployeeId, self.Mac,self.workStatus))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while inserting into ManagersDetails: {e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initialised while inserting into ManagersDatabase")
        
    def existingMAC(self):
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE ManagersDatabase")
                self.cursor.execute("""
                    SELECT
                        Mac               
                    FROM
                        ManagersDetails
                """)
                data = self.cursor.fetchall()
                if data:
                   return {obj[0]for obj in data}
                else:
                    return {obj for obj in data}
            except Exception as e:
                raise Exception(f"error while fetching existing mac:{e}")
        else:
            raise Exception("cursor not initialised while fetching existing mac")





class EmployeeDatabase(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
        self.workStatus = "Active"
    def create_database(self):
        if self.cursor:
            try:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS employeeDatabase")
            except Exception as e:
                raise Exception(f"error while creating employee database:{e}")
            try:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employeeDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) PRIMARY KEY,
                        Firstname VARCHAR(500),
                        LastName VARCHAR(500),
                        Age INT                                  
                    )  
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS contactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) NULL,
                        PhoneNumber VARCHAR(500),
                        Email VARCHAR(500),   
                        FOREIGN KEY(EmployeeId)  REFERENCES   employeeDetails(EmployeeId) ON DELETE SET NULL                                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ResidencyDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) NULL,
                        CurrentAddress VARCHAR(500),
                        District VARCHAR(500),
                        City VARCHAR(500),
                        Village VARCHAR(500),
                        FOREIGN KEY(EmployeeId)  REFERENCES   employeeDetails(EmployeeId) ON DELETE SET NULL                   
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS WorkDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) NULL,
                        WorkStatus VARCHAR(100),
                        Role TEXT,
                        BranchId VARCHAR(500),
                        BranchName VARCHAR(500),
                        Dept VARCHAR(500),
                        DeptId VARCHAR(500),
                        EmploymentType VARCHAR(500),
                        Salary INT,
                        FOREIGN KEY(EmployeeId)  REFERENCES   employeeDetails(EmployeeId) ON DELETE SET NULL                 
                    )
                """)

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Documments(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) NULL,
                        Documents LONGBLOB,
                        FOREIGN KEY(EmployeeId)  REFERENCES  employeeDetails(EmployeeId) ON DELETE SET NULL            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ProfilePictures(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) NULL,
                        profilePicture LONGBLOB,
                        FOREIGN KEY(EmployeeId)  REFERENCES  employeeDetails(EmployeeId) ON DELETE SET NULL                
                    )

                """)
            except Exception as e:
                raise Exception(F"error while creating tables in employeeDatabase :{e} ")

        else:
            raise Exception("cursor not initiated for create employee database")
        

    def insert_into_tables(self,employeeDetails):
        self.employeeId = employeeDetails["id"]
        self.firstName = employeeDetails["firstName"]
        self.lastName = employeeDetails["lastName"]
        self.age = employeeDetails["age"]
        self.phoneNumber = employeeDetails["phoneNumber"]
        self.email = employeeDetails["email"]
        self.current_address = employeeDetails["current_address"]
        self. district = employeeDetails["district"]
        self.city = employeeDetails["city"]
        self.village = employeeDetails["village"]
        self.Branch = employeeDetails["Branch"]
        self.dept = employeeDetails["dept"]
        self.deptId = employeeDetails["deptId"]
        self.employeeType = employeeDetails["employeeType"]
        self.roleAsigned = employeeDetails["roleAsigned"]
        self.salary = employeeDetails["salary"]
        self.documents = employeeDetails["documents"]
        self.profilePicture = employeeDetails["profilePicture"]
        self.branchId = employeeDetails["branchId"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                try:
                    self.cursor.execute("USE employeeDatabase")
                    self.cursor.execute("""
                        INSERT INTO employeeDetails(
                            EmployeeId,
                            Firstname,
                            LastName,
                            Age               
                        )VALUES (%s,%s,%s,%s)  
                    """,(self.employeeId,self.firstName,self.lastName,self.age))
                    self.cursor.execute("""
                        INSERT INTO contactDetails(
                            EmployeeId,
                            PhoneNumber,
                            Email                
                        )VALUES(%s,%s,%s)
                    """,(self.employeeId, self.phoneNumber,self.email))
                    self.cursor.execute("""
                        INSERT INTO ResidencyDetails(
                            EmployeeId,
                            CurrentAddress,
                            District,
                            City,
                            Village               
                        )VALUES(%s,%s,%s,%s,%s)
                    """,(self.employeeId,self.current_address,self.district,self.city,self.village))
                    self.cursor.execute("""
                        INSERT INTO WorkDetails(
                            EmployeeId,
                            WorkStatus,
                            Role,
                            BranchId,
                            BranchName,
                            Dept,
                            DeptId,
                            EmploymentType,
                            Salary                
                        )VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,(self.employeeId,self.workStatus,self.roleAsigned,self.branchId,self.Branch,self.dept,self.deptId, self.employeeType,self.salary))
                    self.cursor.execute("""
                        INSERT INTO Documments(
                            EmployeeId,
                            Documents              
                        )VALUES(%s,%s)
                    """,(self.employeeId,self.documents))

                    self.cursor.execute("""
                        INSERT INTO ProfilePictures(
                            EmployeeId,
                            profilePicture                 
                        ) VALUES(%s,%s)      
                    """,(self.employeeId, self.profilePicture))
                    self.connection.commit()
                except Exception as e:
                    raise Exception(f"error while inserting into employeeDatabase tables:{e}")
                finally:
                    self.close_connection()
            else:
                raise Exception("cursor not connected in insert into tables under employee database")
        except Exception as e:
            raise Exception(f"error while reconnecting the cursor in the insert into tables under employee db:{e}")
        
    def updateEmployeeDept(self,detailsObject):
        """_this methode update employee dept_
            Arg:
                _detailsObject: employeeId (str), dept assigned to (str), newRole (str)_
            Return:
                _Nothing_
        """
        employeeId = detailsObject["employeeId"]
        deptId = detailsObject["deptId"]
        role = detailsObject["NewRole"]

        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    UPDATE WorkDetails
                    SET DeptId = %s, Role = %s
                    WHERE
                        EmployeeId = %s    
                """,(deptId,role,employeeId))
                self.connection.commit()
            else:
                raise Exception("cursor not initialized while updating employee deptment")
        except Exception as e:
            raise Exception(f"error while updating employee dept: {e}")
        finally:
            self.close_connection()
    
    def updateEmployeeBranch(self,detailsObject):
        """_this methode update employee dept_
            Arg:
                _detailsObject: employeeId (str), Branch Id assigned to (str)_
            Return:
                _Nothing_
        """
        employeeId = detailsObject["employeeId"]
        branchId = detailsObject["branchId"]

        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    UPDATE WorkDetails
                    SET BranchId = %s
                    WHERE
                        EmployeeId = %s    
                """,(branchId,employeeId))
                self.connection.commit()
            else:
                raise Exception("cursor not initialized while updating employee deptment")
        except Exception as e:
            raise Exception(f"error while updating employee dept: {e}")
        finally:
            self.close_connection()

    def updateEmployeeSalary(self,detailsObject):
        """_this methode update employee dept_
            Arg:
                _detailsObject: employeeId (str), Salary amount to (int)_
            Return:
                _Nothing_
        """
        employeeId = detailsObject["employeeId"]
        salaryAmount = detailsObject["salary"]

        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    UPDATE WorkDetails
                    SET Salary = %s
                    WHERE
                        EmployeeId == %s    
                """,(salaryAmount,employeeId))
                self.connection.commit()
            else:
                raise Exception("cursor not initialized while updating employee deptment")
        except Exception as e:
            raise Exception(f"error while updating employee dept: {e}")
        finally:
            self.close_connection()
    def fetchEmployeeDetails(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT
                        E.EmployeeId,
                        E.Firstname,
                        E.LastName,
                        E.Age,
                        C.PhoneNumber,
                        C.Email,
                        R.CurrentAddress,
                        R.District,
                        R.City,
                        R.Village,
                        W.WorkStatus,
                        W.Role,
                        W.BranchId,
                        W.BranchName,
                        W.Dept,
                        W.DeptId,
                        W.EmploymentType,
                        W.Salary 
                    FROM
                        employeeDetails AS E
                    JOIN contactDetails AS C ON C.EmployeeId = E.EmployeeId
                    JOIN ResidencyDetails AS R ON R.EmployeeId = E.EmployeeId
                    JOIN WorkDetails AS W ON W.EmployeeId = E.EmployeeId
                                    
                """)
                dataObj = self.cursor.fetchall()
                return [{
                    "EmployeeId":data[0],
                    "Firstname":data[1],
                    "LastName":data[2],
                    "Age":data[3],
                    "PhoneNumber":data[4],
                    "Email":data[5],
                    "CurrentAddress":data[6],
                    "District":data[7],
                    "City":data[8],
                    "Village":data[9],
                    "WorkStatus":data[10],
                    "Role":data[11],
                    "BranchId":data[12],
                    "BranchName":data[13],
                    "Dept":data[14],
                    "DeptId":data[15],
                    "EmploymentType":data[16],
                    "Salary":data[17]
                    } for data in dataObj]
            else:
                raise Exception("cursor not initialized in fetching employee details")
        except Exception as e:
            raise Exception(f"error while fetching employee details:{e}")
        

    def fetchSpecificEmployeeDetails(self,employeeId):
        self.employeeId = employeeId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT
                        E.EmployeeId,
                        E.Firstname,
                        E.LastName,
                        E.Age,
                        C.PhoneNumber,
                        C.Email,
                        R.CurrentAddress,
                        R.District,
                        R.City,
                        R.Village,
                        W.WorkStatus,
                        W.Role,
                        W.BranchId,
                        W.BranchName,
                        W.Dept,
                        W.DeptId,
                        W.EmploymentType,
                        W.Salary 
                    FROM
                        employeeDetails AS E
                    JOIN contactDetails AS C ON C.EmployeeId = E.EmployeeId
                    JOIN ResidencyDetails AS R ON R.EmployeeId = E.EmployeeId
                    JOIN WorkDetails AS W ON W.EmployeeId = E.EmployeeId
                    WHERE E.EmployeeId = %s
                """,(self.employeeId,))
                dataObj = self.cursor.fetchall()
                return [{
                    "EmployeeId":data[0],
                    "Firstname":data[1],
                    "LastName":data[2],
                    "Age":data[3],
                    "PhoneNumber":data[4],
                    "Email":data[5],
                    "CurrentAddress":data[6],
                    "District":data[7],
                    "City":data[8],
                    "Village":data[9],
                    "WorkStatus":data[10],
                    "Role":data[11],
                    "BranchId":data[12],
                    "BranchName":data[13],
                    "Dept":data[14],
                    "DeptId":data[15],
                    "EmploymentType":data[16],
                    "Salary":data[17]
                    } for data in dataObj]
            else:
                raise Exception("cursor not initialized in fetching employee details")
        except Exception as e:
            raise Exception(f"error while fetching employee details:{e}")
        finally:
            self.close_connection()
        

    def fetchSpecificEmployeeMataDataDocument(self,employeeId):
        self.employeeId = employeeId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT
                        Documents
                    FROM
                        Documments
                    WHERE EmployeeId = %s
                """,(self.employeeId,))
                documents = self.cursor.fetchone()[0]
                return  documents 
            else:
                raise Exception("cursor not initialized in fetching employee document")
        except Exception as e:
            raise Exception(f"error while fetching employee document:{e}")
        finally:
            self.close_connection()
        
    def fetchSpecificEmployeeMataDataPictures(self,employeeId):
        self.employeeId = employeeId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT
                        profilePicture
                    FROM
                        ProfilePictures
                    WHERE EmployeeId = %s
                """,(self.employeeId,))
                picture = self.cursor.fetchone()[0]
                return  picture 
            else:
                raise Exception("cursor not initialized in fetching employee picture")
        except Exception as e:
            raise Exception(f"error while fetching employee picture:{e}")
        finally:
            self.close_connection()
    def fetchEmployeeBranchdetails(self,employeeId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT
                        BranchId,
                        BranchName
                    FROM
                        WorkDetails
                    WHERE
                        EmployeeId = %s
                          
                """,(employeeId,))
                data = self.cursor.fetchone()
                return data
            else:
                raise Exception("cursor not initialised in fetching employee branch details")

        except Exception as e:
            raise Exception(f"error while fetching employee dept details:{e}")




class BankingDataBase(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
    def createAccountTable(self):
        try:
            if self.cursor:
                try:
                    self.cursor.execute("CREATE DATABASE IF NOT EXISTS AccountsVault")
                except Exception as e:
                    raise Exception(f"error while creating banking database:{e}")
                try:
                    self.cursor.execute("USE AccountsVault")
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS BankAccount(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500) PRIMARY KEY,
                            FirstName VARCHAR(300),
                            SirName VARCHAR(300)                         
                        )
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS AccountSocialDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            NINNumber VARCHAR(500) PRIMARY KEY, 
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE                       
                        )
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS AccountPersonalDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            DateOfBirth VARCHAR(200),
                            Religion VARCHAR(200),
                            Gender VARCHAR(200),
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE
                        )
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS PermanentContactDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            Village VARCHAR(300),
                            Parish VARCHAR(300),
                            SubCounty VARCHAR(300),
                            County VARCHAR(300),
                            District VARCHAR(300),
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE  
                        )    
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS CurrentContactDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            Village VARCHAR(300),
                            Division VARCHAR(300),
                            District VARCHAR(300),
                            PhoneNumber VARCHAR(100),
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE  
                        )    
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS NextOfKinDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            FirstName VARCHAR(300),
                            SirName VARCHAR(300),
                            PhoneNumber VARCHAR(300),
                            Location VARCHAR(300),
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE                               
                        )
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS accountOwnerNationalId(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            NationalId TEXT,
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE                
                        )
                    """)
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS accountOwnerPicture(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            Photo TEXT,
                            FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE                
                        )
                    """)
                    self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS branchDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
                        BranchId VARCHAR(500),
                        OfficerId VARCHAR(500),
                        FOREIGN KEY(AccountNumber) REFERENCES BankAccount(AccountNumber) ON DELETE CASCADE                        
                    )
                """)
                except Exception as e:
                    raise Exception(f"error while creating tables in banking account database:{e}")
            else:
                raise Exception("cursor not initialized for create banking account")
        except Exception as e:
            raise Exception(f"error in create banking account:{e}")
        finally:
            self.close_connection()


    def insert_into_accountTable(self,accountObject):
        self.AccountNumber = accountObject["AccountNumber"]
        self.FirstName = accountObject["FirstName"]
        self.SirName = accountObject["Sirname"]
        self.NINNumber = accountObject["NinNumber"]
        self.DateOfBirth = accountObject["DateOfBirth"]
        self.Religion = accountObject["Religion"]
        self.Gender = accountObject["Gender"]
        self.Village = accountObject["Village"]
        self.Parish = accountObject["Parish"]
        self.SCounty = accountObject["SCounty"]
        self.county = accountObject["county"]
        self.District = accountObject["District"]
        self.PhoneNumber = accountObject["PhoneNumber"]
        self.CurrentVillage = accountObject["CurrentVillage"]
        self.CurrentDivision = accountObject["CurrentDivision"]
        self.CurrentDistrict = accountObject["CurrentDistrict"]
       
        # next of kin details
        self.nextOfKinDetails = accountObject["NextKinDetails"]
        self.nextOfKinFirstName = self.nextOfKinDetails["nextOfKinFirstName"]
        self.nextOfKinSirName = self.nextOfKinDetails["nextOfKinSirName"]
        self.nextOfKinPhone = self.nextOfKinDetails["PhoneNumber"]
        self.nextOfKinLocation = self.nextOfKinDetails["Location"]
        # pictures 
        self.accountOwnerNationalIdPath = accountObject["NationalIdPic"]
        self.Photo = accountObject["OwnerPic"]

        # branch details
        self.BranchDetails = accountObject["BranchDetails"]
        self.BranchId = self.BranchDetails["BranchId"]
        self.OfficerId = self.BranchDetails["OfficerId"]
        try:
            self.reconnect_if_needed()
        except Exception as e:
            raise Exception(f"error while reconnecting cursor in inserting into account tables:{e}")

        try:
            if self.cursor:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    INSERT INTO BankAccount(
                        AccountNumber,
                        FirstName,
                        SirName                
                ) VALUES(%s,%s,%s)
                """,(self.AccountNumber, self.FirstName, self.SirName))
                self.cursor.execute("""
                    INSERT INTO AccountSocialDetails(
                        AccountNumber,
                        NINNumber                    
                    ) VALUES(%s,%s)
                """,(self.AccountNumber, self.NINNumber))
                self.cursor.execute("""
                    INSERT INTO AccountPersonalDetails(
                        AccountNumber,
                        DateOfBirth,
                        Religion,
                        Gender             
                    ) VALUES (%s,%s,%s,%s)
                """,(self.AccountNumber, self.DateOfBirth,self.Religion,self.Gender))
                self.cursor.execute("""
                    INSERT INTO PermanentContactDetails(
                        AccountNumber,
                        Village,
                        Parish,
                        SubCounty,
                        County,
                        District                
                    ) VALUES(%s,%s,%s,%s,%s,%s)
                """,(self.AccountNumber,self.Village,self.Parish,self.SCounty,self.county, self.District))

                self.cursor.execute("""
                    INSERT INTO CurrentContactDetails(
                        AccountNumber,
                        Village,
                        Division,
                        District,
                        PhoneNumber                
                    ) VALUES(%s,%s,%s,%s,%s)
                """,(self.AccountNumber, self.CurrentVillage, self.CurrentDivision, self.CurrentDistrict, self.PhoneNumber))
                self.cursor.execute("""
                    INSERT INTO NextOfKinDetails(
                        AccountNumber,
                        FirstName,
                        SirName,
                        PhoneNumber,
                        Location               
                    ) VALUES (%s,%s,%s,%s,%s)
                """,(self.AccountNumber, self.nextOfKinFirstName,self.nextOfKinSirName,self.nextOfKinPhone,self.nextOfKinLocation))
                self.cursor.execute("""
                    INSERT INTO accountOwnerNationalId(
                        AccountNumber,
                        NationalId                
                    ) VALUES (%s,%s)
                """,(self.AccountNumber, self.accountOwnerNationalIdPath))

                self.cursor.execute("""
                    INSERT INTO accountOwnerPicture(
                        AccountNumber,
                        Photo                
                    ) VALUES (%s,%s)
                """,(self.AccountNumber, self.Photo))
                self.cursor.execute("""
                    INSERT INTO branchDetails(
                        AccountNumber,
                        BranchId,
                        OfficerId
                    ) VALUES(%s,%s,%s)
                """,(self.AccountNumber,self.BranchId, self.OfficerId))
                self.connection.commit()
            else:
                raise Exception("error while inserting into account database")
        except Exception as e:
            raise Exception(f"error in inserting into account tables:{e}")
        finally:
            self.close_connection()


    def fetchAllClientAccountDetails(self):
        """_This method fetches all clients details_
            _Args:
                _ None_
            Returen:
                _client details (list)_
        """
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        B.AccountNumber,
                        B.FirstName,
                        B.SirName,
                        S.NINNumber,
                        P.DateOfBirth,
                        P.Religion,
                        P.Gender,
                        C.Village,
                        C.Parish,
                        C.SubCounty,
                        C.County,
                        C.District,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        M.Village,
                        M.Division,
                        M.District,
                        M.PhoneNumber,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN PermanentContactDetails AS C ON C.AccountNumber = B.AccountNumber
                    JOIN CurrentContactDetails AS M ON M.AccountNumber = B.AccountNumber
                    JOIN NextOfKinDetails AS N ON N.AccountNumber = B.AccountNumber
                    JOIN accountOwnerPicture AS T ON T.AccountNumber = B.AccountNumber
                    JOIN branchDetails AS D ON D.AccountNumber = B.AccountNumber 
                """)
                data = self.cursor.fetchall()
                return [
                            {
                                "AccountNumber":obj[0],
                                "FirstName":obj[1],
                                "SirName":obj[2],
                                "NINNumber":obj[3],
                                "DateOfBirth":obj[4],
                                "Religion":obj[5],
                                "Gender":obj[6],
                                "Village":obj[7],
                                "Parish":obj[8],
                                "SubCounty":obj[9],
                                "County":obj[10],
                                "District":obj[11],
                                "CurrentAddressDetails":{
                                    "Village":obj[16],
                                    "Division":obj[17],
                                    "Districk":obj[18],
                                    "PhoneNumber":obj[19]
                                },
                                "nextOfKinDetails":{
                                    "FirstName":obj[12],
                                    "SirName":obj[13],
                                    "PhoneNumber":obj[14],
                                    "Location":obj[15]
                                },
                                "AccountOwnerPic":obj[20],
                                "branchDetails":{
                                    "BranchId":obj[21],
                                    "officerId":obj[22]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")
        

    def fetchSpecificClientAccountDetails(self, clientId):
        """_This method fetches all clients details for specific branch_
            _Args:
                _client id (str)_
            Returen:
                _client details (list)_
        """
        self.clientId = clientId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        B.AccountNumber,
                        B.FirstName,
                        B.SirName,
                        S.NINNumber,
                        P.DateOfBirth,
                        P.Religion,
                        P.Gender,
                        C.Village,
                        C.Parish,
                        C.SubCounty,
                        C.County,
                        C.District,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        M.Village,
                        M.Division,
                        M.District,
                        M.PhoneNumber,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN PermanentContactDetails AS C ON C.AccountNumber = B.AccountNumber
                    JOIN CurrentContactDetails AS M ON M.AccountNumber = B.AccountNumber
                    JOIN NextOfKinDetails AS N ON N.AccountNumber = B.AccountNumber
                    JOIN accountOwnerPicture AS T ON T.AccountNumber = B.AccountNumber
                    JOIN branchDetails AS D ON D.AccountNumber = B.AccountNumber
                    WHERE
                        B.AccountNumber =%s
                        
                """,(self.clientId,))
                data = self.cursor.fetchall()
                return [
                            {
                                "AccountNumber":obj[0],
                                "FirstName":obj[1],
                                "SirName":obj[2],
                                "NINNumber":obj[3],
                                "DateOfBirth":obj[4],
                                "Religion":obj[5],
                                "Gender":obj[6],
                                "Village":obj[7],
                                "Parish":obj[8],
                                "Subcounty":obj[9],
                                "County":obj[10],
                                "District":obj[11],
                                "CurrentAddressDetails":{
                                    "Village":obj[16],
                                    "Division":obj[17],
                                    "Districk":obj[18],
                                    "PhoneNumber":obj[19]
                                },
                                "nextOfKinDetails":{
                                    "FirstName":obj[12],
                                    "SirName":obj[13],
                                    "PhoneNumber":obj[14],
                                    "Location":obj[15]
                                },
                                "AccountOwnerPic":obj[20],
                                "branchDetails":{
                                    "BranchId":obj[21],
                                    "officerId":obj[22]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")

        

    def fetchAllClientAccountDetailsForSpecificBranch(self, branchId):
        """_This method fetches all clients details for specific branch_
            _Args:
                _branchId (str)_
            Returen:
                _client details (list)_
        """
        self.BranchId = branchId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        B.AccountNumber,
                        B.FirstName,
                        B.SirName,
                        S.NINNumber,
                        P.DateOfBirth,
                        P.Religion,
                        P.Gender,
                        C.Village,
                        C.Parish,
                        C.SubCounty,
                        C.County,
                        C.District,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        M.Village,
                        M.Division,
                        M.District,
                        M.PhoneNumber,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN PermanentContactDetails AS C ON C.AccountNumber = B.AccountNumber
                    JOIN CurrentContactDetails AS M ON M.AccountNumber = B.AccountNumber
                    JOIN NextOfKinDetails AS N ON N.AccountNumber = B.AccountNumber
                    JOIN accountOwnerPicture AS T ON T.AccountNumber = B.AccountNumber
                    JOIN branchDetails AS D ON D.AccountNumber = B.AccountNumber
                    WHERE
                        D.BranchId =%s
                        
                """,(self.BranchId,))
                data = self.cursor.fetchall()
                return [
                            {
                                "AccountNumber":obj[0],
                                "FirstName":obj[1],
                                "SirName":obj[2],
                                "NINNumber":obj[3],
                                "DateOfBirth":obj[4],
                                "Religion":obj[5],
                                "Gender":obj[6],
                                "Village":obj[7],
                                "Parish":obj[8],
                                "Subcounty":obj[9],
                                "County":obj[10],
                                "District":obj[11],
                                "CurrentAddressDetails":{
                                    "Village":obj[16],
                                    "Division":obj[17],
                                    "Districk":obj[18],
                                    "PhoneNumber":obj[19]
                                },
                                "nextOfKinDetails":{
                                    "FirstName":obj[12],
                                    "SirName":obj[13],
                                    "PhoneNumber":obj[14],
                                    "Location":obj[15]
                                },
                                "AccountOwnerPic":obj[20],
                                "branchDetails":{
                                    "BranchId":obj[21],
                                    "officerId":obj[22]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")




    def fetchAllClientAccountDetailsForSpecificEmployee(self, employeeId):
        """_This method fetches all clients details for specific credit officer_
            _Args:
                _employeeId (str)_
            Returen:
                _client details (list)_
        """
        self.employeeID = employeeId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        B.AccountNumber,
                        B.FirstName,
                        B.SirName,
                        S.NINNumber,
                        P.DateOfBirth,
                        P.Religion,
                        P.Gender,
                        C.Village,
                        C.Parish,
                        C.SubCounty,
                        C.County,
                        C.District,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        M.Village,
                        M.Division,
                        M.District,
                        M.PhoneNumber,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN PermanentContactDetails AS C ON C.AccountNumber = B.AccountNumber
                    JOIN CurrentContactDetails AS M ON M.AccountNumber = B.AccountNumber
                    JOIN NextOfKinDetails AS N ON N.AccountNumber = B.AccountNumber
                    JOIN accountOwnerPicture AS T ON T.AccountNumber = B.AccountNumber
                    JOIN branchDetails AS D ON D.AccountNumber = B.AccountNumber
                    WHERE
                        D.OfficerId =%s
                        
                """,(self.employeeID,))
                data = self.cursor.fetchall()
                return [
                            {
                                "AccountNumber":obj[0],
                                "FirstName":obj[1],
                                "SirName":obj[2],
                                "NINNumber":obj[3],
                                "DateOfBirth":obj[4],
                                "Religion":obj[5],
                                "Gender":obj[6],
                                "Village":obj[7],
                                "Parish":obj[8],
                                "Subcounty":obj[9],
                                "County":obj[10],
                                "District":obj[11],
                                "CurrentAddressDetails":{
                                    "Village":obj[16],
                                    "Division":obj[17],
                                    "Districk":obj[18],
                                    "PhoneNumber":obj[19]
                                },
                                "nextOfKinDetails":{
                                    "FirstName":obj[12],
                                    "SirName":obj[13],
                                    "PhoneNumber":obj[14],
                                    "Location":obj[15]
                                },
                                "AccountOwnerPic":obj[20],
                                "branchDetails":{
                                    "BranchId":obj[21],
                                    "officerId":obj[22]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")
        



    def fetchClientAccountDetailsWithActivateLoanForSpecificEmployee(self, employeeId):
        """_This method fetches all clients with activate loans details for specific credit officer_
            _Args:
                _employeeId (str)_
            Returen:
                _client details (list)_
        """
        self.employeeID = employeeId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.ActiveStatus,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        E.Contact,
                        F.Gender
                    FROM
                        registeredLoans AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                Contact
                            FROM
                                WorkDetails              
                        )AS E ON E.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        AccountsVault.AccountPersonalDetails AS F ON F.AccountNumber = B.ClientID
                            
                    JOIN
                        (SELECT
                            AccountNumber,
                            OfficerId
                        FROM
                            AccountsVault.branchDetails
                        WHERE
                            OfficerId = %s            
                        ) AS D ON D.AccountNumber = B.ClientID
                        
                    WHERE
                        r.ActiveStatus = 'unfinished'
                         
                """,(employeeId,))
                data = self.cursor.fetchall()
                return [{"LoanId":obj[0],
                         "ActivateStatus": obj[1],
                         "AccountNumber":obj[2],
                         "fName":obj[3],
                         "lName":obj[4],
                         "Phonenumber":obj[5],
                         "Gender":obj[6]
                         } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client with activate loans details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients  with activate loansdetails")
        


    def fetchClientAccountDetailsWithActivateLoanFormanager(self,branchId):
        """_This method fetches all clients with activate loans details for the general manager_
            _Args:
                _None_
            Returen:
                _client details (list)_
        """
        
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.ActiveStatus,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        E.Contact,
                        F.Gender,
                        B.BranchId,
                        G.BranchName
                    FROM
                        registeredLoans AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId,
                                BranchId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                Contact
                            FROM
                                WorkDetails              
                        )AS E ON E.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        AccountsVault.AccountPersonalDetails AS F ON F.AccountNumber = B.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches                
                        ) AS G ON G.BranchId = B.BranchId
                        
                        
                    WHERE
                        r.ActiveStatus = 'unfinished' AND B.BranchId = %s
                            
                """,(branchId,))
                data = self.cursor.fetchall()
                return [{"LoanId":obj[0],
                            "ActivateStatus": obj[1],
                            "AccountNumber":obj[2],
                            "fName":obj[3],
                            "lName":obj[4],
                            "Phonenumber":obj[5],
                            "Gender":obj[6],
                            "BranchId":obj[7],
                            "BranchName": obj[8]
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client with activate loans details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients  with activate loansdetails")
        



    def fetchClientAccountDetailsWithFinshedLoanFormanager(self,branchId):
        """_This method fetches all clients with finshed loans details for the general manager_
            _Args:
                _None_
            Returen:
                _client details (list)_
        """
        
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.ActiveStatus,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        E.Contact,
                        F.Gender,
                        B.BranchId,
                        G.BranchName
                    FROM
                        registeredLoans AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId,
                                BranchId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                Contact
                            FROM
                                WorkDetails              
                        )AS E ON E.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        AccountsVault.AccountPersonalDetails AS F ON F.AccountNumber = B.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches
                            WHERE
                                BranchId = %s
                                                   
                        ) AS G ON G.BranchId = B.BranchId
                        
                        
                    WHERE
                        r.ActiveStatus = 'Finshed' AND B.ClientID NOT IN (
                                        SELECT
                                            L.ClientID
                                        FROM
                                            registeredLoans AS r
                                        JOIN
                                            LoanDetails AS L ON L.LoanId = r.LoanId
                                        WHERE
                                            r.ActiveStatus = "unfinished" AND L.BranchId = %s 
                                    )
                            
                """,(branchId,branchId))
                data = self.cursor.fetchall()
                return [{"LoanId":obj[0],
                            "ActivateStatus": obj[1],
                            "AccountNumber":obj[2],
                            "fName":obj[3],
                            "lName":obj[4],
                            "Phonenumber":obj[5],
                            "Gender":obj[6],
                            "BranchId":obj[7],
                            "BranchName": obj[8]
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client with activate loans details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients  with activate loansdetails")
        
    def fetchAllClientAccountDetailsForSpecificBranchFormanager(self, branchId):
        """_This method fetches all clients details for specific credit branch_
            _Args:
                _Branch (str)_
            Returen:
                _client details (list)_
        """
        self.branchId = branchId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        B.AccountNumber,
                        B.FirstName,
                        B.SirName,
                        S.NINNumber,
                        P.DateOfBirth,
                        P.Religion,
                        P.Gender,
                        C.Village,
                        C.Parish,
                        C.SubCounty,
                        C.County,
                        C.District,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        M.Village,
                        M.Division,
                        M.District,
                        M.PhoneNumber,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId,
                        M.BranchName
                        
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN PermanentContactDetails AS C ON C.AccountNumber = B.AccountNumber
                    JOIN CurrentContactDetails AS M ON M.AccountNumber = B.AccountNumber
                    JOIN NextOfKinDetails AS N ON N.AccountNumber = B.AccountNumber
                    JOIN accountOwnerPicture AS T ON T.AccountNumber = B.AccountNumber
                    JOIN branchDetails AS D ON D.AccountNumber = B.AccountNumber
                    JOIN NisaBranches.Branches AS M ON M.BranchId = D.BranchId
                    WHERE
                        D.BranchId = %s
                                      
                """,(self.branchId,))
                data = self.cursor.fetchall()
                return [
                            {
                                "AccountNumber":obj[0],
                                "FirstName":obj[1],
                                "SirName":obj[2],
                                "NINNumber":obj[3],
                                "DateOfBirth":obj[4],
                                "Religion":obj[5],
                                "Gender":obj[6],
                                "Village":obj[7],
                                "Parish":obj[8],
                                "Subcounty":obj[9],
                                "County":obj[10],
                                "District":obj[11],
                                "CurrentAddressDetails":{
                                    "Village":obj[16],
                                    "Division":obj[17],
                                    "Districk":obj[18],
                                    "PhoneNumber":obj[19]
                                },
                                "nextOfKinDetails":{
                                    "FirstName":obj[12],
                                    "SirName":obj[13],
                                    "PhoneNumber":obj[14],
                                    "Location":obj[15]
                                },
                                "AccountOwnerPic":obj[20],
                                "branchDetails":{
                                    "BranchId":obj[21],
                                    "Branchname":obj[22],
                                    "officerId":obj[23]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")





    def fetchClientAccountDetailsWithFinshedLoanForSpecificEmployee(self, employeeId):
        """_This method fetches all clients with finished loans details for specific credit officer_
            _Args:
                _employeeId (str)_
            Returen:
                _client details (list)_
        """
        self.employeeID = employeeId
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.ActiveStatus,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        E.Contact,
                        F.Gender
                    FROM
                        registeredLoans AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                Contact
                            FROM
                                WorkDetails              
                        )AS E ON E.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        AccountsVault.AccountPersonalDetails AS F ON F.AccountNumber = B.ClientID
                            
                    JOIN
                        (SELECT
                            AccountNumber,
                            OfficerId
                        FROM
                            AccountsVault.branchDetails
                        WHERE
                            OfficerId = %s            
                        ) AS D ON D.AccountNumber = B.ClientID
                        
                    WHERE
                        r.ActiveStatus = 'Finshed' AND B.ClientID NOT IN  (
                                        SELECT
                                            L.ClientID
                                        FROM
                                            registeredLoans AS r
                                        JOIN
                                            LoanDetails AS L ON L.LoanId = r.LoanId
                                        WHERE
                                            r.ActiveStatus = "unfinished" AND L.OfficerId = %s  
                                    )
                         
                """,(self.employeeID,self.employeeID))
                data = self.cursor.fetchall()
                return [{"LoanId":obj[0],
                         "ActivateStatus": obj[1],
                         "AccountNumber":obj[2],
                         "fName":obj[3],
                         "lName":obj[4],
                         "Phonenumber":obj[5],
                         "Gender":obj[6]
                         } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client with Finshed loans details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients  with Finshed loansdetails")







    
    def update_ClientphoneNumber(self, newnumberObject):
        """
            _summary: this method is called when update client's number
            Arg:
                _newnumberObject:(dic),accountNumber and phoneNumber
            Return: none  
        """

        self.accountNumber = newnumberObject["accountNumber"]
        self.phoneNumber = newnumberObject["phoneNumber"]

        # reconnect to database 
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE AccountsVault")
                update_query = """
                        UPDATE PermanentContactDetails
                        SET PhoneNumber = %s
                        WHERE AccountNumber = %s
                    """
                self.cursor.execute(update_query, (self.phoneNumber ,self.accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating phone numer:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not availabe to update phone number:")
        
    
    def create_loanApplicationTAbles(self):
        self.reconnect_if_needed()
        try:
            if self.cursor:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS LoanApplications")
                self.cursor.execute("USE LoanApplications")

                # Create LoanDetails table
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LoanDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        ClientID VARCHAR(500) NOT NULL,
                        BranchId VARCHAR(500),
                        OfficerId VARCHAR(500),
                        LoanAmount VARCHAR(300),
                        InterestRateInPercentage VARCHAR(50),
                        LoanPeriodInDays VARCHAR(50),
                        Status VARCHAR(100)
                    )
                """)

                # Create AddressDetails table with foreign key referencing LoanDetails
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS AddressDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500),
                        ClientCurrentaddress VARCHAR(500),
                        DivisionCity VARCHAR(500),
                        District VARCHAR(500),
                        FOREIGN KEY(LoanId) REFERENCES LoanDetails(LoanId) ON DELETE CASCADE
                    )
                """)

                # Create WorkDetails table with foreign key referencing LoanDetails
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS WorkDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500),
                        Occupation VARCHAR(500), 
                        WorkArea VARCHAR(500),
                        BusinessLocation VARCHAR(500),  
                        Contact VARCHAR(500),
                        BusinessImages VARCHAR(1000),
                        FOREIGN KEY(LoanId) REFERENCES LoanDetails(LoanId) ON DELETE CASCADE
                    )
                """)

            else:
                raise Exception("cursor not intialized in create loanapplication tables methods")
        except Exception as e:
            raise Exception(f"error in create loan application table methods:{e}")
        finally:
            self.close_connection()
    def insert_into_loanApplicationTAbles(self, loanApplicationDetails):
        self.loanStatus ="notApproved"
        self.loanID = loanApplicationDetails["loanID"]
        self.clientId = loanApplicationDetails["clientId"]
        self.loanAmount = loanApplicationDetails["loanAmount"]
        self.interestRate = loanApplicationDetails["interestRate"]
        self.loanPeriod = loanApplicationDetails["loanPeriod"]
        self.clientCurrentaddress = loanApplicationDetails["clientCurrentaddress"]
        self.devisioncity = loanApplicationDetails["devisioncity"]
        self.state = loanApplicationDetails["state"]
        self.Occuption = loanApplicationDetails["Occuption"]
        self.workArea = loanApplicationDetails["workArea"]
        self.businessLoaction = loanApplicationDetails["businessLoaction"]
        self.contact = loanApplicationDetails["contact"]
        self.businessPictureRelativePath = loanApplicationDetails["businessPictureRelativePath"]
        # BranchDetails
        BranchDetails = loanApplicationDetails["BranchDetails"]
        self.BranchId = BranchDetails["BranchId"]
        self.OfficerId = BranchDetails["OfficerId"]



        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO LoanDetails(
                        LoanId,
                        ClientID ,
                        BranchId ,
                        OfficerId,
                        LoanAmount,
                        InterestRateInPercentage,
                        LoanPeriodInDays,
                        Status                   
                    )VALUES(%s,%s,%s,%s,%s,%s,%s,%s)

                """,(self.loanID, self.clientId,self.BranchId,self.OfficerId,self.loanAmount,self.interestRate,self.loanPeriod, self.loanStatus))
                self.cursor.execute("""
                    INSERT INTO AddressDetails(
                        LoanId,
                        ClientCurrentaddress,
                        DivisionCity,
                        District               
                    ) VALUES(%s,%s,%s,%s)
                """,(self.loanID, self.clientCurrentaddress,self.devisioncity,self.state))
                self.cursor.execute("""
                    INSERT INTO WorkDetails(
                        LoanId,
                        Occupation, 
                        WorkArea,
                        BusinessLocation,  
                        Contact,
                        BusinessImages                
                    )VALUES(%s,%s,%s,%s,%s,%s)
                """,(self.loanID, self.Occuption,self.workArea,self.businessLoaction,self.contact,self.businessPictureRelativePath))
                self.connection.commit()
                
            else:
                raise Exception("cursor not initialiesed while inserting into loanApplication tables")
        except Exception as e:
            raise Exception(f"error in insert into loan application tables method:{e}")
        finally:
            self.close_connection()


    def updateLoanApplicationApprovalStatus(self, loanApprovalDetails):
        self.approval = "approved"
        self.amount = loanApprovalDetails["approvedAmount"]
        self.interestRate = loanApprovalDetails["interestRate"]
        self.period = loanApprovalDetails["paymentPeriod"]
        self.loanId = loanApprovalDetails["loanId"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE LoanDetails
                    SET
                        LoanAmount =%s,
                        InterestRateInPercentage =%s,
                        LoanPeriodInDays =%s,
                        Status =%s
                    WHERE LoanId = %s
                """, (self.amount, self.interestRate,self.period,self.approval,self.loanId))
                self.connection.commit()
            else:
                raise Exception("cursor not initialised in loan approval status methode")
        except Exception as e:
            raise Exception(f"error while updating loan approval status:{e}")
        finally:

            self.close_connection()

    def updateLoanApplicationToDeletedBYUnderWriter(self, loanId):
        self.deleted = "Deleted"
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE LoanDetails
                    SET
                        Status =%s
                    WHERE LoanId = %s
                """, (self.deleted,loanId))
                self.connection.commit()
            else:
                raise Exception("cursor not initialised while deleting the loan")
        except Exception as e:
            raise Exception(f"error while updating loan status to deleted:{e}")
        finally:

            self.close_connection()


    def loanApplicationApprovelTrigger(self):
        """
            _this method is called in underwriter's route where loan approval is done_
            Args:
                _approvedLoanDetails(_dic):approved loan details
            Return:
                _none
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                 # Drop the trigger if it exists to avoid duplicate errors
                self.cursor.execute("DROP TRIGGER IF EXISTS registeredLoanAfterApprovalByManager")
                self.cursor.execute("""
                    CREATE TRIGGER registeredLoanAfterApprovalByManager
                    BEFORE UPDATE ON LoanDetails
                    FOR EACH ROW
                    BEGIN
                        
                        INSERT INTO approvedLoans(
                            LoanId,
                            ClientID,
                            BranchId,
                            OfficerId,
                            LoanAmountAppliedFor,
                            LoanAmountApproved,
                            InterestRateInPercentage,
                            LoanPeriodInDays                
                        ) VALUES(
                            OLD.LoanId,
                            OLD.ClientID,
                            OLD.BranchId,
                            OLD.OfficerId,
                            OLD.LoanAmount,
                            NEW.LoanAmount,
                            NEW.InterestRateInPercentage,
                            NEW.LoanPeriodInDays
                        );
                    END;
                """)
                
                self.connection.commit()
            else:
                raise Exception("cursor not initialised in the trigger loan approvel status")
        except Exception as e:
            raise Exception(f"error while trigger loan approvel status:{e}")


    def create_loanBalancingTable(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE  LoanApplications")
                self.cursor.execute("""
                    
                    CREATE TABLE IF NOT EXISTS LoanBalancing(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        BalancingAmount DECIMAL(13,2),
                        AccountBalancedWith VARCHAR(500)              
                    )
                """)
            else:
                raise Exception("error while creating loan balancing table")
        except Exception as e:
            raise Exception(f"error while creating loan balancing table:{e}")
        finally:
            self.close_connection()


    def CreateapprovedLoans_tables(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS approvedLoans(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        ClientID VARCHAR(500) NOT NULL,
                        BranchId VARCHAR(500),
                        OfficerId VARCHAR(500),
                        LoanAmountAppliedFor DECIMAL(13,2),
                        LoanAmountApproved DECIMAL(13,2),
                        InterestRateInPercentage DECIMAL(12,1),
                        LoanPeriodInDays VARCHAR(50)               
                    )
                """)
            else:
                raise Exception("cursor not initialized while creating approved loan tables")
        except Exception as e:
            raise Exception(f"error while creating approved loan tables:{e}")


    
        
    def Create_disbursement_table(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS DisbursementDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY              
                    )
                """)
            else:
                raise Exception("cursor not initialized in disburshment method")
        except Exception as e:
            raise Exception(f"error in while creating disburshement table in disburshment methode:{e}")
        finally:
            self.close_connection()

    def insert_into_disbursement_table(self,loanId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO DisbursementDetails(
                        LoanId                
                    ) VALUES(%s)
                """,(loanId,))
                self.connection.commit()
            else:
                raise Exception("cursor not initialized while inserting into  disburshment table")
        except Exception as e:
            raise Exception(f"error in while inserting into  disburshement table:{e}")
        finally:
            self.close_connection()
    def clientloanpaymentsAndInvestmentTable(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ClientsLOANpaymentDETAILS(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500),
                        Amount DECIMAL(30, 2)                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ClientsInvestmentPaymentDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ClientId  VARCHAR(500),
                        Amount DECIMAL(30, 2)                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ClientsTotalInvestment(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ClientId  VARCHAR(500) PRIMARY KEY,
                        TotalCurrentInvestment DECIMAL(30, 2)                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LoanPaymentStatistics(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId  VARCHAR(500),
                        Commitment DECIMAL(30, 2),
                        Paid DECIMAL(30,2),
                        Balance DECIMAL(30,2),
                        Portifolio DECIMAL(30,2)               
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PenaltiesAndOverDues(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId  VARCHAR(500),
                        Commitment DECIMAL(30, 2),
                        Paid DECIMAL(30,2),
                        OverDue DECIMAL(30, 2),
                        Penalty DECIMAL(30,2) 
                                    
                    )

                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TotalPenaltiesAndOverDues(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId  VARCHAR(500) PRIMARY KEY,
                        TotalOverDue DECIMAL(30, 2),
                        TotalPenalty DECIMAL(30,2) 
                                    
                    )

                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PenaltyPayments(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId  VARCHAR(500),
                        Amount DECIMAL(30,2) 
                                    
                    )

                """)
            else:
                raise Exception("cursor not initialised while creating client loan payment table")
        except Exception as e:
            raise Exception(f"error while creating client loan payment table:{e}")
        finally:
            self.close_connection()

    
    def insert_into_ClientsPenaltyPayments(self, paymentsdata):
        LoanId = paymentsdata['loanId']
        amount = paymentsdata['amount']
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO PenaltyPayments(
                        LoanId,
                        Amount               
                    )VALUES(%s,%s)
                """,(LoanId,amount))
                self.connection.commit()
                return True
            else:
                raise Exception("cursor not initialised while inserting into penalty payments  table")
        except Exception as e:
            raise Exception(f"error while inserting into  penalty payment  table:{e}")
        finally:
            self.close_connection()

    def total_PenaltyPayments_triger(self, paymentsdata):
        LoanId = paymentsdata['loanId']
        amount = paymentsdata['amount']
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE  TotalPenaltiesAndOverDues
                    SET TotalPenalty = TotalPenalty - %s
                    WHERE LoanId = %s
                """,(amount,LoanId))
                self.connection.commit()
                return True
            else:
                raise Exception("cursor not initialised while updating total penalty payments  table")
        except Exception as e:
            raise Exception(f"error while updating total penalty  table:{e}")
        finally:
            self.close_connection()

    def insert_into_ClientsInvestmentPaymentDetails(self,AccountNumber,amount):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO ClientsInvestmentPaymentDetails(
                        ClientId,
                        Amount               
                    )VALUES(%s,%s)
                """,(AccountNumber,amount))
                self.connection.commit()
            else:
                raise Exception("cursor not initialised while inserting into investmentpayment  table")
        except Exception as e:
            raise Exception(f"error while inserting into  ClientsInvestmentPaymentDetails  table:{e}")
        

    def TotalInvestmentsTrigger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS insertIntoTotalInvestment")
                self.cursor.execute("""
                    CREATE TRIGGER insertIntoTotalInvestment
                    AFTER INSERT ON ClientsInvestmentPaymentDetails
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO ClientsTotalInvestment(
                            ClientId,
                            TotalCurrentInvestment            
                        )
                        VALUES(
                            NEW.ClientId,
                            NEW.Amount           
                        )
                        ON DUPLICATE KEY UPDATE
                            TotalCurrentInvestment = COALESCE(TotalCurrentInvestment,0) + NEW.Amount;
                    END;
                        
                """)
            else:
                raise Exception("cursor not initialised in the total investment trigger")
        except Exception as e:
            raise Exception(f"error while firing total investment trigger:{e}")


    def fetch_total_loan_penalty_payments(self,clientid):
        try:
            self.reconnect_if_needed()
            self.cursor.execute("USE LoanApplications")
            self.cursor.execute("""
                select
                    COALESCE(SUM(Amount),0)
                from
                    PenaltyPayments
                where
                    LoanId IN (
                                SELECT
                                    LoanId
                                FROM 
                                    registeredLoans
                                WHERE
                                    ActiveStatus = "unfinished" AND 
                                    LoanId IN  (
                                                SELECT 
                                                    LoanId 
                                                FROM 
                                                    LoanDetails 
                                                WHERE 
                                                    ClientID = %s
                                            ) 
                                
                            )        
                    
            """,(clientid,))
            data = self.cursor.fetchone()
            return {'amount':float(data[0])}
        except Exception as e:
            return Exception(f"cursor failed to reconnect while fetching clients penalty payment detials:{e}")
    def fetch_loan_penalty_payments(self,clientid):
        try:
            self.reconnect_if_needed()
            self.cursor.execute("USE LoanApplications")
            self.cursor.execute("""
                select
                    Amount
                from
                    PenaltyPayments
                where
                    LoanId IN (
                                SELECT
                                    LoanId
                                FROM 
                                    registeredLoans
                                WHERE
                                    ActiveStatus = "unfinished" AND 
                                    LoanId IN  (
                                                SELECT 
                                                    LoanId 
                                                FROM 
                                                    LoanDetails 
                                                WHERE 
                                                    ClientID = %s
                                            ) 
                                
                            )        
                    
            """,(clientid,))
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            return Exception(f"cursor failed to reconnect while fetching clients penalty payment detials:{e}")
        
    def fetch_ClientsInvestmentDetails(self,AccountNumber):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(Date),
                        Amount
                    FROM
                        ClientsInvestmentPaymentDetails
                    WHERE
                        ClientId = %s             
                """,(AccountNumber,))
                data = self.cursor.fetchall()
                return [{"date": str(obj[0]),"Amount": float(obj[1])} for obj in data]
            else:
                raise Exception("cursor not initialised while fetching client investment details")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  table:{e}")
        
    

    def fetch_ClientsInvestmentDetailsForSpecficEmployee(self,EmployeeId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(A.Date),
                        A.ClientId,
                        C.FirstName,
                        C.SirName,
                        A.Amount
                    FROM
                        ClientsInvestmentPaymentDetails AS A
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount                   
                        ) AS C ON C.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                OfficerId
                            FROM
                                AccountsVault.branchDetails
                            WHERE
                                OfficerId = %s 
                        ) AS B ON B.AccountNumber = A.ClientId 
                    WHERE
                        DATE(A.Date) = %s
                                  
                """,(EmployeeId,current_date))
                data = self.cursor.fetchall()
                if data:
                    return [{"date": str(obj[0]), "AccountNumber":obj[1], "fname":obj[2], "lName":obj[3], "Amount": float(obj[4])} for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client investment details for a specific employee")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  for a specific employee table:{e}")




    def fetch_ClientsInvestmentDetailsForSpecficBranch(self,BranchId):
        """
            This method fetches recieved investment details for a branch
            _Arg:branchid,(str)
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(A.Date),
                        A.ClientId,
                        C.FirstName,
                        C.SirName,
                        A.Amount,
                        B.BranchId,
                        M.BranchName
                    FROM
                        ClientsInvestmentPaymentDetails AS A
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount                   
                        ) AS C ON C.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                BranchId
                            FROM
                                AccountsVault.branchDetails
                            WHERE
                                BranchId = %s 
                        ) AS B ON B.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches             
                        ) AS M ON M.BranchId = B.BranchId
                    WHERE
                        DATE(A.Date) = %s
                                  
                """,(BranchId,current_date))
                data = self.cursor.fetchall()
                if data:
                    return [{"date": str(obj[0]), 
                             "AccountNumber":obj[1], 
                             "fname":obj[2], 
                             "lName":obj[3], 
                             "Amount": float(obj[4]),
                             "BranchId":obj[5],
                             "BranchName":obj[6]
                             } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client investment details for a specific branch")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  for a specific  branch:{e}")

    def fetch_GeneralCurrent_ClientsInvestmentDetails(self):
        """
            This method fetches recieved  general investment details
            _Arg:none
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(A.Date),
                        A.ClientId,
                        C.FirstName,
                        C.SirName,
                        A.Amount,
                        B.BranchId,
                        M.BranchName
                    FROM
                        ClientsInvestmentPaymentDetails AS A
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount                   
                        ) AS C ON C.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                BranchId
                            FROM
                                AccountsVault.branchDetails
                             
                        ) AS B ON B.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches             
                        ) AS M ON M.BranchId = B.BranchId
                    WHERE
                        DATE(A.Date) = %s
                    ORDER BY B.BranchId 
                                  
                """,(current_date,))
                data = self.cursor.fetchall()
                if data:
                    return [{"date": str(obj[0]), 
                             "AccountNumber":obj[1], 
                             "fname":obj[2], 
                             "lName":obj[3], 
                             "Amount": float(obj[4]),
                             "BranchId":obj[5],
                             "BranchName":obj[6]
                             } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client investment details for a specific branch")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  for a specific  branch:{e}")



    def fetch_GeneralCurrentClientsInvestmentTotal(self):
        """
            This method fetches   general  total investment
            _Arg:none
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                            SELECT
                                SUM(Amount)
                            FROM
                                ClientsInvestmentPaymentDetails
                            WHERE
                                DATE(Date) = %s
                                  
                """,(current_date,))
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"total":float(data[0])}
                else:
                    return {"total":0}
            else:
                raise Exception("cursor not initialised while fetching client total investment ")
        except Exception as e:
            raise Exception(f"error while fetching from  total ClientsInvestmentPaymentDetails :{e}")


    def fetch_GeneralClientsInvestmentTotal(self):
        """
            This method fetches   general  total investment
            _Arg:none
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        SUM(Amount) AS TotalSavings
                    FROM
                        (
                            SELECT
                                A.ClientId,
                                C.FirstName,
                                C.SirName,
                                A.Amount,
                                B.BranchId,
                                M.BranchName
                            FROM
                                ClientsInvestmentPaymentDetails AS A
                            JOIN
                                (
                                    SELECT
                                        AccountNumber,
                                        FirstName,
                                        SirName
                                    FROM
                                        AccountsVault.BankAccount                   
                                ) AS C ON C.AccountNumber = A.ClientId
                            JOIN
                                (
                                    SELECT
                                        AccountNumber,
                                        BranchId
                                    FROM
                                        AccountsVault.branchDetails
                                    
                                ) AS B ON B.AccountNumber = A.ClientId
                            JOIN
                                (
                                    SELECT
                                        BranchId,
                                        BranchName
                                    FROM
                                        NisaBranches.Branches             
                                ) AS M ON M.BranchId = B.BranchId          
                        ) AS subquery;
                    
                                  
                """)
                data = self.cursor.fetchone()
                
                if data[0] != None:
                    return {"total":float(data[0])}
                else:
                    return {"total":0}
            else:
                raise Exception("cursor not initialised while fetching client total investment ")
        except Exception as e:
            raise Exception(f"error while fetching from  total ClientsInvestmentPaymentDetails :{e}")

    def fetch_GeneralClientsInvestmentDetails(self):
        """
            This method fetches recieved  general investment details
            _Arg:none
        """
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(A.Date),
                        A.ClientId,
                        C.FirstName,
                        C.SirName,
                        A.Amount,
                        B.BranchId,
                        M.BranchName
                    FROM
                        ClientsInvestmentPaymentDetails AS A
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount                   
                        ) AS C ON C.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                BranchId
                            FROM
                                AccountsVault.branchDetails
                             
                        ) AS B ON B.AccountNumber = A.ClientId
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches             
                        ) AS M ON M.BranchId = B.BranchId
                    ORDER BY B.BranchId 
                                  
                """)
                data = self.cursor.fetchall()
                if data:
                    return [{"date": str(obj[0]), 
                             "AccountNumber":obj[1], 
                             "fname":obj[2], 
                             "lName":obj[3], 
                             "Amount": float(obj[4]),
                             "BranchId":obj[5],
                             "BranchName":obj[6]
                             } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client investment details for a specific branch")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  for a specific  branch:{e}")








    def fetch_current_total_investments(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        SUM(Amount)
                    FROM
                        ClientsInvestmentPaymentDetails
                    WHERE
                        DATE(Date) =  %s  
                """,(current_date,))
                data = self.cursor.fetchone()
                return data
            else:
                raise Exception("cursor not initialised while fetching otal current investments")

        except Exception as e:
            raise Exception(f"error while fetching total current investments:{e}")


    def fetch_total_investments(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        SUM(Amount)
                    FROM
                        ClientsInvestmentPaymentDetails  
                """)
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"totalInvetment":float(data[0])}
                else:
                    return {"totalInvetment":0}
            else:
                raise Exception("cursor not initialised while fetching total investments")

        except Exception as e:
            raise Exception(f"error while fetching total investments:{e}")
        

    def fetch_total_security(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        SUM(TotalSecurity)
                    FROM
                        TotalLoanSecurity
                """) 
                data = self.cursor.fetchone()
                if data and data[0] !=  None:
                    return {"totalSecurity":float(data[0])}
                else:
                    return {"totalSecurity":0}
            else:
                raise Exception("cursor not initialised while fetching total_securitl")

        except Exception as e:
            raise Exception(f"error while fetching total_securitl:{e}")





    def fetch_General_ClientsInvestmentDetails(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                current_date = datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        DATE(A.Date),
                        A.ClientId,
                        C.FirstName,
                        C.SirName,
                        A.Amount
                    FROM
                        ClientsInvestmentPaymentDetails AS A
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount                   
                        ) AS C ON C.AccountNumber = A.ClientId 
                    WHERE
                        DATE(A.Date) = %s
                                  
                """,(current_date,))
                data = self.cursor.fetchall()
                if data:
                    return [{"date": str(obj[0]), "AccountNumber":obj[1], "fname":obj[2], "lName":obj[3], "Amount": float(obj[4])} for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client investment details for a specific employee")
        except Exception as e:
            raise Exception(f"error while fetching from  ClientsInvestmentPaymentDetails  for a specific employee table:{e}")







    def fetch_clients_current_penalties_overdue(self,clientId):
        self.client_id = clientId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        TotalOverDue,
                        TotalPenalty
                    FROM
                        TotalPenaltiesAndOverDues
                    WHERE
                        LoanId IN (
                                    SELECT
                                        LoanId
                                    FROM 
                                        registeredLoans
                                    WHERE
                                        ActiveStatus = "unfinished" AND 
                                        LoanId IN  (
                                                    SELECT 
                                                        LoanId 
                                                    FROM 
                                                        LoanDetails 
                                                    WHERE 
                                                        ClientID = %s
                                                ) 
                                    
                                )
                                    
                                    
                """,(self.client_id,))
        
                results = self.cursor.fetchone()
                return {'overdue':float(results[0]), 'penalty':float(results[1])}
        except Exception as e:
            raise Exception(f"error while fetching clients current penalties and overdues:{e}")
        finally:
            self.close_connection()

    def fetch_clients_penaltyoverdueDetails(self,clientId):
        self.client_id = clientId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        Date,
                        Commitment,
                        Paid,
                        OverDue,
                        Penalty
                    FROM
                        PenaltiesAndOverDues
                    WHERE
                        LoanId IN (
                                    SELECT
                                        LoanId
                                    FROM 
                                        registeredLoans
                                    WHERE
                                        ActiveStatus = "unfinished" AND 
                                        LoanId IN  (
                                                    SELECT 
                                                        LoanId 
                                                    FROM 
                                                        LoanDetails 
                                                    WHERE 
                                                        ClientID = %s
                                                ) 
                                    
                                )
                                    
                                    
                """,(self.client_id,))
        
                results = self.cursor.fetchall()
                formatted_data = []
                for row in results:
                    formatted_data.append({
                        'Date': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                        'Commitment': float(row[1]),
                        'Paid': float(row[2]),
                        'Overdue': float(row[3]),
                        'Penalty': float(row[4])
                    })
                return formatted_data
        except Exception as e:
            raise Exception(f"error while fetching clients current penalties and overdues:{e}")
        finally:
            self.close_connection()

    def fetch_clients_Total_penaltyoverdueDetails(self,clientId):
        self.client_id = clientId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        TotalOverDue,
                        TotalPenalty
                    FROM
                        TotalPenaltiesAndOverDues
                    WHERE
                        LoanId IN (
                                    SELECT
                                        LoanId
                                    FROM 
                                        registeredLoans
                                    WHERE
                                        ActiveStatus = "unfinished" AND 
                                        LoanId IN  (
                                                    SELECT 
                                                        LoanId 
                                                    FROM 
                                                        LoanDetails 
                                                    WHERE 
                                                        ClientID = %s
                                                ) 
                                    
                                )
                                    
                                    
                """,(self.client_id,))
        
                results = self.cursor.fetchone()
                return {'TotalOverDue':float(results[0]),'TotalPenalty':float(results[1])}
        except Exception as e:
            raise Exception(f"error while fetching clients current penalties and overdues:{e}")
        finally:
            self.close_connection()



    
    def fetch_clientsCurrentPortifolio(self,clientId):
        self.client_id = clientId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        COALESCE((
                            SELECT
                                Portifolio
                            FROM
                                LoanPaymentStatistics
                            WHERE
                                LoanId =(
                                            SELECT
                                                LoanId
                                            FROM 
                                                registeredLoans
                                            WHERE
                                                ActiveStatus = "unfinished" AND 
                                                LoanId IN  (
                                                            SELECT 
                                                                LoanId 
                                                            FROM 
                                                                LoanDetails 
                                                            WHERE 
                                                                ClientID = %s
                                                )
                                            
                                )
                            ORDER BY Date DESC
                            LIMIT 1      
                        ),
                        (
                            SELECT
                                Portifolio
                            FROM
                                LoanRepaymentScheduleDetails
                            WHERE
                                 LoanId =(
                                            SELECT
                                                LoanId
                                            FROM 
                                                registeredLoans
                                            WHERE
                                                ActiveStatus = "unfinished" AND 
                                                LoanId IN  (
                                                            SELECT 
                                                                LoanId 
                                                            FROM 
                                                                LoanDetails 
                                                            WHERE 
                                                                ClientID = %s
                                                )
                                            
                                )   
                                    
                                
                        )
                                    
                    ) as portifolio

                """,(self.client_id,self.client_id))
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return data[0]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised in fetch LoanPaymentStatistics")
        except Exception as e:
            raise Exception(f"error while fetching LoanPaymentStatistics:{e}")
        






    def fetch_officerCurrentPortifolio(self,officerID):
        self.employeeId = officerID
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                    
                        (SELECT   
                            SUM(A.Portifolio) AS portifolio
                        FROM
                            LoanRepaymentScheduleDetails AS A
                        JOIN
                            (
                                SELECT
                                    LoanId
                                FROM
                                    registeredLoans
                                WHERE
                                    ActiveStatus = "unfinished"        
                            ) AS B ON B.LoanId = A.LoanId
                        WHERE
                            A.LoanId IN (
                                        SELECT
                                            LoanId
                                        FROM
                                            LoanDetails
                                        WHERE
                                            OfficerId = %s
                                        )  ) - COALESCE((
                                                SELECT
                                                    sum(C.Paid)
                                                FROM
                                                    LoanPaymentStatistics AS C
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            LoanDetails
                                                        WHERE
                                                            OfficerId = %s
                                                    ) AS E ON E.LoanId = C.LoanId
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            registeredLoans
                                                        WHERE
                                                            ActiveStatus = "unfinished"

                                                    ) AS D ON D.LoanId =  C.LoanId
                                        
                                        ),0)

                """,(self.employeeId,self.employeeId))
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"totalPortifoli":data[0]}
                else:
                    return {"totalPortifoli":0}
            else:
                raise Exception("cursor not initialised in fetch LoanPaymentStatistics")
        except Exception as e:
            raise Exception(f"error while fetching LoanPaymentStatistics:{e}")
        

    def fetch_GeneralCurrentPortifolio(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
               
                self.cursor.execute("""
                    with notMadeAnyPaymentYet as (
                        SELECT
                            COALESCE(SUM(A.Portifolio),0) AS total_notYetmadePayment
                        FROM
                            LoanRepaymentScheduleDetails AS A
                        WHERE
                            A.LoanId  IN (
                                        SELECT
                                            LoanId
                                        FROM 
                                            registeredLoans
                                        WHERE
                                            ActiveStatus = "unfinished"
                                    ) AND NOT EXISTS(
                                        SELECT
                                            LoanId
                                        FROM
                                            ClientsLOANpaymentDETAILS AS B
                                        WHERE
                                            A.LoanId = B.LoanId
                                    )          
                    )
                                    

                    SELECT
                        (SELECT total_notYetmadePayment FROM notMadeAnyPaymentYet ) +
                        SUM(Portifolio)
                    FROM
                        (
                            SELECT
                                LoanId,
                                Date,
                                Portifolio,
                                ROW_NUMBER() OVER (PARTITION BY LoanId ORDER BY Date DESC)  AS rn
                            FROM
                                LoanPaymentStatistics             
                        ) AS latest_portifolio
                    WHERE rn = 1
                """)
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"totalPortifoli":float(data[0])} 
                else:
                    return {"totalPortifoli":0}
            else:
                raise Exception("cursor not initialised in GeneralCurrentPortifolio")
        except Exception as e:
            raise Exception(f"error while fetching GeneralCurrentPortifolio:{e}")


    
        
        
        



    def fetch_CurrentPortifolioForSpecificBranch(self,branchId):
        self.branchId = branchId
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                    
                        (SELECT   
                            SUM(A.Portifolio) AS portifolio
                        FROM
                            LoanRepaymentScheduleDetails AS A
                        JOIN
                            (
                                SELECT
                                    LoanId
                                FROM
                                    registeredLoans
                                WHERE
                                    ActiveStatus = "unfinished"        
                            ) AS B ON B.LoanId = A.LoanId
                        WHERE
                            A.LoanId IN (
                                        SELECT
                                            LoanId
                                        FROM
                                            LoanDetails
                                        WHERE
                                            BranchId = %s
                                        )  ) - COALESCE((
                                                SELECT
                                                    sum(C.Paid)
                                                FROM
                                                    LoanPaymentStatistics AS C
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            LoanDetails
                                                        WHERE
                                                            BranchId = %s
                                                    ) AS E ON E.LoanId = C.LoanId
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            registeredLoans
                                                        WHERE
                                                            ActiveStatus = "unfinished"

                                                    ) AS D ON D.LoanId =  C.LoanId
                                        
                                        ),0)

                """,(self.branchId,self.branchId))
                data = self.cursor.fetchone()
                if data[0] == None:
                    return {"totalPortifoli":0}
                    
                else:
                    return {"totalPortifoli":data[0]}
                    
            else:
                raise Exception("cursor not initialised in CurrentPortifolioForSpecificBranch")
        except Exception as e:
            raise Exception(f"error while fetching CurrentPortifolioForSpecificBranch:{e}")
        





        

    
    def fetch_branchOfficerdetails(self, branchId):
        try:
            self.cursor.execute("USE employeeDatabase")
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("""
                    SELECT
                        A.EmployeeId,
                        A.Firstname,
                        A.LastName,
                        E.BranchId
                    FROM
                        employeeDetails AS A
                    JOIN
                        WorkDetails AS E ON  E.EmployeeId = A.EmployeeId
                    WHERE
                        E.BranchId = %s               
                """,(branchId,))
                data = self.cursor.fetchall()
                if data:
                   return [{"employeeId":obj[0], "Fname":obj[1],"Lname":obj[2],"branchId":obj[3]} for obj in data]
                else:
                    return {"status":"no matching details"}
            else:
                raise Exception("cursor not initialised in branch officer details")
        except Exception as e:
            raise Exception(f"error while fetching Branch officer details :{e}")
        






    def fetch_GeneralCurrentPortifolioDetails(self):
        datedetails = datetime.now()
        currentDate = datedetails.strftime("%Y,%m,%d")
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        A.LoanId,
                        B.Portifolio,
                        C.ClientID,
                        C.BranchId,
                        D.FirstName,
                        D.SirName,
                        E.PhoneNumber,
                        F.BranchName
                    FROM
                        registeredLoans AS A
                    JOIN
                        (
                            SELECT
                                LoanId,
                                ClientID,
                                BranchId
                            FROM
                                LoanDetails              
                        )AS C ON C.LoanId = A.LoanId
                    JOIN
                        (
                            SELECT
                                DATE(Date),
                                LoanId,
                                Portifolio
                            FROM
                                LoanPaymentStatistics
                             
                        ) AS B ON B.LoanId = A.LoanId
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                FirstName,
                                SirName
                            FROM
                                AccountsVault.BankAccount               
                        ) AS D ON D.AccountNumber = C.ClientID
                    JOIN
                        (
                            SELECT
                                AccountNumber,
                                PhoneNumber
                            FROM
                                AccountsVault.ContactDetails               
                        ) AS E ON E.AccountNumber = C.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches         
                        )AS F ON F.BranchId = C.BranchId
                    
                    WHERE
                        A.ActiveStatus = "unfinished"
                    ORDER BY C.BranchId
                """)
                data = self.cursor.fetchall()
                return [{
                    "loanId":obj[0],
                    "portifolio":float(obj[1]),
                    "accountNumber":obj[2],
                    "branchId":obj[3],
                    "FirstName":obj[4],
                    "lastname":obj[5],
                    "phoneNumber":obj[6],
                    "BranchName":obj[7]

                } for obj in data]
            else:
                raise Exception("cursor not initialised in fetch general portifolio details")
        except Exception as e:
            raise Exception(f"error while fetching general portifolio details:{e}")
        

    def fetch_GeneralCurrentPrinciple(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                        SELECT
                            SUM(Principle)
                        FROM
                            registeredLoans
                        WHERE
                            ActiveStatus = "unfinished"
                """)
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"TOtalprinciple":data[0]}
                else:
                    return {"TOtalprinciple":0}
            else:
                raise Exception("cursor not initialised in fetching current principle")

        except Exception as e:
            raise Exception(f"error while fetching current principle:{e}")
        




    def fetch_CurrentPortifolio_FORgenralManager(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                    
                        (SELECT   
                            SUM(A.Portifolio) AS portifolio
                        FROM
                            LoanRepaymentScheduleDetails AS A
                        JOIN
                            (
                                SELECT
                                    LoanId
                                FROM
                                    registeredLoans
                                WHERE
                                    ActiveStatus = "unfinished"        
                            ) AS B ON B.LoanId = A.LoanId
                        WHERE
                            A.LoanId IN (
                                        SELECT
                                            LoanId
                                        FROM
                                            LoanDetails
                                    
                                        )  ) - COALESCE((
                                                SELECT
                                                    sum(C.Paid)
                                                FROM
                                                    LoanPaymentStatistics AS C
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            LoanDetails
                                                    ) AS E ON E.LoanId = C.LoanId
                                                JOIN
                                                    (
                                                        SELECT
                                                            LoanId
                                                        FROM
                                                            registeredLoans
                                                        WHERE
                                                            ActiveStatus = "unfinished"

                                                    ) AS D ON D.LoanId =  C.LoanId
                                        
                                        ),0)

                """)
                data = self.cursor.fetchall()
                return data
            else:
                raise Exception("cursor not initialised in fetch LoanPaymentStatistics")
        except Exception as e:
            raise Exception(f"error while fetching LoanPaymentStatistics:{e}")
        
    def fetchClientCurrentLoanPaymentDetails(self,clientId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        Date ,
                        LoanId ,
                        Commitment,
                        Paid ,
                        Balance,
                        Portifolio
                    FROM
                        LoanPaymentStatistics
                    WHERE
                        LoanId  = (SELECT
                                        LoanId 
                                    FROM
                                        LoanDetails
                                    WHERE
                                        ClientID = %s AND LoanId  IN (SELECT LoanId
                            FROM registeredLoans
                            WHERE ActiveStatus = 'unfinished')
                                )
                """,(clientId,))
                data = self.cursor.fetchall()
                print(f"pppo:{data}")
                return [{
                    "date":obj[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "loanId":obj[1],
                    "Commitment":float(obj[2]),
                    "Paid":float(obj[3]),
                    "Balance":float(obj[4]),
                    "Portifolio":float(obj[5])
                    
                    }for obj in data]
            else:
                raise Exception("cursor not initialised in fetching current loan payment details")
                
        except Exception as e:
            raise Exception(f"error while fetching current loan payment details:{e}")


    def fetchCollectionSheetDetails(self,employeeId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute(""" 


                         SELECT
                        s.LoanId,
                        s.DailCommitmentAmount,
                        D.ClientID,
                        D.OfficerId,
                        B.FirstName,
                        B.SirName,
                        W.Contact                              
                    FROM
                        LoanRepaymentScheduleDetails AS s
                    JOIN
                        (
                            SELECT
                                LoanId,
                                ClientID,
                                OfficerId
                            FROM
                                LoanDetails
                            WHERE
                                OfficerId = %s             
                        ) AS D ON D.LoanId = s.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                ActiveStatus
                                    
                            FROM
                                registeredLoans
                            WHERE
                                ActiveStatus = "unfinished"  
                        ) AS P ON P.LoanId = s.LoanId
                    JOIN
                        AccountsVault.BankAccount AS B ON B.AccountNumber = D.ClientID
                    JOIN
                        WorkDetails AS W ON  W.LoanId = s.LoanId         
                        
                """,(employeeId,))
                data = self.cursor.fetchall()
                return [ {"LoanId":obj[0],
                         "commitment":obj[1],
                         "AccountNumber":obj[2],
                         "creditOfficerId":obj[3],
                         "clientFName":obj[4],
                         "clientSName":obj[5],
                         "ClientPhonenumber":obj[6]
                         } for obj in data  ]
            else:
                raise Exception("cursor not initialised in fetching current loan payment details")
                
        except Exception as e:
            raise Exception(f"error while fetching current loan payment details:{e}")
        

    def fetchCollectionSheetDetailsForAspecificBranch(self,branchId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute(""" 


                    SELECT
                        s.LoanId,
                        s.DailCommitmentAmount,
                        D.ClientID,
                        D.BranchId,
                        B.FirstName,
                        B.SirName,
                        W.Contact,
                        M.BranchName                              
                    FROM
                        LoanRepaymentScheduleDetails AS s
                    JOIN
                        (
                            SELECT
                                LoanId,
                                ClientID,
                                BranchId
                            FROM
                                LoanDetails
                            WHERE
                                BranchId = %s             
                        ) AS D ON D.LoanId = s.LoanId
                    JOIN
                        (
                            SELECT
                                LoanId,
                                ActiveStatus
                                    
                            FROM
                                registeredLoans
                            WHERE
                                ActiveStatus = "unfinished"  
                        ) AS P ON P.LoanId = s.LoanId
                    JOIN
                        AccountsVault.BankAccount AS B ON B.AccountNumber = D.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches                                            
                        ) AS M ON M.BranchId = D.BranchId
                        
                    JOIN
                        WorkDetails AS W ON  W.LoanId = s.LoanId         
                        
                """,(branchId,))
                data = self.cursor.fetchall()
                return [ {"LoanId":obj[0],
                         "commitment":obj[1],
                         "AccountNumber":obj[2],
                         "creditOfficerId":obj[3],
                         "clientFName":obj[4],
                         "clientSName":obj[5],
                         "ClientPhonenumber":obj[6],
                         "Branchname":obj[7]
                         } for obj in data  ]
            else:
                raise Exception("cursor not initialised in fetching current loan payment details")
                
        except Exception as e:
            raise Exception(f"error while fetching current loan payment details:{e}")
        

    # def fetchClientLoanSecurityDetails(self,clientId):
    #     try:
    #         self.reconnect_if_needed()
    #         if self.cursor:
    #             self.cursor.execute("USE LoanApplications")
    #             self.cursor.execute("""
    #                 SELECT
    #                     sum(LoanSecurity) AS TOTAL_SECURITY
    #                 FROM
    #                     LoanRepaymentScheduleDetails
    #                 WHERE
    #                     LoanId IN (SELECT LoanId FROM LoanDetails WHERE  ClientID = %s          
    #                     )   
                        
    #             """,(clientId,))
    #             data = self.cursor.fetchone()
    #             return {"totalSecurity":data[0]}
    #         else:
    #             raise Exception("cursor not initialised in fetch client loan security details")
    #     except Exception as e:
    #         raise Exception(f"error while fetching client loan security details:{e}")

    
    
    def insert_into_ClientsLOANpaymentDETAILS(self,paymentDetails):
        self.loanId = paymentDetails["loanId"]
        self.amount = paymentDetails["amount"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO ClientsLOANpaymentDETAILS(
                        LoanId,
                        Amount                
                    ) VALUES(%s,%s)
                """, (self.loanId,self.amount))
                self.connection.commit()
            else:
                raise Exception("cursor not initialised in ClientsLOANpaymentDETAILS table")

        except Exception as e:
            raise Exception(f"error while inserting into ClientsLOANpaymentDETAILS :{e}")
        finally:
            self.close_connection()

    def get_current_Cleints_loan_Commitment_details(self, loan_id):
        """
            this methode fetches updated payment details
        """
        today = datetime.today().date()
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")

                self.cursor.execute("""
                    SELECT
                        M.DailCommitmentAmount
                    FROM
                        LoanRepaymentScheduleDetails AS M
                    WHERE
                        M.LoanId = %s AND M.LoanId IN (
                            SELECT A.LoanId
                            FROM registeredLoans AS A
                            WHERE A.ActiveStatus = 'unfinished'
                        )
                """,(loan_id,))
                data = self.cursor.fetchone()
                return float(data[0])
            raise ValueError("error while fetching clients loan commitment")

        except Exception as e:
            raise Exception(f"cursor failed to connect in get current client loan commitment :{e}")
        finally:
            self.close_connection()

    def calculate_clients_overdue_and_penalties(self, payment_details):
        
        loanId = payment_details['loanId']
        amount_paid = float(payment_details['paid'])
        commitment = float(payment_details['commitment'])
        if amount_paid >= commitment:
            penalty = 0
            overdue = 0
            return {
                'LoanId':loanId,
                'Paid':amount_paid,
                'Commitment':commitment,
                'OverDue':overdue,
                'Penalty':penalty

                }
        elif amount_paid < commitment:
            overdue = commitment - amount_paid
            penalty =  overdue * 0.1
            return {
                'LoanId':loanId,
                'Paid':amount_paid,
                'Commitment':commitment,
                'OverDue':overdue,
                'Penalty':penalty

                }
        
    
    def insert_clients_penalties_and_overdues(self, overdue_penalties):
        if overdue_penalties:
            loanId = overdue_penalties["LoanId"]
            commitment = overdue_penalties['Commitment']
            paid = overdue_penalties['Paid']
            overdue = overdue_penalties['OverDue']
            penalty = overdue_penalties['Penalty']
            try:
                self.reconnect_if_needed()
                if self.cursor:
                    self.cursor.execute("USE LoanApplications")
                    self.cursor.execute("""
                        INSERT INTO PenaltiesAndOverDues (
                            LoanId,
                            Commitment,
                            Paid,
                            OverDue,
                            Penalty
                        ) VALUES (%s, %s, %s, %s, %s)
                    """, (loanId,commitment,paid,overdue,penalty))
                    self.connection.commit()
                    return 1
               
            except Exception as e:
                raise Exception(f"Cursor failed in insert_clients_penalties_and_overdues: {e}")
            finally:
                self.close_connection()

    def total_penalties_and_oversdues_triger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS insertIntoPenaltiesAndOverdues")
                self.cursor.execute("""
                    CREATE TRIGGER insertIntoPenaltiesAndOverdues
                    AFTER INSERT ON PenaltiesAndOverDues
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO TotalPenaltiesAndOverDues(
                            LoanId,
                            TotalOverDue,
                            TotalPenalty           
                        )
                        VALUES(
                            NEW.LoanId,
                            NEW.OverDue,
                            NEW.Penalty           
                        )
                        ON DUPLICATE KEY UPDATE
                            TotalOverDue = COALESCE(TotalOverDue,0) + NEW.OverDue,
                            TotalPenalty  = COALESCE(TotalPenalty ,0) + NEW.Penalty;
                    END;
                        
                """)
            else:
                raise Exception("cursor not initialised in the total insertIntoPenaltiesAndOverdues trigger")
        except Exception as e:
            raise Exception(f"error while firing insertIntoPenaltiesAndOverdues trigger:{e}")
        finally:
            self.close_connection()



    def loanPaymenttrigger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS populateLoanStatistictTable")
                self.cursor.execute("""
                    CREATE TRIGGER populateLoanStatistictTable
                    AFTER INSERT ON ClientsLOANpaymentDETAILS
                    FOR EACH ROW
                    BEGIN          
                        INSERT INTO LoanPaymentStatistics(
                            LoanId,
                            Commitment,
                            Paid,
                            Balance,
                            Portifolio          
                        )
                        SELECT
                            NEW.LoanId AS LoanId,
                            db.DailCommitmentAmount AS Commitment,
                            NEW.Amount AS Paid,
                            db.DailCommitmentAmount - NEW.Amount AS Balance,
                            db.Portifolio - (SELECT COALESCE(SUM(Amount),0) FROM ClientsLOANpaymentDETAILS WHERE LoanId = NEW.LoanId)  AS Portifolio 
                        FROM
                            LoanRepaymentScheduleDetails as db
                        WHERE
                            db.LoanId = NEW.LoanId;
                    END; 
                      
                            
                """)
                self.connection.commit()
            else:
                raise Exception("cursor not initialised in loan payment trigger")
        except Exception as e:
            raise Exception(f"error in loan payment trigger:{e}")
        
    # def loanPaymenttrigger(self):
    #     try:
    #         self.reconnect_if_needed()
    #         if self.cursor:
    #             self.cursor.execute("USE LoanApplications")
    #             self.cursor.execute("DROP TRIGGER IF EXISTS populateLoanStatistictTable")
    #             self.cursor.execute("""
    #                 CREATE TRIGGER populateLoanStatistictTable
    #                 AFTER INSERT ON ClientsLOANpaymentDETAILS
    #                 FOR EACH ROW
    #                 BEGIN
    #                     DECLARE v_commitment DECIMAL(10,2);
    #                     DECLARE v_previous_portfolio DECIMAL(10,2);
    #                     DECLARE v_penalty DECIMAL(10,2);
    #                     DECLARE v_total_paid DECIMAL(10,2);
    #                     DECLARE v_portfolio DECIMAL(10,2);

    #                     -- Get commitment and previous portfolio
    #                     SELECT DailCommitmentAmount, Portifolio
    #                     INTO v_commitment, v_previous_portfolio
    #                     FROM LoanRepaymentScheduleDetails
    #                     WHERE LoanId = NEW.LoanId;

    #                     -- Get total penalties
    #                     SELECT COALESCE(TotalPenalty, 0) INTO v_penalty
    #                     FROM TotalPenaltiesAndOverDues
    #                     WHERE LoanId = NEW.LoanId;

    #                     -- Get total amount paid so far
    #                     SELECT COALESCE(SUM(Amount), 0) INTO v_total_paid
    #                     FROM ClientsLOANpaymentDETAILS
    #                     WHERE LoanId = NEW.LoanId;

    #                     -- Compute final portfolio
    #                     SET v_portfolio = COALESCE((v_previous_portfolio + v_penalty - v_total_paid),0);

    #                     -- Insert into statistics table
    #                     INSERT INTO LoanPaymentStatistics (
    #                         LoanId, Commitment, Paid, Balance, Portifolio
    #                     )
    #                     VALUES (
    #                         NEW.LoanId,
    #                         v_commitment,
    #                         NEW.Amount,
    #                         v_commitment - NEW.Amount,
    #                         v_portfolio
    #                     );
    #                 END;
                      
                            
    #             """)
    #             self.connection.commit()
    #         else:
    #             raise Exception("cursor not initialised in loan payment trigger")
    #     except Exception as e:
    #         raise Exception(f"error in loan payment trigger:{e}")
        
        

    def balancing(self,balancinDetails):
        self.loanId = balancinDetails["loanId"]
        self.balancingWith = balancinDetails["withdrawAccount"]
        self.BalancingAmount = balancinDetails["amount"]
        
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO LoanBalancing(
                        LoanId,
                        BalancingAmount,
                        AccountBalancedWith                
                    ) VALUES(%s,%s,%s)                    
                """,(self.loanId,self.BalancingAmount,self.balancingWith ))
                self.connection.commit()
                return True
            else:
                raise Exception("cursor not initialized while balancing the loan")
        except Exception as e:
            raise Exception(f"error while inserting into loan  balancing table:{e}")

    def fetchClientAccountnumber(self,loanId):
        try:
            self.reconnect_if_needed()
            self.cursor.execute("USE LoanApplications")
            self.cursor.execute("""
                SELECT ClientID FROM LoanDetails WHERE LoanId = %s
            """,(loanId,))
            data = self.cursor.fetchone()
            if data:
                return data[0]
        except Exception as e:
            raise Exception(f"error while fetching client account number given loan id:{e}")
    def fetchloanSecurity(self,clientId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        TotalSecurity
                    FROM
                        TotalLoanSecurity
                    WHERE
                        AccountNumber = %s 
                        
                """,(clientId,))
                data = self.cursor.fetchone()
                if data:
                    return data[0]
                else:
                    return 0
        except Exception as e:
            raise Exception(f"error while fetching client total loan security:{e}")
    
    def fetchClientInvestment(self,clientId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        TotalCurrentInvestment
                    FROM
                        ClientsTotalInvestment
                    WHERE
                        ClientId = %s 
                        
                """,(clientId,))
                data = self.cursor.fetchone()
               
                if data:
                    return data[0]
                else:
                    return 0
        except Exception as e:
            raise Exception(f"error while fetching client total investment:{e}")
        

    def calculateloanSecurity(self, loanId):
        self.reconnect_if_needed()
        accountNumber =  self.fetchClientAccountnumber(loanId=loanId)
        if accountNumber:
            loanSecurity = self.fetchloanSecurity(clientId=accountNumber)
            return loanSecurity
        
    def calculateClientInvestment(self, loanId):
        self.reconnect_if_needed()
        accountNumber =  self.fetchClientAccountnumber(loanId=loanId)
        if accountNumber:
            loanSecurity = self.fetchClientInvestment(clientId=accountNumber)
            return loanSecurity
    def compareLoanSecurityAndBalancingFigure(self, loanid, balancingAmount):

        currentLoanSecurity = self.calculateloanSecurity(loanId=loanid)
        if currentLoanSecurity >= int(balancingAmount):
            return True
        return False
    
    def compareClientInvestmentAndBalancingFigure(self, loanid, balancingAmount):

        currentClientInvestments = self.calculateClientInvestment(loanId=loanid)

        if int(currentClientInvestments)>= int(balancingAmount):
            return True
        return False
    
    def updateClientTotalLoanSecurityTrigerAfterBalancing(self, amount,loanId):
        try:
            
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE
                        TotalLoanSecurity 
                    SET
                        TotalSecurity = COALESCE(TotalSecurity,0) - %s
                    WHERE
                        AccountNumber = (SELECT ClientID FROM LoanDetails WHERE LoanId = %s)
                                                        
                """,(amount,loanId))
                self.connection.commit()
                return True
            else:
                    raise Exception("cursor not initialized while updating client loan security after  balancing ")
        except Exception as e:
            raise Exception(f"error while updating client loan security after balancing:{e}")

    
    def updateClientTotalLoanSecurityAfterWithdraw(self, amount,accountNumber):
        try:
            
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE
                        TotalLoanSecurity 
                    SET
                        TotalSecurity = COALESCE(TotalSecurity,0) - %s
                    WHERE
                        AccountNumber = %s
                                                        
                """,(amount,accountNumber))
                self.connection.commit()
                return True
            else:
                    raise Exception("cursor not initialized while updating client loan security after  withdraw")
        except Exception as e:
            raise Exception(f"error while updating client loan security after withdraw:{e}")

    def updateClientTotalInvestmentTrigerAfterBalancing(self, loanId, amount):
        try:
            
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE
                        ClientsTotalInvestment 
                    SET
                        TotalCurrentInvestment  = COALESCE(TotalCurrentInvestment,0) - %s
                    WHERE
                        ClientId = (SELECT ClientID FROM LoanDetails WHERE LoanId = %s)
                                                        
                """,(amount,loanId))
                self.connection.commit()
                return True
            else:
                    raise Exception("cursor not initialized while updating client total investment after  balancing ")
        except Exception as e:
            raise Exception(f"error while updating client total investment after balancing:{e}")

    def updateClientTotalInvestmentTrigerAfterWithdraw(self,accountNumber, amount):
        try:
            
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    UPDATE
                        ClientsTotalInvestment 
                    SET
                        TotalCurrentInvestment  = COALESCE(TotalCurrentInvestment,0) - %s
                    WHERE
                        ClientId = %s
                                                        
                """,(amount,accountNumber))
                self.connection.commit()
                return True
            else:
                    raise Exception("cursor not initialized while updating client total investment after  withdraw ")
        except Exception as e:
            raise Exception(f"error while updating client total investment after withdraw :{e}")

        


    def updatePortifolioAfterBalancingTrigger(self, loanId, amount):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO ClientsLOANpaymentDETAILS(
                            LoanId,
                            Amount            
                        )
                    VALUES(%s,%s)                                   
                """,(loanId,amount))
                self.connection.commit()
                return True
            else:
                raise Exception("cursor not initialised while updating Portifolio After Balancing")
        except Exception as e:
            raise Exception(f"error while updating Portifolio After Balancing:{e}")
        

    

    def registeredLoans(self):
        
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS registeredLoans(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        Principle DECIMAL(30,2),
                        InterestRate DECIMAL(12,1),
                        PaymentperiodinDays VARCHAR(500),
                        ActiveStatus VARCHAR(200)            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LoanRepaymentScheduleDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        Portifolio DECIMAL(12,2),
                        LoanSecurity DECIMAL(12,2),
                        DailCommitmentAmount DECIMAL(12,2) 
                        
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TotalLoanSecurity(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(300) PRIMARY KEY,
                        TotalSecurity DECIMAL(12,2)
                                        
                    )
                """)
            else:
                raise Exception("cursor not initialed while creating registeredLoans")
        except Exception as e:
            raise Exception(f"error while creating registeredLoans :{e}")
        finally:
            self.close_connection()
    def registeredLoanTriger(self):
        self.activateStatus = "unfinished"
        
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS registeredLoan")
                self.cursor.execute("""
                    CREATE TRIGGER registeredLoan
                    BEFORE INSERT ON DisbursementDetails
                    FOR EACH ROW 
                    BEGIN
                        
                        INSERT INTO registeredLoans (LoanId, Principle, InterestRate, PaymentperiodinDays, ActiveStatus)
                        SELECT
                            LoanId,
                            LoanAmountApproved,
                            InterestRateInPercentage,
                            LoanPeriodInDays,
                            'unfinished'
                        FROM approvedLoans
                        WHERE LoanId = NEW.LoanId;

                        INSERT INTO LoanRepaymentScheduleDetails (LoanId, Portifolio, LoanSecurity, DailCommitmentAmount)
                        SELECT
                            LoanId,
                            LoanAmountApproved * (1 + (InterestRateInPercentage / 100)) AS Portifolio,
                            LoanAmountApproved * 0.1 AS LoanSecurity,
                            (LoanAmountApproved * (1 + (InterestRateInPercentage / 100))) / LoanPeriodInDays AS DailCommitmentAmount
                        FROM approvedLoans
                        WHERE LoanId = NEW.LoanId;
                    END;
                """)
                self.connection.commit()

            else:
                raise Exception("cursor not initialized in register loan trigger")
        except Exception as e:
            raise Exception(f"error while registering comfirmed loans in register loan trigger:{e}")
        

    def LoanSecurityCalaculationTriggerAfterloanRegistration(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS loanSecurityCalaculationTrigger")
                self.cursor.execute("""
                    CREATE TRIGGER loanSecurityCalaculationTrigger
                    AFTER INSERT ON LoanRepaymentScheduleDetails
                    FOR EACH ROW 
                    BEGIN
                        INSERT INTO TotalLoanSecurity (AccountNumber, TotalSecurity)
                        VALUES (
                            (SELECT ClientID FROM LoanDetails WHERE LoanId = NEW.LoanId),
                            (SELECT LoanSecurity FROM LoanRepaymentScheduleDetails WHERE LoanId = NEW.LoanId)
                        )
                        ON DUPLICATE KEY UPDATE
                            TotalSecurity = TotalSecurity + (SELECT LoanSecurity FROM LoanRepaymentScheduleDetails WHERE LoanId = NEW.LoanId);
                    END;
                """)
                self.connection.commit()
            else:
                raise Exception("cursor not initialized in Loan Security Calaculation Trigger AfterloanR egistration trigger")
        except Exception as e:
            raise Exception(f"error while Loan Security Calaculation Trigger After loan Registration:{e}")
        
    

    def changeLoanRegistrationStatusTrigger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    DROP TRIGGER IF EXISTS changeLoanRegistrationStatus
                """)
                self.cursor.execute("""                    
                    CREATE TRIGGER changeLoanRegistrationStatus
                    BEFORE INSERT ON LoanPaymentStatistics
                    FOR EACH ROW
                    BEGIN
                        IF  NEW.Portifolio = 0 THEN
                                UPDATE registeredLoans
                                SET ActiveStatus = "Finshed"
                                WHERE
                                    LoanId = NEW.LoanId;
                        END IF;
                    END;
                                    
                """)
            else:
                raise Exception("cursor not initialized in changeLoan Registration Status Trigger")


        except Exception as e:
            raise Exception(f"error while changing loan regitration in changeLoanRegistrationStatusTrigger  :{e}")

        
    def fetchClientCreditDetails(self,clientId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                                                                      
                    SELECT
                        rl.Date,
                        rl.LoanId,
                        rl.Principle,
                        rl.InterestRate,
                        rl.PaymentperiodinDays,
                        LR.Portifolio,
                        LR.LoanSecurity,
                        LR.DailCommitmentAmount
                    FROM
                        registeredLoans AS rl
                    JOIN
                        LoanRepaymentScheduleDetails AS LR ON LR.LoanId = rl.LoanId
                    JOIN
                        (SELECT
                            LoanId 
                        FROM
                            LoanDetails
                        WHERE
                            ClientID = %s
                        )AS D ON D.LoanId = rl.LoanId
                    WHERE
                        rl.ActiveStatus = "unfinished"                      
                        
                """,(clientId,))
                data = self.cursor.fetchone()
                if data:
                    return {
                        "Date":data[0].strftime(("%Y-%m-%d")),
                        "loanId":data[1], 
                        "Principle":data[2],
                        "InterestRate":data[3],
                        "PaymentperiodinDays":data[4],
                        "Portifolio":data[5],
                        "LoanSecurity":data[6],
                        "DailCommitmentAmount": data[7]
                        }
                return []
            else:
                raise Exception("cursor not initialised in fetch clients credit details")
        except Exception as e:
            raise Exception(f"error in fetching client credit details: {e}")
        
    def fetchDebtedLoanAccountDetailForSpecificOfficer(self, officerId):
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.Amount,
                        B.ClientID,
                        C.FirstName,
                        C.SirName
                    FROM
                        ClientsLOANpaymentDETAILS AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        (SELECT
                            AccountNumber,
                            OfficerId
                        FROM
                            AccountsVault.branchDetails
                        WHERE
                            OfficerId = %s            
                        ) AS D ON D.AccountNumber = B.ClientID
                        
                    WHERE
                        DATE(r.Date) = %s
                         
                """,(officerId,current_date))
                data = self.cursor.fetchall()
                if data:
                    return [{"LoanId":obj[0],
                            "AmountPaid":float(obj[1]),
                            "AccountNumber":obj[2],
                            "fName":obj[3],
                            "lName":obj[4]
                            } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client debted loan accounts")
        except Exception as e:
            raise Exception(f"error while fetching client debted loan account details in fetchDebtedLoanAccountDetail method:{e}")
        


    def fetchDebtedLoanAccountDetailForSpecificBranch(self, branchId):
        """
            This method fetches recieved credit details for a branch
            _Arg:branchid,(str)
        """
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.Amount,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        D.BranchId,
                        M.BranchName
                    FROM
                        ClientsLOANpaymentDETAILS AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        (SELECT
                            AccountNumber,
                            BranchId
                        FROM
                            AccountsVault.branchDetails
                        WHERE
                            BranchId = %s            
                        ) AS D ON D.AccountNumber = B.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches             
                        ) AS M ON M.BranchId = D.BranchId
                        
                        
                    WHERE
                        DATE(r.Date) = %s
                         
                """,(branchId,current_date))
                data = self.cursor.fetchall()
                if data:
                    return [{"LoanId":obj[0],
                            "AmountPaid":float(obj[1]),
                            "AccountNumber":obj[2],
                            "fName":obj[3],
                            "lName":obj[4],
                            "BranchId":obj[5],
                            "Branchname":obj[6]
                            } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching client debted loan accounts for specfic branch")
        except Exception as e:
            raise Exception(f"error while fetching client debted loan account details in fetchDebtedLoanAccountDetailForSpecificBranch method :{e}")
        
    def fetchGeneralDebtedLoanAccountDetail(self):
        """
            This method fetches recieved credit details for a branch
            _Arg:branchid,(str)
        """
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        r.LoanId,
                        r.Amount,
                        B.ClientID,
                        C.FirstName,
                        C.SirName,
                        D.BranchId,
                        M.BranchName,
                        DATE(r.Date)
                    FROM
                        ClientsLOANpaymentDETAILS AS r
                    JOIN
                        (
                            SELECT
                                ClientID,
                                LoanId
                            FROM
                                LoanDetails                 
                        ) AS B ON B.LoanId = r.LoanId
                    JOIN
                        AccountsVault.BankAccount AS C ON C.AccountNumber = B.ClientID
                    JOIN
                        (SELECT
                            AccountNumber,
                            BranchId
                        FROM
                            AccountsVault.branchDetails           
                        ) AS D ON D.AccountNumber = B.ClientID
                    JOIN
                        (
                            SELECT
                                BranchId,
                                BranchName
                            FROM
                                NisaBranches.Branches             
                        ) AS M ON M.BranchId = D.BranchId
                        
                        
                    WHERE
                        DATE(r.Date) = %s
                         
                """,(current_date,))
                data = self.cursor.fetchall()
                if data:
                    return [{"LoanId":obj[0],
                            "AmountPaid":float(obj[1]),
                            "AccountNumber":obj[2],
                            "fName":obj[3],
                            "lName":obj[4],
                            "BranchId":obj[5],
                            "Branchname":obj[6],
                            "date":obj[7].strftime("%Y-%m-%d")
                            } for obj in data]
                else:
                    return 0
            else:
                raise Exception("cursor not initialised while fetching general client debted loan accounts")
        except Exception as e:
            raise Exception(f"error while fetching client debted loan account details in GeneralDebtedLoanAccountDetail method :{e}")
        
    def fetchTotalgeneralCreditCollections(self):
        """
            This method fetches total general credit collections
            _Arg:branchid,(str)
        """
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        SUM(Amount)
                    FROM
                        ClientsLOANpaymentDETAILS
                    WHERE
                        DATE(Date) = %s
                         
                """,(current_date,))
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return {"AmountPaid":float(data[0])}
                else:
                    return {"AmountPaid":0}
            else:
                raise Exception("cursor not initialised while fetching total general credit collections")
        except Exception as e:
            raise Exception(f"error while fetching total general credit collections in GeneralDebtedLoanAccountDetail method :{e}")
        









        


    def fetchLoanApplicationDetails(self):
        self.loanStatus = "notApproved"
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("USE AccountsVault")
                self.cursor.execute("""
                    SELECT
                        L.Date,
                        L.LoanId,
                        L.ClientID ,
                        L.BranchId ,
                        L.OfficerId,
                        L.LoanAmount,
                        L.InterestRateInPercentage,
                        L.LoanPeriodInDays,
                        R.ClientCurrentaddress,
                        R.DivisionCity,
                        R.District,
                        B.Occupation, 
                        B.WorkArea,
                        B.BusinessLocation,  
                        B.Contact,
                        B.BusinessImages,
                        Db.FirstName,
                        Db.SirName
                        
                    FROM
                        LoanApplications.LoanDetails AS L
                    JOIN LoanApplications.AddressDetails AS R ON R.LoanId = L.LoanId
                    JOIN LoanApplications.WorkDetails AS B ON B.LoanId = L.LoanId
                    JOIN AccountsVault.BankAccount AS Db on Db.AccountNumber = L.ClientID
                    WHERE
                        L.Status = %s
                """,(self.loanStatus,))
                data = self.cursor.fetchall()
                return [{
                    "Date":client[0].strftime('%Y-%m-%d %H:%M:%S'),
                    "LoanId":client[1],
                    "ClientId":client[2],
                    "BranchId":client[3],
                    "OfficerId":client[4],
                    "LoanAmount":client[5],
                    "intereRate":client[6],
                    "LoanPeriodInDays":client[7],
                    "ClientCurrentaddress":client[8],
                    "DivisionCity":client[9],
                    "District":client[10],
                    "Occupation":client[11],
                    "WorkArea":client[12],
                    "BusinessLocation":client[13],
                    "Contact":client[14],
                    "BusinessImages":client[15],
                    "FirstName":client[16],
                    "SirName":client[17]

                } for client in data]
            else:
                raise Exception("cursor not initialized in fetching loan application details")
        except Exception as e:
            raise Exception(f"error in fetch loan application details:{e}")
    def fetchApprovedLoandetails(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        
                        B.FirstName,
                        B.SirName,
                        C.BranchName,
                        E.Firstname,
                        E.LastName,
                        A.LoanId,
                        A.ClientID,
                        A.BranchId,
                        A.OfficerId,
                        A.LoanAmountAppliedFor,
                        A.LoanAmountApproved,
                        A.InterestRateInPercentage,
                        A.LoanPeriodInDays,
                        B.Date
                    FROM approvedLoans AS A
                    JOIN AccountsVault.BankAccount AS B ON B.AccountNumber = A.ClientID
                    JOIN NisaBranches.Branches AS C ON C.BranchId = A.BranchId
                    JOIN employeeDatabase.employeeDetails AS E ON E.EmployeeId = A.OfficerId
                    WHERE
                        NOT EXISTS (SELECT LoanId FROM DisbursementDetails AS D  WHERE A.LoanId = D.LoanId )

                    
                """)
                details = self.cursor.fetchall()
                return [{
                            "clientDetails":{
                                "AccountNumber":data[6],
                                "FirstName":data[0],
                                "SirName":data[1],
                                },
                            "branchDetails":{
                                "BranchId":data[7],
                                "BranchName":data[2],
                                "Firstname":data[3],
                                "LastName":data[4],
                                "OfficerId":data[8]
                            },
                            "loanDetails":{
                                "ApprovedDate":data[13].strftime('%Y-%m-%d %H:%M:%S'),
                                "LoanId":data[5],
                                "LoanAmountAppliedFor":data[9],
                                "LoanAmountApproved":data[10],
                                "InterestRateInPercentage":data[11],
                                "LoanPeriodInDays":data[12]
                            }
                    } for data in details]
            else:
                raise Exception("cursor not initialized in fetching approved loan details methode")

        except Exception as e:
            raise Exception(f"error while fetching approved loans details:{e}")
        finally:
            self.close_connection()

    def fetchApprovedLoandetailsForSpecificBranch(self,branchId):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT
                        B.FirstName,
                        B.SirName,
                        C.BranchName,
                        E.Firstname,
                        E.LastName,
                        A.LoanId,
                        A.ClientID,
                        A.BranchId,
                        A.OfficerId,
                        A.LoanAmountAppliedFor,
                        A.LoanAmountApproved,
                        A.InterestRateInPercentage,
                        A.LoanPeriodInDays
                    FROM approvedLoans AS A
                    JOIN AccountsVault.BankAccount AS B ON B.AccountNumber = A.ClientID
                    JOIN NisaBranches.Branches AS C ON C.BranchId = A.BranchId
                    JOIN employeeDatabase.employeeDetails AS E ON E.EmployeeId = A.OfficerId
                    WHERE
                        C.BranchId = %s
                        
                """,(branchId,))
                details = self.cursor.fetchall()
                return [{
                            "clientDetails":{
                                "AccountNumber":data[6],
                                "FirstName":data[0],
                                "SirName":data[1],
                                },
                            "branchDetails":{
                                "BranchId":data[7],
                                "BranchName":data[2],
                                "Firstname":data[3],
                                "LastName":data[4],
                                "OfficerId":data[8]
                            },
                            "loanDetails":{
                                "LoanId":data[5],
                                "LoanAmountAppliedFor":data[9],
                                "LoanAmountApproved":data[10],
                                "InterestRateInPercentage":data[11],
                                "LoanPeriodInDays":data[12]
                            }
                    } for data in details]
            else:
                raise Exception("cursor not initialized in fetching approved loan details methode")

        except Exception as e:
            raise Exception(f"error while fetching approved loans details:{e}")
        finally:
            self.close_connection()

    def withdraws(self):
        self.reconnect_if_needed()
        if self.cursor:
            self.cursor.execute("USE LoanApplications")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS LoanSecurityWithdraws(
                    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    AccountNumber VARCHAR(500),
                    Amount DECIMAL(30,2)         
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS InvestmentWithdraws(
                    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    AccountNumber VARCHAR(500),
                    Amount DECIMAL(30,2)               
                )
            """)

    def insertIntoLoanSecurityWithDraws(self, accountNumber,amount):
        """
            arg: accountNumber,amount
            return: success 
        
        """
        self.accountNumber = accountNumber
        self.amount = amount
        self.reconnect_if_needed
        if self.cursor:
            self.cursor.execute("USE LoanApplications")
            try:
                self.cursor.execute("""
                    INSERT INTO LoanSecurityWithdraws(AccountNumber,Amount) VALUES(%s,%s)
                """,self.accountNumber,self.amount)
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while inserting into LoanSecurityWithdraws:{e}")
            finally:
                self.close_connection()
                return "success"
        raise "mysql server not connected"
    def insertInvestmentWithDraws(self, accountNumber,amount):
        """
            arg: accountNumber,amount
            return: success 
        
        """
        self.accountNumber = accountNumber
        self.amount = amount
        self.reconnect_if_needed
        if self.cursor:
            try:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    INSERT INTO InvestmentWithdraws(AccountNumber,Amount) VALUES(%s,%s)
                """,self.accountNumber,self.amount)
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while inserting into InvestmentWithdraws:{e}")
            finally:
                self.close_connection()
                return "success"
        raise "mysql server not connected in inserting into InvestmentWithdraws"
    


class Penalties_Overdues(ConnectToMySql):
    def __init__(self):
        super().__init__()
    def get_who_paid_and_how_much_they_paid(self):
        """
            this methode get those who have to pay and they have paid
        """
        today = datetime.today().date()
        start_of_day = datetime.combine(today, time(0, 0))      # 00:00:00
        eight_pm = datetime.combine(today, time(20, 0)) 
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")

                self.cursor.execute("""
                    SELECT
                        C.LoanId,
                        C.Amount
                        
                    FROM
                        ClientsLOANpaymentDETAILS AS C
                    WHERE
                        C.Date BETWEEN %s AND %s
                        AND C.LoanId IN (
                            SELECT A.LoanId
                            FROM registeredLoans AS A
                            WHERE A.ActiveStatus = 'unfinished'
                        )
                """,(start_of_day, eight_pm))
                data = self.cursor.fetchall()
                paid_and_how_much = [{"LoanId": item[0], 'amount':item[1]} for item in data]
                made_loan_payments = {data[0] for data in data}
                return {'paid':made_loan_payments,'Details':paid_and_how_much}
            raise ValueError("error while fetching loan payments in penalties and overdue class")

        except Exception as e:
            raise Exception(f"cursor failed to connect in getting payment detaild under penalties and overdue :{e}")
        finally:
            self.close_connection()
    def get_who_suposed_to_pay_and_what_they_have_to_pay(self):
        """this method get those who have to pay and what they have to pay regardless"""
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    SELECT 
                        A.LoanId,
                        M.Commitment
                    FROM registeredLoans AS A
                    JOIN LoanPaymentStatistics AS M              
                    WHERE A.ActiveStatus = 'unfinished' AND A.LoanId = M.LoanId
                """)
                data = self.cursor.fetchall()
                who_and_how_much_to_pay = [{'loanId':data[0],'amount':float(data[1])} for data in data]
                who_have_to_pay = {item[0] for  item in data}
                return {'pay':who_have_to_pay,'details':who_and_how_much_to_pay}
            raise ValueError("error while getting who have to pay in penalties and overdue class")
        except Exception as e:
            return Exception(f"cursor failed to connect in getting those who have to pay under penalties and overdue class:{e}")
        finally:
            self.close_connection()

    def get_who_havent_paid(self, suposed_to_pay, those_who_have_paid):
        return suposed_to_pay.difference(those_who_have_paid)
    def get_current_Cleints_loan_Commitment_details(self, loan_id):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")

                self.cursor.execute("""
                    SELECT
                        M.DailCommitmentAmount
                    FROM
                        LoanRepaymentScheduleDetails AS M
                    WHERE
                        M.LoanId = %s AND M.LoanId IN (
                            SELECT A.LoanId
                            FROM registeredLoans AS A
                            WHERE A.ActiveStatus = 'unfinished'
                        )
                """,(loan_id,))
                data = self.cursor.fetchone()
                return float(data[0])
            raise ValueError("error while fetching clients loan commitment")

        except Exception as e:
            raise Exception(f"cursor failed to connect in get current client loan commitment :{e}")
        finally:
            self.close_connection()

    def calculate_overdue_and_penalties(self,loanId,Amount_paid, commitment):
        loanId = loanId
        commitment = float(commitment)
        amount_paid = float(Amount_paid)
        if amount_paid >= commitment:
            penalty = 0
            overdue = 0
            return {
                'LoanId':loanId,
                'Paid':amount_paid,
                'Commitment':commitment,
                'OverDue':overdue,
                'Penalty':penalty

                }
        elif amount_paid < commitment:
            overdue = commitment - amount_paid
            penalty =  overdue * 0.1
            return {
                'LoanId':loanId,
                'Paid':amount_paid,
                'Commitment':commitment,
                'OverDue':overdue,
                'Penalty':penalty

                }
        return 0
    
    
    def total_penalties_and_oversdues_triger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS insertIntoPenaltiesAndOverdues")
                self.cursor.execute("""
                    CREATE TRIGGER insertIntoPenaltiesAndOverdues
                    AFTER INSERT ON PenaltiesAndOverDues
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO TotalPenaltiesAndOverDues(
                            LoanId,
                            TotalOverDue,
                            TotalPenalty           
                        )
                        VALUES(
                            NEW.LoanId,
                            NEW.OverDue,
                            NEW.Penalty           
                        )
                        ON DUPLICATE KEY UPDATE
                            TotalOverDue = COALESCE(TotalOverDue,0) + NEW.OverDue,
                            TotalPenalty  = COALESCE(TotalPenalty ,0) + NEW.Penalty;
                    END;
                        
                """)
            else:
                raise Exception("cursor not initialised in the total insertIntoPenaltiesAndOverdues trigger")
        except Exception as e:
            raise Exception(f"error while firing insertIntoPenaltiesAndOverdues trigger:{e}")
        finally:
            self.close_connection()

    
    def insert_penalties_and_overdues(self,overdue_penalties):
        if overdue_penalties:
            loanId = overdue_penalties["LoanId"]
            commitment = overdue_penalties['Commitment']
            paid = overdue_penalties['Paid']
            overdue = overdue_penalties['OverDue']
            penalty = overdue_penalties['Penalty']
            try:
                self.reconnect_if_needed()
                if self.cursor:
                    self.cursor.execute("USE LoanApplications")
                    self.cursor.execute("""
                        INSERT INTO PenaltiesAndOverDues (
                            LoanId,
                            Commitment,
                            Paid,
                            OverDue,
                            Penalty
                        ) VALUES (%s, %s, %s, %s, %s)
                    """, (loanId,commitment,paid,overdue,penalty))
                    self.connection.commit()
                    return 1
                return 0
            except Exception as e:
                raise Exception(f"Cursor failed in insert_clients_penalties_and_overdues: {e}")
            finally:
                self.close_connection()

    def make_zero_payments(self):
        try:
            payment_exceptation_details = self.get_who_suposed_to_pay_and_what_they_have_to_pay()
            suposed_to_pay = payment_exceptation_details['pay']
            # print(f"supose:{suposed_to_pay}")
            actual_payments_made = self.get_who_paid_and_how_much_they_paid()
            who_paid  = actual_payments_made['paid']
            # print(f"paid:{who_paid}")
            who_is_to_pay_with_zero = self.get_who_havent_paid(suposed_to_pay=suposed_to_pay,those_who_have_paid=who_paid)
            # making payments
            # print(who_is_to_pay_with_zero)
            bank = BankingDataBase()
            bank.changeLoanRegistrationStatusTrigger()
            bank.loanPaymenttrigger()
            for loan in who_is_to_pay_with_zero:
                bank.insert_into_ClientsLOANpaymentDETAILS(paymentDetails={"loanId":loan,"amount":0})
                commitment = self.get_current_Cleints_loan_Commitment_details(loan_id=loan)
                penalty_overdue_data = self.calculate_overdue_and_penalties(loanId=loan, Amount_paid=0,commitment=commitment)
                self.total_penalties_and_oversdues_triger()
                self.insert_penalties_and_overdues(overdue_penalties=penalty_overdue_data)
            return True
        except Exception as e:
            raise Exception(f"error while making zero payments in make zero payments under penalties and overdue class:{e}")
    

    # def get_todays_payments_details(self):
    #     """
    #         this methode fetches updated payment details
    #     """
    #     today = datetime.today().date()
    #     start_of_day = datetime.combine(today, time(0, 0))      # 00:00:00
    #     eight_pm = datetime.combine(today, time(20, 0)) 
    #     try:
    #         self.reconnect_if_needed()
    #         if self.cursor:
    #             self.cursor.execute("USE LoanApplications")

    #             self.cursor.execute("""
    #                 SELECT
    #                     C.LoanId,
    #                     C.Amount,
    #                     M.Commitment
                        
    #                 FROM
    #                     ClientsLOANpaymentDETAILS AS C
    #                 JOIN (
    #                         SELECT LoanId, Commitment
    #                         FROM LoanPaymentStatistics
    #                         WHERE Date IN (
    #                             SELECT MAX(Date)
    #                             FROM LoanPaymentStatistics
    #                             GROUP BY LoanId
    #                         )
    #                     ) AS M ON M.LoanId = C.LoanId
    #                 WHERE
    #                     C.Date BETWEEN %s AND %s
    #                     AND C.LoanId IN (
    #                         SELECT A.LoanId
    #                         FROM registeredLoans AS A
    #                         WHERE A.ActiveStatus = 'unfinished'
    #                     )
    #             """,(start_of_day, eight_pm))
    #             data = self.cursor.fetchall()
    #             return [{'loanId':loan[0],'paid':float(loan[1] or 0 ),'commitment':float(loan[2] or 0)} for loan in data]
    #         raise ValueError("error while fetching updated loan payments in penalties and overdue class")

    #     except Exception as e:
    #         raise Exception(f"cursor failed to connect in get todays payments under penalties and overdue :{e}")
    #     finally:
    #         self.close_connection()
    

        



class AuthenticationDetails(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
    def employeeLoginCridentials(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS AuthenticationDb")
                self.cursor.execute("USE AuthenticationDb")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EmployeeLogindetails(
                        DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
                        EmployeeId VARCHAR(500) PRIMARY KEY,
                        Password  VARCHAR(500)              
                    )
                """)
                
        except Exception as e:
            raise Exception(f"error while creating login bd:{e}")
        finally:
            self.close_connection()

    def insert_into_employeeLoginCridentials(self,loginDetails):
        self.id = loginDetails["EmployeeId"]
        self.password = loginDetails["password"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE AuthenticationDb")
                self.cursor.execute("""
                    INSERT INTO EmployeeLogindetails(
                        EmployeeId,
                        Password               
                    )VALUES(%s,%s)
                """,(self.id, self.password))
                self.connection.commit()
            else:
                raise Exception("cursor not initialised while inserting into creditOfficers authentications")
        except Exception as e:
            raise Exception(f"error while inserting into creditOfficers authentication details:{e}")
        finally:
            self.close_connection()
    def update_EmployeePassword(self,employeeId, password):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE AuthenticationDb")
                self.cursor.execute("""
                    UPDATE EmployeeLogindetails
                    SET 
                        Password = %s
                    WHERE
                        EmployeeId = %s         

                """,(employeeId, password))
            else:
                raise Exception("cursor not intialised while updating employees password")

        except Exception as e:
            raise Exception(f"error while updating employee password:{e}")
        
    def is_authenticatedEmployee(self,EmployeeId,password):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE AuthenticationDb")
                self.cursor.execute("""
                    SELECT
                        A.EmployeeId,
                        A.Password
                    FROM
                        EmployeeLogindetails AS A
                    JOIN
                        employeeDatabase.employeeDetails AS E ON E.EmployeeId = A.EmployeeId
                    WHERE
                        A.EmployeeId = %s AND A.Password = %s
                """,(EmployeeId, password))
                data = self.cursor.fetchone()
                if data:
                    return True
                else:
                    return False
            else:
                raise Exception("cursor not initialised while authenticating employee")

        except Exception as e:
            raise Exception(f"error while authenticating Employee:{e}")
        finally:
            self.close_connection()
    
    def is_amanager(self, employeeId,mac):
        self.workStatus = "Activate"
        self.reconnect_if_needed()
        if self.cursor:
            try:
                self.cursor.execute("USE ManagersDatabase")
                self.cursor.execute("""
                    SELECT
                        EmployeeId,
                        Mac,
                        WorkStatus
                    FROM
                        ManagersDetails
                    WHERE
                        EmployeeId = %s AND Mac = %s AND WorkStatus = %s  
                """,(employeeId,mac,self.workStatus))
                data = self.cursor.fetchone()
                if data and data[0] != None:
                    return TRUE
                else:
                    return False

            except Exception as e:
                raise Exception(f"error while checking if employee is a manager:{e}")
        else:
            raise Exception("cursor not intialised while hecking if employee is a manager")
            
    



        

    




       
# employee = EmployeeDatabase()
# employee.create_database() 

# branchObj = Branches()
# branchObj.createDatabase()

# dept = Deptments()
# dept.createDatabase()


banking  = BankingDataBase()
# print(banking.penalties_overdue_trigger())
# banking.createAccountTable()
# banking.create_loanApplicationTAbles()
# banking.CreateapprovedLoans_tables()
# banking.Create_disbursement_table()
# banking.registeredLoans()
# banking.create_loanBalancingTable()
banking.clientloanpaymentsAndInvestmentTable()
# banking.withdraws()

# # creating a manager section

# idobj = GenerateIds()
# manager = ManagersDatabase()
# manager.creat_database()
# existingmac = manager.existingMAC()
# mac = idobj.managerAuthenticationCode(existingMac=existingmac)
# managerDetails = {"employeeId":"NE30748","mac":mac}
# manager.insert_into_database(managerDatils=managerDetails)


# penalties and overdue

# obj = Penalties_Overdues()
# d = obj.calculate_overdue_and_penalties()





auth = AuthenticationDetails()
auth.employeeLoginCridentials()