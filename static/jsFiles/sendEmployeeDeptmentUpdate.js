function getEmployeeBranchUpdate() {
    const employeeId = document.getElementById("employeeId").value;
    const branchId = document.getElementById("deptId").value;
    const NewRole = document.getElementById("NewRole").value;
    return {"employeeId":employeeId, "deptId":branchId, "NewRole":NewRole}
    
}

async function sendEmployeeDeptUpdateToServer(){
    let datails = await getEmployeeBranchUpdate()
    let data = {"type":"employeeDeptmentUpdte", "data":datails}



    fetch("/employeeRecrutimentForm",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("server faced error while sending employee Dept updates to server")
        }
        return response.json()
    })
    .then(data =>{
        
    })
    .catch(error =>{
        console.log(error)
    })

}

function trigger(){
    document.getElementById("updateEmployeeDept")
        .addEventListener("click",()=>{
            sendEmployeeDeptUpdateToServer()
            location.reload()
        })
}

trigger()

