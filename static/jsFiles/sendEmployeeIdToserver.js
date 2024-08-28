function getEmployeeId(){
    let employeeId = ""
    document.addEventListener("click", ( event)=> {
        if(event.target && event.target.matches('a.nav-link')){
            const element = event.target;
            employeeId = element.getAttribute('data-employee-id');
            const data = {"type":"employeeId", "data":employeeId};

            fetch("/employeeProfile",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify(data)
            })
            .then(response =>{
                if(!response.ok){
                    throw new Error("error while sending EmployeeId to server from workerpage")
                }
                return response.json()
            })
            .then(data =>{
        
            } )
            .catch(error =>{
                console.log(error)
            })
        }
    })
    
}

