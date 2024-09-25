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

function generatePaybutton(data){
    return `
        <a data-loan-id="${data["loanId"]}" href="/Makepayments" class="btn btn-success">pay</a>
    `

}

function generateCreditdetails(data){
    var html = `
        <tr>
            <td>17/3/2024</td>
            <td>Daily</td>
            <td>${data["Principle"]}</td>
            <td>${data["InterestRate"]}</td>
            <td>${data["Portifolio"]}</td>
            <td>${data["PaymentperiodinDays"]} days</td>
            <td>${data["DailCommitmentAmount"]}</td>
        </tr>
        
                            
    `
    return html;


}


function generatepersonalHtml(data) {
    var html = ""
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
                    <div class="row g-3">
                        <div class="col">Branch</div>
                        <div class="col">${obj["branchDetails"]["BranchId"]}</div>
                    </div>

                </div>
            </div>
            <div class="row mt-2">
                <div class="col">
                    <div class="card">
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
    return html

    
}

async function loadCredit() {
    const creditData = await fetchCreditdetails();
    const creditHtml = generateCreditdetails(data = creditData);
    
    document.getElementById("credit-body").innerHTML = creditHtml

    
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

loadhtml();
loadCredit();
loadpaybutton()

