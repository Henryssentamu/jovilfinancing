import mysql.connector as sql

from mainproject import branch

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
                        AccountNumber VARCHAR(500),
                        PhoneNumber VARCHAR(200),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL              
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS socialDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
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
                        AccountNumber VARCHAR(500),
                        PermanentAddress_village TEXT,
                        City_Devission TEXT,
                        District TEXT,  
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
                        NinNumber VARCHAR(500),
                        FullName VARCHAR(500),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)  ON DELETE SET NULL                                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinContactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
                        PhoneNumber VARCHAR(100),
                        Location VARCHAR(200),
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL              
                    )
                """)

                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pictures(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
                        OwnerPic LONGBLOB NOT NULL,
                        FOREIGN KEY (AccountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL
                        
                    )   
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS branchDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(500),
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
                    SELECT AccountNumber FROM AccountOwner
                """)
                accounts = self.cursor.fetchall()
                self.close_connection()
            except Exception as e:
                raise Exception(f"error while fetching existing accounts: {e}")
            return { accountObj[0] for accountObj in accounts}
        

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
                        BranchId VARCHAR(300),
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
        self.BranchId = branchObject["branchId"]
        self.BranchName = branchObject["branchName"]
        self.BranchManager = branchObject["BranchManager"]
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
            except Exception as e:
                raise Exception(f" error while inserting into NiceBranches tables:{e}")
            
    def update_branchManager(self, employeeId, branchId):
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
            except Exception as e:
                raise Exception(f"error while updating branch manager:{e}")
            

    def DeleteBranch(self,branchId):
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

        
            

