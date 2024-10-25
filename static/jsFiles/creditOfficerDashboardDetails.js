document.addEventListener("DOMContentLoaded", function(){
    let selectElement = document.getElementById("clientSelect")
    selectElement.addEventListener("change",function(){
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        const clientName = selectedOption.value
        var clienttId = selectedOption.getAttribute("data-client-id")

        if(clientName){
            if(clienttId){
                // here we will send client id to server to fetch client details
                // and then update the client prifile section
                var modalBody = document.getElementById("clientDetails")
                modalBody.innerHTML = `
                    <div class= "container">
                        <div class="row row-cols-2 g-3">
                            <div class="col">
                                <div class="card shadow-sm" >
                                    <button class="btn text-info " data-bs-target="#clientinfo" data-bs-toggle="modal">
                                        PERSONAL INFO    
                                    </button>
                                    <div class="modal" id="clientinfo">
                                        <div class="modal-dialog  modal-dialog-centered modal-dialog-scrollable">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    Client: ${clientName}
                                                    <button class=" btn-close" data-bs-dismiss="modal" data-bs-target="#clientinfo"></button>    
                                                </div>
                                                <div class="modal-body"> 
                                                    <div> DOB: 12/3/1393</div>
                                                    <div> GENDER: male</div>
                                                    <div> CONTACT: 078888888</div>
                                                    <div> ADDRES: wampewo</div>
                                                    
                                                </div>
                                            </div>
                                            
                                        </div>
                                        
                                    </div>
                                      
                                </div>
                            </div>
                            
                            <div class="col">
                                <div class="card shadow-sm" >
                                    <button class="btn text-info " data-bs-target="#currentLoan" data-bs-toggle="modal">
                                        CURRENT LOAN  
                                    </button>
                                    <div class="modal" id="currentLoan">
                                        <div class="modal-dialog  modal-dialog-centered modal-dialog-scrollable">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    LOAN TYPE: Bussines
                                                    <button class=" btn-close" data-bs-dismiss="modal" data-bs-target="#currentLoan"></button>    
                                                </div>
                                                <div class="modal-body"> 
                                                    <div> Loan Amount: Ugx 200,000</div>
                                                    <div> Interest Rate: 20%</div>
                                                    <div> Total: Ugx 240,000</div>
                                                    <div> Payment schedule: daily </div>
                                                    <div> Loan Period: 30 days</div>
                                                    <div class=" text-success"> Balance: Ugx 59000</div>
                                                    
                                                    
                                                </div>
                                            </div>
                                            
                                        </div>
                                        
                                    </div>
                                      
                                </div>
                            </div>

                            <div class="col">
                                <div class="card shadow-sm" >
                                    <button class="btn text-info " data-bs-target="#creditHistory" data-bs-toggle="modal">
                                        CREDIT HISTORY  
                                    </button>
                                    <div class="modal" id="creditHistory">
                                        <div class="modal-dialog  modal-dialog-centered modal-dialog-scrollable">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    CREDIT SCORES: 67%
                                                    <button class=" btn-close" data-bs-dismiss="modal" data-bs-target="#creditHistory"></button>    
                                                </div>
                                                <div class="modal-body"> 
                                                    <div> Current loan: 90% </div>
                                                    <div> loan 2: 70%</div>
                                                    <div> loan 1: 89%</div>
                                                </div>
                                            </div>
                                            
                                        </div>
                                        
                                    </div>
                                      
                                </div>
                            </div>

                            <div class="col">
                                <div class="card shadow-sm" >
                                    <button class="btn text-info " data-bs-target="#savingInvestments" data-bs-toggle="modal">
                                        SAVINGS 
                                    </button>
                                    <div class="modal" id="savingInvestments">
                                        <div class="modal-dialog  modal-dialog-centered modal-dialog-scrollable">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    annual interest 3%
                                                    <button class=" btn-close" data-bs-dismiss="modal" data-bs-target="#savingInvestments"></button>    
                                                </div>
                                                <div class="modal-body"> 
                                                    <div class=" text-success"> saving: Ugx 59000</div>
                                                    
                                                    
                                                </div>
                                            </div>
                                            
                                        </div>
                                        
                                    </div>
                                      
                                </div>
                            </div>
                        </div>
                    </div>

                `;

                const displayHtml = new bootstrap.Modal(document.getElementById('clientProfile'));
                displayHtml.show();
            }
        }
    })

});
async function getcollectionSheetDetails(){
    return await fetch("/crediofficerDashboard?type=ForSpecificEmployee")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching collection sheet details")
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

async function getOfficerPortifolioDetails(){
    return await fetch("/crediofficerDashboard?type=portifolio")
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


async function fetchInvestmentDetails() {
    return await fetch("/crediofficerDashboard?type=savings")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error  while fetching investment details for a specfic employee")
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

async function fetchClientDebtedLoanAccountDetails() {
    return fetch("/crediofficerDashboard?type=credit")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetching client debted loan details")
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

function calaculateTotalExpectation(data){
    let total = 0
    data.forEach((obj) =>{
        total += Number(obj["commitment"])
    })
    return total
};


function calaculateTotalCredit(data){
    let total = 0;
    if(data){
        data.forEach((obj)=>{
            total += obj["AmountPaid"]
        })
        return total;
    }
    else{
        return total;
    }
};

function calaculateTotalSavings(data){
    let total = 0;
    if(data){
        data.forEach((obj)=>{
            total += obj["Amount"]
        })
        return total;
    }
    else{
        return total;
    }
};


async function loadExceptation() {
    const data = await getcollectionSheetDetails();
    const portifolio = await getOfficerPortifolioDetails();
    const creditDetails =  await fetchClientDebtedLoanAccountDetails() ;
    const savingsDetails = await fetchInvestmentDetails();
    const exceptation =  calaculateTotalExpectation(data);

    // calculations
    const credit = calaculateTotalCredit(creditDetails);
    const savings = calaculateTotalSavings(savingsDetails);



    const totalCollections = Number(savings) + Number(credit)
    
    
    document.getElementById("Exceptation").innerHTML = exceptation;
    document.getElementById("portifolio").innerHTML = portifolio["totalPortifoli"];
    document.getElementById("collections").innerHTML = totalCollections;
    document.getElementById("credit").innerHTML = credit;
    document.getElementById("savings").innerHTML = savings;

    
};
loadExceptation();