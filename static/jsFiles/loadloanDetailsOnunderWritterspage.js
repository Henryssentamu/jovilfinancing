async function getLoanApplicationDetails() {
    return await fetch("/underWritter?type=loandetails")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching loan application details")
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

function generatehtml(data){
    html = ""
    data.forEach(obj =>{
        html += `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">Client: ${obj["FirstName"]} <span> </span> ${obj["SirName"]} </h5>
                    <div class="row">
                        <div class="col">
                            Application Date: ${obj["Date"]}
                        </div>

                        <div class="col">
                            Client Contact: ${obj["Contact"]}
                        
                        </div>
                        <div class="col">
                            <div class="row">
                                Business Loaction: ${obj["BusinessLocation"]}
                            </div>
                            <div class="row">
                                Work Area: ${obj["WorkArea"]}
                            </div>
                            <div class="row">
                                Business/ Occupation: ${obj["Occupation"]}
                            </div>

                        </div>
                    </div>

                    <!-- Loan Application Details -->
                    <div class="row">
                        <div class="col-md-4">
                            <p><strong>Loan Amount:</strong></p>
                            <input type="number" class="form-control" value="${obj["LoanAmount"]}" id="loanAmount1">
                        </div>
                        <div class="col-md-4">
                            <p><strong>Interest Rate (%):</strong></p>
                            <input type="number" class="form-control" value="${obj["intereRate"]}" id="interestRate1">
                        </div>
                        <div class="col-md-4">
                            <p><strong>Payment Period (Days):</strong></p>
                            <input type="number" class="form-control" value="${obj["LoanPeriodInDays"]}" id="paymentPeriod1">
                        </div>
                    </div>
                    <div class="row mt-4" style={width:100px}>
                        <div class = "col-8">
                            <img style={width:50px} src="../static/${obj["BusinessImages"]}">
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-primary me-2" onclick="approveLoan(1)">Approve</button>
                    </div>
                </div>
            </div>
        `
    })
    return html
}

async function loadhtml(){
    const data = await getLoanApplicationDetails();
    const html = await generatehtml(data);
    document.getElementById("body-content")
        .innerHTML += html

}

loadhtml()



