function sendbranchDetails(){
    document.getElementById("createbranch")
        .addEventListener("click", (event)=>{
            event.preventDefault()
            const branchName = document.getElementById("branchName").value;
            const branchLocation = document.getElementById("branchLocation").value;
            const branchManager = document.getElementById("branchManager").value;
            const data = {
                "type":"branchCreation",
                "data":{"branchName":branchName, "Loction":branchLocation, "branchManager": branchManager}
            };

            fetch("createBranch",{
                method:"POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response =>{
                if(!response.ok){
                    throw new Error("error while sending branch details to server")
                }
                return response.json()
            })
            .then(data =>{
                if(data["response"] === "success"){
                    alert(data["response"])
                }
                else{
                    alert("contact system admin")
                }
            })
            .catch(error =>{
                alert(error)
            })

        })
}

sendbranchDetails()