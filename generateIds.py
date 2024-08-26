import secrets


class GenerateIds:
    def __init__(self) -> None:
        self.branchPrefix = "NB"
        self.EmployeePrefix = "NE"
        self.DeptPrefix = "ND"
        self.IdLength = 5

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

