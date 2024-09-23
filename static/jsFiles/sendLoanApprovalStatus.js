function getApproveddetails(index){
    var loanAmount = document.getElementById(`loanAmount-${index}`).value;
    var intererate =   document.getElementById(`interestRate-${index}`).value;
    var paymentPeriod = document.getElementById(`paymentPeriod-${index}`).value;
    var loanId = document.querySelector(`.loanId-${index}`).getAttribute("data-loan-id");
    return {"loanId":loanId,"approvedAmount": loanAmount,"interestRate":intererate, "paymentPeriod":paymentPeriod}
}

async function approveLoan(index) {
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
        alert(data["response"])
        location.reload()
    })
    .catch(error =>{
        console.log(error)
    })

    
}