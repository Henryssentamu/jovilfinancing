async  function fetchClientDetails(){
    return await  fetch("/clientProfileOnManagersPage?type=clientDetails")
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
    return await fetch("/clientProfileOnManagersPage?type=clientCreditdetails")
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
    return await fetch("/clientProfileOnManagersPage?type=clientPortifolio")
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
    return fetch("/clientProfileOnManagersPage?type=clientLoanSecurity")
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
    return fetch("/clientProfileOnManagersPage?type=investments")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching clients investments")
            }
            return response.json()
        })
        .then(data =>{
            var total = 0;
            if(data){
                data.forEach((obj)=>{
                    total += obj["Amount"]
                })
            }
            return total
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

function generatePaybutton(data){
    return `
        <a class="btn btn-success" onclick="sendLoanIdForPayment('${data["loanId"]}')">Make loan payment</a>
    `
};

function captureSelectedOption(select){
    var selectedOption = select.options[select.selectedIndex];
    var loanId = selectedOption.getAttribute("data-loanId");
    var selectedValue = selectedOption.value;
    if(loanId && (selectedValue === "loanSecurity" || selectedValue === "investment" )){
        fetch("/balancing",{
            method:"POST",
            headers:{
                "Content-type":"application/json"
            },
            body:JSON.stringify({"type": "loanpayment","data":{"reductFrom":selectedValue,"loanId":loanId}})
        })
        .then(response =>{
            if(!response.ok){
                throw new Error("server erroe while sending loan id on payment route")
            }
            return response.json()
        })
        .then(data =>{
            if(data["response"] === "recieved"){
                window.location.href = "/balancing"
            }
        })
        .catch(error =>{
            console.log(error)
        })
    }

}

function generatebalancingButton(data){
    return `
        <a class="btn btn-outline-primary"  data-bs-target="#balancing" data-bs-toggle="modal"> Loan Balance </a>
        <div class="modal" id="balancing">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="modal-title">Close </div>
                        <button class="btn-close" data-bs-dismiss="modal" data-bs-target="#balancing"></button>
                    </div>
                    <div class="modal-body">
                        <select class="form-select" size="2" aria-label="size 2" onchange="captureSelectedOption(this)"> 
                            <option selected> Balance With ?</option>
                            <option value="loanSecurity" data-loanId='${data["loanId"]}'> Loan Security </option>
                            <option value="investment" data-loanId='${data["loanId"]}'> Investment </option>
                        </select>
                    
                    </div>
                </div>
            </div>
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
                        
    
                    </div>
                </div>
                <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2  mt-2">
                    <div class="col">
                        <div class="card mb-3">
                            <div class="card-header">
                                <div>contact info</div>
                            </div>
                            <div class="card-body">
                                <div>  <strong>PhoneNumber: </strong> <span>${obj["PhoneNumber"]}</span></div>
                                <div>  <strong>Current Address: </strong>   <span> ${obj["CurrentAddress"]} </span>  </div>
                                <div>   <strong>Divission/City:</strong> ${obj["CityDivision"]} <span></span> </div>
                                <div>   <strong>District:</strong> <span>${obj["District"]} </span> </div>
                            </div>
                        </div>
                    </div>
    
                    <div class="col">
                        <div class="card">
                            <div class="card-header">
                                <div>Occupation Details </div>
                            </div>
                            <div class="card-body">
                                <div> <strong>Occupation:</strong> <span> vendor </span> </div>
                                <div> <strong>working Area:</strong>   <span>kalerwe markete</span> </div>
                                <div> <strong>Zone</strong>  <span>Dembe market </span> </div>
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

async function loadCredit() {
    const creditData = await fetchCreditdetails();
    const portifolio = await fetchClientPortifolio();
    
    const creditHtml = generateCreditdetails(data = creditData);
    document.getElementById("credit-body").innerHTML = creditHtml;
    document.getElementById("current-portifolio").innerHTML = portifolio["portifolio"];
}


async function loadhtml() {
    const data = await fetchClientDetails();
    const html = generatepersonalHtml(data);
   document.querySelector(".personalDetails").innerHTML = html;
    
}

async function loadpaybutton() {
    const data = await fetchCreditdetails();
    const btn  = generatePaybutton(data);
    const balances = generatebalancingButton(data);
    document.getElementById("paybutton").innerHTML = btn;
    document.getElementById("balanceTheLoan").innerHTML = balances;
    
}

async function loadLoanSecurity() {
    const loan_security = await fetchLoanSecurity();
    document.getElementById("loan_security").innerHTML = loan_security["totalSecurity"]
    
}

async function loadinvestmentAndLoanSecurityButton() {
    const data = await fetchClientDetails();
    var html = generateInvestmentButton(data)
    document.getElementById("makeinvestmentPayment").innerHTML = html;
    
};
async function loadInvestmentDetails() {
    const totalInvestment = await fetchClientInvestment();
    document.getElementById("investment"). innerHTML = totalInvestment;
    
}

loadhtml();
loadCredit();
loadpaybutton();
loadLoanSecurity();
loadinvestmentAndLoanSecurityButton();
loadInvestmentDetails();

 


