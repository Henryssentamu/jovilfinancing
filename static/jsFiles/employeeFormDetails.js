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
    formatedata.append("dept",document.getElementById("department").value);
    formatedata.append("employeeType",document.getElementById("employeeType").value);
    formatedata.append("roleAsigned",document.getElementById("roleAsigned").value);
    formatedata.append("salary",document.getElementById("salary").value);
    formatedata.append("documents",document.getElementById("academicPapers").files[0])

    return formatedata
}


function sendTosever(){
    document.getElementById("submit")
        .addEventListener("click", async (event) =>{
            event.preventDefault()
            const data = getinputs()

            await fetch("/employeeRecrutimentForm",{
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
                    }

                })
                .catch(error =>{
                    console.log(error)
                })

        })
}

sendTosever()