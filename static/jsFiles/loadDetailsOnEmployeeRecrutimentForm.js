async function fetchBranchDetails(){
    return await fetch("/employeeRecrutimentForm?type=branchDetails")
        .then(response =>{
            if(!response.ok){
                throw new Error("Error while fetching branch details")
            }
            return response.json()
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
}

async function genenrateBranchOptions(data){
    
    let html = ""

    for(let i = 0; i< data.length; i++){
        html += `
            <option data-branch-id=${data[i]["branchId"]}>${data[i]["branchName"]}</option>
        
        `
    }

    return html
}



async function fetchDeptDetails(){
    return await fetch("/employeeRecrutimentForm?type=getDeptdetails")
        .then(response =>{
            if(!response.ok){
                throw new Error("Error while fetching dept details")
            }
            return response.json()
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
}

function generatedeptOptiond(data){
    let html  = ""
    for (let i = 0; i< data.length; i ++){
        html += `
            <option data-dept-id=${data[i]["deptId"]}> ${data[i]["deptName"]}</option>
        `
    }
    return html
}





async function loadhtml(){
    const data = await fetchBranchDetails()
    const DeptData = await fetchDeptDetails()
    const html = await genenrateBranchOptions(data)
    const Depthtml = generatedeptOptiond(DeptData)
    document.getElementById("Branch")
        .innerHTML += html
    document.getElementById("deptOptions")
        .innerHTML += Depthtml
    
}

loadhtml()