async function getGeneralPortifolioDetails(){
    return await fetch("/managrDashboard?type=portifolio")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching portifolio details")
            }
            return response.json()
            
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
};


async function getGeneralprincipleDetails(){
    return await fetch("/managrDashboard?type=principle")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching principle details")
            }
            return response.json()
            
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
};

async function getTotal_investments(){
    return await fetch("/managrDashboard?type=current_total_investment")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching current_total_investment")
            }
            return response.json()
            
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
};


async function getTotal_loanSecurity(){
    return await fetch("/managrDashboard?type=loanSecurity")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching total loanSecurity")
            }
            return response.json()
            
        })
        .then(data =>{
            return data
        })
        .catch(error =>{
            console.log(error)
        })
};

async function loaddetails() {
    const portifolio = await getGeneralPortifolioDetails();
    const principle = await getGeneralprincipleDetails();
    const total_investment = await getTotal_investments();
    const total_security = await getTotal_loanSecurity();
    document.getElementById("portifolio_value").innerHTML = portifolio["totalPortifoli"];
    document.getElementById("Principle_value").innerHTML = principle["TOtalprinciple"];
    document.getElementById("total_investments").innerHTML = total_investment["totalInvetment"];
    document.getElementById("total_security").innerHTML = total_security["totalSecurity"]
    
};
loaddetails()

