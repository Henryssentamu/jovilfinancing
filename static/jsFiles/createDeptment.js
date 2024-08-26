function sendDeptDetails(){
    document.getElementById("createDept")
        .addEventListener("click", (event)=>{
            event.preventDefault()
            const deptName = document.getElementById("deptName").value;
            const headOfDept = document.getElementById("headOfDept").value;
            const data = {
                "type":"deptCreation",
                "data":{"deptName":deptName, "headOfDept": headOfDept}
            };

            fetch("createDeptments",{
                method:"POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response =>{
                if(!response.ok){
                    throw new Error("error while sending deptment details to server")
                }
                return response.json()
            })
            .then(data =>{
                if(data["response"] === "succuse"){
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

sendDeptDetails()