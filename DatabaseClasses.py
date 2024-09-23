
import mysql.connector as sql


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
                        CREATE TABLE IF NOT EXISTS ContactDetails(
                            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            AccountNumber VARCHAR(500),
                            CurrentAddress VARCHAR(300),
                            CityDivision VARCHAR(300),
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
        self.CurrentAddress = accountObject["CurrentAddress"]
        self.CityDivision = accountObject["CityDivision"]
        self.District = accountObject["District"]
        self.PhoneNumber = accountObject["PhoneNumber"]
       
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
                    INSERT INTO ContactDetails(
                        AccountNumber,
                        CurrentAddress,
                        CityDivision,
                        District,
                        PhoneNumber                
                    ) VALUES(%s,%s,%s,%s,%s)
                """,(self.AccountNumber,self.CurrentAddress,self.CityDivision, self.District,self.PhoneNumber))
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
                        C.CurrentAddress,
                        C.CityDivision,
                        C.District,
                        C.PhoneNumber,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN ContactDetails AS C ON C.AccountNumber = B.AccountNumber
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
                                "CurrentAddress":obj[7],
                                "CityDivision":obj[8],
                                "District":obj[9],
                                "PhoneNumber":obj[10],
                                "nextOfKinDetails":{
                                    "FirstName":obj[11],
                                    "SirName":obj[12],
                                    "PhoneNumber":obj[13],
                                    "Location":obj[14]
                                },
                                "AccountOwnerPic":obj[15],
                                "branchDetails":{
                                    "BranchId":obj[16],
                                    "officerId":obj[17]
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
                        C.CurrentAddress,
                        C.CityDivision,
                        C.District,
                        C.PhoneNumber,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN ContactDetails AS C ON C.AccountNumber = B.AccountNumber
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
                                "CurrentAddress":obj[7],
                                "CityDivision":obj[8],
                                "District":obj[9],
                                "PhoneNumber":obj[10],
                                "nextOfKinDetails":{
                                    "FirstName":obj[11],
                                    "SirName":obj[12],
                                    "PhoneNumber":obj[13],
                                    "Location":obj[14]
                                },
                                "AccountOwnerPic":obj[15],
                                "branchDetails":{
                                    "BranchId":obj[16],
                                    "officerId":obj[17]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")




    def fetchAllClientAccountDetailsForSpecificEmployee(self, employeeId):
        """_This method fetches all clients details for specific branch_
            _Args:
                _branchId (str)_
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
                        C.CurrentAddress,
                        C.CityDivision,
                        C.District,
                        C.PhoneNumber,
                        N.FirstName,
                        N.SirName,
                        N.PhoneNumber,
                        N.Location,
                        T.Photo ownerpic,
                        D.BranchId,
                        D.OfficerId
                    FROM
                        BankAccount AS B
                    JOIN AccountSocialDetails AS S ON S.AccountNumber = B.AccountNumber
                    JOIN AccountPersonalDetails AS P ON P.AccountNumber = B.AccountNumber
                    JOIN ContactDetails AS C ON C.AccountNumber = B.AccountNumber
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
                                "CurrentAddress":obj[7],
                                "CityDivision":obj[8],
                                "District":obj[9],
                                "PhoneNumber":obj[10],
                                "nextOfKinDetails":{
                                    "FirstName":obj[11],
                                    "SirName":obj[12],
                                    "PhoneNumber":obj[13],
                                    "Location":obj[14]
                                },
                                "AccountOwnerPic":obj[15],
                                "branchDetails":{
                                    "BranchId":obj[16],
                                    "officerId":obj[17]
                                }
                            } for obj in data]
            except Exception as e:
                raise Exception(f"error while fetching all client's details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not initalised in fetching all clients details")






    
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
                        FOREIGN KEY(LoanId) REFERENCES LoanDetails(LoanId)
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
                        FOREIGN KEY(LoanId) REFERENCES LoanDetails(LoanId)
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
                        LoanAmountAppliedFor VARCHAR(300),
                        LoanAmountApproved VARCHAR(300),
                        InterestRateInPercentage VARCHAR(50),
                        LoanPeriodInDays VARCHAR(50)               
                    )
                """)
            else:
                raise Exception("cursor not initialized while creating approved loan tables")
        except Exception as e:
            raise Exception(f"error while creating approved loan tables:{e}")


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
                self.cursor.execute("DROP TRIGGER IF EXISTS loanApproved")
                self.cursor.execute("""
                    CREATE TRIGGER loanApproved
                    AFTER UPDATE ON LoanDetails
                    FOR EACH ROW
                    BEGIN
                        IF NEW.Status = 'approved' THEN
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
                        END IF;
                    END
                """)
                
                self.connection.commit()
            else:
                raise Exception("cursor not initialised in the trigger loan approvel status")
        except Exception as e:
            raise Exception(f"error while trigger loan approvel status:{e}")
        
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

    def registeredLoans(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS registeredLoans(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        Principle VARCHAR(500),
                        InterestRate VARCHAR(500),
                        PaymentperiodinDays VARCHAR(500)            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LoanRepaymentScheduleDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        LoanId VARCHAR(500) PRIMARY KEY,
                        Portifolio TEXT,
                        LoanSecurity TEXT,
                        DailCommitmentAmount TEXT 
                        
                    )
                """)
            else:
                raise Exception("cursor not initialed while creating registeredLoans")
        except Exception as e:
            raise Exception(f"error while creating registeredLoans :{e}")
        finally:
            self.close_connection()
    def registeredLoanTriger(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE LoanApplications")
                self.cursor.execute("DROP TRIGGER IF EXISTS registeredLoan")
                self.cursor.execute("""
                    CREATE TRIGGER registeredLoan
                    AFTER INSERT ON DisbursementDetails
                    FOR EACH ROW 
                    BEGIN 
                        INSERT INTO registeredLoans(LoanId,Principle,InterestRate,PaymentperiodinDays)
                        SELECT
                            LoanId,
                            LoanAmountApproved,
                            InterestRateInPercentage,
                            LoanPeriodInDays
                        FROM approvedLoans
                        WHERE 
                            LoanId = NEW.LoanId;
                                    
                        INSERT INTO LoanRepaymentScheduleDetails(LoanId,Portifolio,LoanSecurity,DailCommitmentAmount)
                        SELECT
                            LoanId,
                            LoanAmountApproved * (1 + (InterestRateInPercentage / 100) ) AS Portifolio,
                            LoanAmountApproved * 0.1 AS LoanSecurity,
                            (LoanAmountApproved * (1 + (InterestRateInPercentage / 100) )) / LoanPeriodInDays AS DailCommitmentAmount
                        FROM approvedLoans
                        WHERE 
                            LoanId = NEW.LoanId;
                            
                    END;
                                    
                """)
                self.connection.commit()
            else:
                raise Exception("cursor not initialized in register loan trigger")
        except Exception as e:
            raise Exception(f"error while registering comfirmed loans in register loan trigger:{e}")
        
    def calculateLoanDetails(self):
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientRegisteredLoandetails(
                                    
                    )
                """)
            else:
                raise Exception("cursor not initialised while creating clientRegisteredLoandetails")
        except Exception as e:
            raise Exception(f"error while creating clientRegisteredLoandetails:{e}")
        

        


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
                    LEFT JOIN LoanApplications.DisbursementDetails AS O ON O.LoanId = A.LoanId
                    WHERE
                        O.LoanId IS NULL
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
    



        

    




       
# employee = EmployeeDatabase()
# employee.create_database() 

# branchObj = Branches()
# branchObj.createDatabase()

# dept = Deptments()
# dept.createDatabase()


# banking  = BankingDataBase()
# banking.createAccountTable()
# banking.create_loanApplicationTAbles()
# banking.CreateapprovedLoans_tables()
# banking.Create_disbursement_table()
# banking.registeredLoans()


# auth = AuthenticationDetails()
# auth.employeeLoginCridentials()