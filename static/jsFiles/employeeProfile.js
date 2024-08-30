async function getEmployeedetails(){
    return await fetch("/employeeProfile?type=employeeDetails")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching employee Details")
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

async function getEmployeePicturedetails(){
    return await fetch("/employeeProfile?type=employeePic")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching employee picture Details")
            }
            return response.blob()
        })
        .then(data =>{
            return URL.createObjectURL(data)
        })
        .catch(error =>{
            console.log(error)
        })
}

function generateHtml(data, picUrl){
    const details = data[0]
    const html = `
        <div class="profile-header">
            <img src="${picUrl}" alt="Employee Photo" class="img-thumbnail" width="180" height="50">
            <div>
                <h1> ${details["Firstname"]} <span class="ml-2"></span> ${details["LastName"]} </h1>
                <p>Position: ${details["Role"]}</p>
                <p>Employee ID: ${details["EmployeeId"]}</p>
            </div>
        </div>
        <div class="section">
            <h2>Employment Information</h2>
            <div class="card">
                <div class="card-body">
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th>Branch</th>
                                <td>${details["BranchName"]}</td>
                            </tr>
                            <tr>
                                <th>Department</th>
                                <td>${details["Dept"]}</td>
                            </tr>
                            <tr>
                                <th>Salary</th>
                                <td>${details["Salary"]}</td>
                            </tr>

                            
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="section">
            <h2>Contact Information</h2>
            <div class="card">
                <div class="card-body">
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th>Phone Number</th>
                                <td>${details["PhoneNumber"]}</td>
                            </tr>
                            <tr>
                                <th>Email Address</th>
                                <td>${details["Email"]}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Personal Information</h2>
            <div class="card">
                <div class="card-body">
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th>Current Address</th>
                                <td>${details["CurrentAddress"]}</td>
                            </tr>
                            <tr>
                                <th>District</th>
                                <td>${details["District"]}</td>
                            </tr>
                            <tr>
                                <th>City/Devision</th>
                                <td>${details["City"]}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `
    return html

}

async function loadHtml(){
    const data = await getEmployeedetails();
    const picurl = await getEmployeePicturedetails();
    const detail = await generateHtml(data,picurl);
    document.getElementById("employeeDetails")
        .innerHTML = detail

}

loadHtml()

