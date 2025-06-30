function getApproveddetails(index){
    var loanAmount = document.getElementById(`loanAmount-${index}`).value;
    var intererate =   document.getElementById(`interestRate-${index}`).value;
    var paymentPeriod = document.getElementById(`paymentPeriod-${index}`).value;
    var loanId = document.querySelector(`.loanId-${index}`).getAttribute("data-loan-id");
    return {"loanId":loanId,"approvedAmount": loanAmount,"interestRate":intererate, "paymentPeriod":paymentPeriod}
}

async function approveLoan(index) {
    const loader = document.getElementById("loader");
    loader.style.display = "flex";
    const data = await getApproveddetails(index);
    fetch("/underWritter",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({"type":"approvedloan","data":data})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("error while sending loan approval details to server")
        }
        return response.json()
    })
    .then(data =>{
        loader.style.display = "none";
        location.reload()
    })
    .catch(error =>{
        loader.style.display = "none";
        console.log(error)
    })

    
}



async function deleted_loan(index) {
    const loader = document.getElementById("loader");
    loader.style.display = "flex";
    const data = await getApproveddetails(index);
    fetch("/underWritter",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({"type":"deleted_loan","data":data['loanId']})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("error while sending loan approval details to server")
        }
        return response.json()
    })
    .then(data =>{
        loader.style.display = "none";
        location.reload()
    })
    .catch(error =>{
        loader.style.display = "none";
        console.log(error)
    })

    
}