async function fetchEmployeedetails () {
    return await fetch("/workersPage?type=employeeDetails")
        .then(response =>{
            if(! response.ok){
                throw new Error("error while fetching employee details")
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

function generatehtml(data){
    let html = "";
    data.forEach((obj,index) =>{
        html += `
            <tr>
                <td>
                    <a href="/employeeProfile" class=" btn btn-sm  nav-link" id="${index}" data-employee-id="${obj["EmployeeId"]}"> ${obj["Firstname"]} <span class="ml-2"></span> ${obj["LastName"]}</a>
                </td>
                <td> ${obj["Dept"]}</td>
                <td> ${obj["BranchName"]}</td>
                <td>${obj["PhoneNumber"]}</td>
                <td>${obj["Email"]}</td>
            </tr>       
        `
    })

    return html

}

async function loadDetails(){
    let data = await fetchEmployeedetails ();
    let generatedHtml = generatehtml(data);
    document.getElementById("employeeDetails")
        .innerHTML = generatedHtml
}

loadDetails()

