async  function fetchClientDetails(){
    return await  fetch("/clientProfile?type=clientDetails")
        .then(response =>{
            if (!response.ok){
                throw new Error("server error while fetching client details")
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

async function fetchCreditdetails() {
    return await fetch("/clientProfile?type=clientCreditdetails")
    .then(response =>{
        if (!response.ok){
            throw new Error("server error while fetching client credit details")
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

async function fetchClientPortifolio() {
    return await fetch("/clientProfile?type=clientPortifolio")
    .then(response =>{
        if (!response.ok){
            throw new Error("server error while fetching client credit details")
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



async function fetchLoanSecurity() {
    return fetch("/clientProfile?type=clientLoanSecurity")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching client loan security details")
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

async function fetchClientInvestment() {
    return fetch("/clientProfile?type=investments")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching clients investments")
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

function sendLoanIdForPayment(id){ 
    fetch("/Makepayments",{
        method:"POST",
        headers:{
            "Content-type":"application/json"
        },
        body:JSON.stringify({"type": "loanpayment","loanId":id})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("server erroe while sending loan id on payment route")
        }
        return response.json()
    })
    .then(data =>{
        if(data["response"] === "recieved"){
            window.location.href = "/Makepayments"
        }
    })
    .catch(error =>{
        console.log(error)
    })


}

function sendLoanIdForPenaltyPayment(id){ 
    fetch("/payPenalty",{
        method:"POST",
        headers:{
            "Content-type":"application/json"
        },
        body:JSON.stringify({"type": "penaltyPayment","loanId":id})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("server erroe while sending loan id on payment route")
        }
        return response.json()
    })
    .then(data =>{
        if(data["response"] === "recieved"){
            window.location.href = "/payPenalty"
        }
    })
    .catch(error =>{
        console.log(error)
    })


}

function generatePaybutton(data){
    return `
        <div>
            <a class="btn btn-success" onclick="sendLoanIdForPayment('${data["loanId"]}')">Make loan payment</a>
            <a class="btn btn-outline-success" onclick="sendLoanIdForPenaltyPayment('${data["loanId"]}')">Pay Penalties</a>
        </div>
    `

}

function generateInvestmentButton(data){
    var html = "";
    if(data){
        data.forEach((obj)=>{
            html += `<a class="btn btn-primary" onclick="sendClientAccountNumberForInvestment('${obj["AccountNumber"]}')">Make An Investment</a>`

        })
    }
    return html
}

function sendClientAccountNumberForInvestment(accountnumber){ 
    fetch("/Investmentpayments",{
        method:"POST",
        headers:{
            "Content-type":"application/json"
        },
        body:JSON.stringify({"type": "investment","accountnumber":accountnumber})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("server erroe while sending accountnumber on investment payment route")
        }
        return response.json()
    })
    .then(data =>{
        if(data["response"] === "recieved"){
            window.location.href = "/Investmentpayments"
        }
    })
    .catch(error =>{
        console.log(error)
    })


}

async function fetchClientTotalPenaltiesAndOverdue() {
            return await fetch("/clientProfile?type=clientTotalpenaltiesOverdue")
            .then(response =>{
                if (!response.ok){
                    throw new Error("server error while fetching client credit details")
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

function generateCreditdetails(data) {
    let html = "";
    if (data) {
        html += `
        <tr>
            <td>${data["Date"] || 'No Active Loan For This Client'} </td>  
            <td>Daily</td> 
            <td>${data["Principle"] || ''}</td>
            <td>${data["InterestRate"] || ''}%</td>
            <td>${data["Portifolio"] || ''}</td>
            <td>${data["PaymentperiodinDays"] || ''} days</td>
            <td>${data["DailCommitmentAmount"] || ''}</td>
        </tr>
    `;
    } else {
        html += "<div>This Client has No Active Loan</div>";
    }

    return html;
}



function generatepersonalHtml(data) {
    var html = "";
    if(data && data.length > 0){
        data.forEach(obj =>{
            html += `
                <div class="row">
                    <div class="col">
                        <img src="../static/${obj["AccountOwnerPic"]}" alt="owners pic" class="img-thumbnail img-fluid">
                    </div>
                    <div class="col">
                        <div class="row bg-secondary text-white">
                            <div class="col">Name</div>
                            <div class="col">${obj["FirstName"]} <span> </span> ${obj["SirName"]} </div>
                        </div>
                        <div class="row bg-success text-white">
                            <div class="col"> Account Number</div>
                            <div onclick="copyToClipboard('${obj["AccountNumber"]}')"  style="cursor: pointer;" title="Click to copy" class="col"> ${obj["AccountNumber"]}</div>
                            
                            
                            
                            
                        
                        </div>
                        
    
                    </div>
                </div>
                <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2  mt-2">
                    <div class="col">
                        <div class="card mb-3">
                            <div class="card-header">
                                <div>Permanent Address info</div>
                            </div>
                            <div class="card-body">
                                <div>  <strong>Village: </strong>   <span> ${obj["Village"]} </span>  </div>
                                <div>   <strong>Parish:</strong> ${obj["Parish"]} <span></span> </div>
                                <div>   <strong>County:</strong> <span>${obj["County"]} </span> </div>
                                <div>   <strong>District:</strong> <span>${obj["District"]} </span> </div>
                            </div>
                        </div>
                    </div>
    
                    <div class="col">
                        <div class="card">
                            <div class="card-header">
                                <div>Current Address Details </div>
                            </div>
                            <div class="card-body">
                                <div>  <strong>Village: </strong> <span>${obj["CurrentAddressDetails"]["Village"]}</span></div>
                                <div>  <strong>Division: </strong> <span>${obj["CurrentAddressDetails"]["Division"]}</span></div> 
                                <div>  <strong>District: </strong> <span>${obj["CurrentAddressDetails"]["Districk"]}</span></div>
                                <div>  <strong>PhoneNumber: </strong> <span>${obj["CurrentAddressDetails"]["PhoneNumber"]}</span></div>  
                            </div>
                        </div>
                    </div>
                </div>
            `
            
        })

    }else{
        html += "<div> No details on this person </div>"
    }
    
    return html

    
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard:', text);
    }).catch(err => {
        alert('Failed to copy to clipboard:', err);
    });
}

async function loadCredit() {
    const creditData = await fetchCreditdetails();
    const portifolioData = await fetchClientPortifolio();
    const portifolio_overdue = await fetchClientTotalPenaltiesAndOverdue()
    
    
    const portifolio = parseFloat(portifolioData["portifolio"]) + parseFloat(portifolio_overdue['TotalPenalty'])
    // #tofixed is to make it have only 2 decimal places
    // console.log(penalty)
    

    
    const creditHtml = generateCreditdetails(data = creditData);
    document.getElementById("credit-body").innerHTML = creditHtml;
    document.getElementById("current-portifolio").innerHTML = portifolio;
}


async function loadhtml() {
    const data = await fetchClientDetails();
    const html = generatepersonalHtml(data);
   document.querySelector(".personalDetails").innerHTML = html;
    
}

async function loadpaybutton() {
    const data = await fetchCreditdetails();
    const btn  = generatePaybutton(data);
    document.getElementById("paybutton").innerHTML = btn;
    
}

async function loadLoanSecurity() {
    const loan_security = await fetchLoanSecurity();
    const penalty_overdue = await fetchClientTotalPenaltiesAndOverdue()
    document.getElementById("loan_security").innerHTML = loan_security["loanSecurity"]
    document.getElementById("penalty").innerHTML = penalty_overdue["TotalPenalty"]
    document.getElementById("overdue").innerHTML = penalty_overdue["TotalOverDue"]
    
}

async function loadinvestmentAndLoanSecurityButton() {
    const data = await fetchClientDetails();
    var html = generateInvestmentButton(data)
    document.getElementById("makeinvestmentPayment").innerHTML = html;
    
};
async function loadInvestmentDetails() {
    const totalInvestment = await fetchClientInvestment();
    document.getElementById("investment"). innerHTML = totalInvestment["investment"];
    
}

loadhtml();
loadCredit();
loadpaybutton();
loadLoanSecurity();
loadinvestmentAndLoanSecurityButton();
loadInvestmentDetails();

 


