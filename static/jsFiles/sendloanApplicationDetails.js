function getLoanApplicationDetails(){
    let loanApplicationData = new FormData()
    loanApplicationData.append("clientId", document.getElementById("clientNumber").value)
    loanApplicationData.append("loanAmount", document.getElementById("loanAmount").value)
    loanApplicationData.append("clientCurrentaddress", document.getElementById("clientCurrentaddress").value)
    loanApplicationData.append("devisioncity",document.getElementById("devisioncity").value)
    loanApplicationData.append("state",document.getElementById("state").value)
    loanApplicationData.append("Occuption",document.getElementById("Occuption").value)
    loanApplicationData.append("workArea",document.getElementById("workArea").value)
    loanApplicationData.append("businessLoaction",document.getElementById("businessLoaction").value)
    loanApplicationData.append("contact", document.getElementById("contact").value)
    loanApplicationData.append("businessPic",document.getElementById("businessPic").files[0])
    // insuring interesting rate and loan period are accessed if default values are changed using  ternary operator with trim()

    // document.getElementById("interestRate").value.trim() removes any leading or trailing spaces from the value.
    // If the trimmed value is an empty string (""), it assigns the default value of 20.
    // Otherwise, it uses the entered value

    let interestRate = document.getElementById("interestRate").value.trim() === "" ? 20 : document.getElementById("interestRate").value;
    let loanPeriod = document.getElementById("loanPeriod").value.trim() === "" ? 30 : document.getElementById("loanPeriod").value;
    loanApplicationData.append("interestRate", interestRate);
    loanApplicationData.append("loanPeriod", loanPeriod)

    return loanApplicationData
}

function sendLoanApplicationDetails() {
    document.getElementById("submitt")
        .addEventListener("click", async(event)=>{
            event.preventDefault();
            let data = getLoanApplicationDetails();
        
            await fetch("/loanApplication",{
                method:"POST",
                body:data
            })
            .then(response =>{
                if(!response.ok){
                    throw new Error("error while sending loan application to server")
                }
                return response.json()
            })
            .then(data =>{
                alert(data["response"])
                location.reload()
            })
            .catch(error =>{
                console.log(error)
                alert(error)
            })


        })
    
}

sendLoanApplicationDetails()