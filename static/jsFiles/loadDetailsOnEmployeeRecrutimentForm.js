fetch("/employeeRecrutimentForm?type=branchDetails")
    .then(response =>{
        if(!response.ok){
            throw new Error("Error while fetching branch details")
        }
        return response.json()
    })
    .then(data =>{
        console.log(data)
    })
    .catch(error =>{
        console.log(error)
    })