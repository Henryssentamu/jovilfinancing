
from DatabaseClasses import ConnectToMySql


class Authenticate(ConnectToMySql):
    def __init__(self) -> None:
        super().__init__()
    def GeneralManager(self, loginDetails ):
        self.employeeId = loginDetails["id"]
        self.password = loginDetails["password"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE ")
            else:
                raise Exception("cursor not initialised while fetching general managers login details")

        except Exception as e:
            raise Exception(f"error while fetching general managers authentication details:{e}")
        
    def CreditOfficer(self, loginDetails ):
        self.employeeId = loginDetails["id"]
        self.password = loginDetails["password"]
        try:
            self.reconnect_if_needed()
            if self.cursor:
                self.cursor.execute("USE employeeDatabase")
                self.cursor.execute("""
                    SELECT:
                """)
            else:
                raise Exception("cursor not initialised while fetching general managers login details")

        except Exception as e:
            raise Exception(f"error while fetching general managers authentication details:{e}")

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
