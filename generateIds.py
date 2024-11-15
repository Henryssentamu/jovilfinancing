import secrets


class GenerateIds:
    def __init__(self) -> None:
        self.branchPrefix = "NB"
        self.EmployeePrefix = "NE"
        self.DeptPrefix = "ND"
        self.loanIDprefix = "NL"
        self.macPrefix = "GM"
        self.IdLength = 5
        self.macLength = 10

    def branchId(self,existingBranchIDs):
        """_this methode is called whenever a new branch is created_
            Args:
                existingBrachIds (_set_): _set of existing branch ids_
        """
        self.existingBranchIds = existingBranchIDs
        number = str(secrets.randbelow(5 ** self.IdLength)).zfill(self.IdLength)
        id = f"{self.branchPrefix}{number}"
        if id not in self.existingBranchIds:
            return id
        else:
            return self.branchId(self,existingBranchIDs)
        
    def managerAuthenticationCode(self,existingMac):
        """_this methode is called whenever a new manager is created_
            Args:
                existingMac (_set_): _set of existing MAC_
        """
        if not isinstance(existingMac, set):
            raise TypeError("existingMac must be a set of existing MAC addresses.")
        
        self.existingMAC = existingMac
        number = str(secrets.randbelow(10 ** self.macLength)).zfill(self.macLength)
        id = f"{self.macPrefix}{number}"

        if id not in self.existingMAC:
            return id
        else:
            return self.managerAuthenticationCode(self,existingMac)



    def employeeId(self,existingEmployeeIDs):
        """_this methode is called whenever a new employee is registered_
            Args:
                existing employee Ids (_set_): _set of existing Employee Ids_
        """

        self.existingEmployeeIds = existingEmployeeIDs
        number = str(secrets.randbelow(10**self.IdLength)).zfill(self.IdLength)
        id = f"{self.EmployeePrefix}{number}"
        if id not in self.existingEmployeeIds:
            return id
        else:
            return self.employeeId(self,existingEmployeeIDs)
    def deptmentId(self,existingDeptIds):
        """_this methode is called whenever a new dept is created_
            Args:
                existing dept Ids (_set_): _set of existing dept Ids_
        """
        self.existingDeptIds = existingDeptIds
        number = str(secrets.randbelow(10**self.IdLength)).zfill(self.IdLength)
        id = f"{self.DeptPrefix}{number}"
        if id not in self.existingDeptIds:
            return id
        else:
            return self.deptmentId(existingDeptIds)
    def loanId(self,existingLoanIds):
        """_this method is called whenever a new loan application is need_
            Args:
                existing loanIdz(_set_):_set of existing loan idz
        """
        self.existloanIds = existingLoanIds
        number = str(secrets.randbelow(10**self.IdLength)).zfill(self.IdLength)
        id = f"{self.loanIDprefix}{number}"
        if id not in self.existloanIds:
            return id
        else:
            return self.loanId(existingLoanIds)


