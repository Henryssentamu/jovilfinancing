import mysql.connector as sql

class ConnectToMySql:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
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
            
       
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    

class Acount(ConnectToMySql):
    def __init__(self, dataObject):
        super().__init__()
        self.data = dataObject
        if not self.cursor:
            raise Exception("Database cursor is not initialized. Check the database connection.")

    def create_Database(self):
        try:
            if self.cursor:
                self.cursor.execute("""
                    CREATE DATABASE IF NOT EXISTS Acount
                """)
            else:
                raise Exception("Cursor is not available.")
        except Exception as e:
            raise Exception(f"Error in create_Database: {e}")

    def create_account(self):
        if self.cursor:
            try:
                self.cursor.execute("USE Acount")
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS AccountOwner(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AccountNumber VARCHAR(200) PRIMARY KEY,
                        FirstName VARCHAR(500),
                        Sirname VARCHAR(500)              
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ContactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AcountNumber VARCHAR(500),
                        PhoneNumber VARCHAR(200),
                        FOREIGN KEY (AcountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL              
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS socialDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AcountNumber VARCHAR(500),
                        DateOfBirth  VARCHAR(100),
                        Gender VARCHAR(50),
                        Religion VARCHAR(200),
                        NinNumber VARCHAR(500),
                        FOREIGN KEY (AcountNumber) REFERENCES AccountOwner(AccountNumber)  ON DELETE SET NULL     
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS AddressDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AcountNumber VARCHAR(500),
                        PermanentAddress_village TEXT,
                        City_Devission TEXT,
                        District TEXT,  
                        FOREIGN KEY (AcountNumber) REFERENCES AccountOwner(AccountNumber) ON DELETE SET NULL            
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AcountNumber VARCHAR(500),
                        NinNumber VARCHAR(500),
                        FullName VARCHAR(500),
                        FOREIGN KEY (AcountNumber) REFERENCES AccountOwner(AccountNumber)  ON DELETE SET NULL                                
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NextOfKinContactDetails(
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        AcountNumber VARCHAR(500),
                        PhoneNumber VARCHAR(100),
                        Location VARCHAR(200),
                        FOREIGN KEY (AcountNumber) REFERENCES AccountOwner(AccountNumber)   ON DELETE SET NULL              
                    )
                """)
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while creating tables in Account class table: {e} ")
            finally:
                self.close_connection()
        else:
            raise Exception("Cursor is not available to create tables.")
        
    def update_phoneNumber(self,accountNumber,phoneNumber):
        if self.cursor:
            try:
                self.cursor.execute("USE Acount")
                update_query = """
                        UPDATE ContactDetails
                        SET PhoneNumber = %s
                        WHERE AcountNumber = %s
                    """
                self.execute(update_query, (phoneNumber,accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating phone numer:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not availabe to update phone number:")
        
    def update_AddressDetails(self,accountNumber,locationDetails):
        PermanentAddress = locationDetails["PermanentAddress "]
        CityDevission = locationDetails["city"]
        District = locationDetails["District"]
        if self.cursor:
            try:
                self.cursor.execute("USE Acount")
                update_query = """
                        UPDATE AddressDetails
                        SET PermanentAddress_village = %s
                        SET City_Devission = %s
                        SET District = %s
                        WHERE AcountNumber = %s

                    """
                self.execute(update_query, (PermanentAddress,CityDevission, District, accountNumber))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while updating address details:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not availabe to update phone number:")
        
    def update_nextOfKin(self, accountNumber, nextOfKinDetailsObject):
        fullname = nextOfKinDetailsObject["FullName"]
        Ninnumber =  nextOfKinDetailsObject["NinNumber"]
        PhoneNumber = nextOfKinDetailsObject["PhoneNumber"]
        Location = nextOfKinDetailsObject["PhoneNumber"]

        if self.cursor:
            try:
                self.cursor.execute(" USE Acount")
                name_querry = """
                    UPDATE NextOfKinDetails
                    SET FullName  = %s
                    SET NinNumber = %s
                    WHERE
                        AcountNumber = %s
                """

                contact_querry = """
                    UPDATE NextOfKinContactDetails
                    SET  PhoneNumber = %s
                    SET Location = %s
                    WHERE
                        AcountNumber = %s

                """
                self.cursor.execute(name_querry,(fullname,Ninnumber, accountNumber))
                self.cursor.execute(contact_querry,(PhoneNumber,Location))
                self.connection.commit()
            except Exception as e:
                raise Exception(f" error while updating next of kin details : {e}")
        else:
            raise Exception("cursor not availabe to update next of kin")
    def delete_account(self, accountNumber):
        if self.cursor:
            try:
                self.execute("USE  Acount ")
                delet_querry = " DELETE FROM AccountOwner  WHERE AcountNumber =%s"
                self.cursor.execute(delet_querry,(accountNumber,))
                self.connection.commit()
            except Exception as e:
                raise Exception(f"error while deleting account:{e}")
            finally:
                self.close_connection()
        else:
            raise Exception("cursor not available to delete account number")

    



obj = {
    "name":"henry"
}

ac = Acount(dataObject=obj)
ac.create_Database()
ac.create_account()


