async function getDetails() {
    return await fetch("/disburshmentReports?type=loanApprovedDetails")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching approved loan details")
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

function generateHtml(data){
    let html = ""
    data.forEach((obj,index)=>{
        var loanDetails = obj["loanDetails"];
        var clientDetails = obj["clientDetails"];
        var branchDetails = obj["branchDetails"];
        html += `
            <tr id="element-container-id-${index}">
                <td>${loanDetails["ApprovedDate"]}</td>
                <td>${clientDetails["FirstName"]} <span> </span> ${clientDetails["SirName"]} </td>
                <td> ${branchDetails["BranchName"]}</td>
                <td>${loanDetails["LoanAmountApproved"]}</td> 
                <td> <button  id="ElementId-${index}" data-loan-details="${loanDetails["LoanId"]}" class="btn btn-success"  onclick="sendLoanId('${index}')"> Confirm Disbursment </button> </td> 
            </tr>
        `
    })
    return html
}

async function loadhtml() {
    const data = await getDetails();
    let html = await generateHtml(data);
    document.getElementById("details").innerHTML = html

    
}

function sendLoanId(index){
    const loader = document.getElementById("loader");
    loader.style.display = "flex"
    var elemt = document.getElementById(`ElementId-${index}`);
    var id = elemt.getAttribute("data-loan-details");
    fetch("/disburshmentReports",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({"type":"confirmedLoan","data":id})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("error while sending confirmed loan details to server")
        }
        return response.json()
    })
    .then(data =>{
        if(data["response"] =="LoanConfirmed"){
            loader.style.display = "none"
            document.getElementById(`element-container-id-${index}`).innerHTML = "";
            location.reload()
        }
        loader.style.display = "none";
        location.reload()
    })
    .catch(error =>{
        loader.style.display = "none";
        console.log(error)
    })

    
            
};

loadhtml()

