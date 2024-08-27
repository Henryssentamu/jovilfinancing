function getEmployeeBranchUpdate() {
    const employeeId = document.getElementById("employeeId").value;
    const branchId = document.getElementById("branchId").value;
    return {"employeeId":employeeId, "branchId":branchId}
    
}

async function sendEmployeeBranchUpdateToServer(){
    let datails = await getEmployeeBranchUpdate()
    let data = {"type":"employeebranchUpdte", "data":datails}



    fetch("/employeeRecrutimentForm",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("server faced error while sending employeeBranch updates to server")
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
    document.getElementById("updateEmployeeBranch")
        .addEventListener("click",()=>{
            sendEmployeeBranchUpdateToServer()
            location.reload()
        })
}

trigger()

