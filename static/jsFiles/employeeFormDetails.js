function getinputs(){
    const formatedata = new FormData()

    formatedata.append("firstName", document.getElementById("firstName").value);
    formatedata.append("lastName",document.getElementById("lastName").value);
    formatedata.append("phoneNumber",document.getElementById("phone").value);
    formatedata.append("email",document.getElementById("email").value);
    formatedata.append("age",document.getElementById("age").value);
    formatedata.append("current_address",document.getElementById("address").value);
    formatedata.append("district",document.getElementById("state").value);
    formatedata.append("city",document.getElementById("city").value);
    formatedata.append("village",document.getElementById("zone").value);
    formatedata.append("Branch", document.getElementById("Branch").value);
    formatedata.append("dept",document.getElementById("deptOptions").value);
    formatedata.append("employeeType",document.getElementById("employeeType").value);
    formatedata.append("roleAsigned",document.getElementById("roleAsigned").value);
    formatedata.append("salary",document.getElementById("salary").value);
    formatedata.append("profilePicture",document.getElementById("profilePicture").files[0]);
    formatedata.append("documents",document.getElementById("academicPapers").files[0])

    return formatedata
}

function getSelectedBranch(){
    // Get the select element
    const selectElement = document.getElementById('Branch');
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const branchId = selectedOption.dataset.branchId;
    return branchId

}

function getSelectedDept(){
    const selectedElement = document.getElementById("deptOptions")
    const selectedoption = selectedElement.options[selectedElement.selectedIndex];
    const deptId = selectedoption.dataset.deptId
    return deptId
}

function sendTosever(){
    document.getElementById("submit")
        .addEventListener("click", async (event) =>{
            event.preventDefault()
            const data = await getinputs()
            const selectedBranch = await getSelectedBranch()
            const selectedDept =  await getSelectedDept()
            data.append("branchId",selectedBranch)
            data.append("deptId", selectedDept)
            fetch("/employeeRecrutimentForm",{
                method:"POST",
                body: data
            })

                .then(response =>{
                    if (!response.ok){
                        throw new Error("error while sending employee details to server")
                    }
                     return response.json()
                })
                .then(data =>{
                    if (data["response"] === "success"){
                        alert(data["response"])
                        location.reload()
                    }

                })
                .catch(error =>{
                    console.log(error)
                })

        })
}

sendTosever()