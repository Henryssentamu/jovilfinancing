

async function getBranchdetails(){
    return await fetch("/branches?type=branchDetails")
        .then(response => {
            if(!response.ok){
                throw new Error("error while fetching branch details")
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

async function fetchNumberOfBranches() {
    return await fetch("/branches?type=numberOfBranches")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching number of branched from the server")
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

function generateHtml(data) {
    let html = "";
    data.forEach((branchObject, index) => {
        html += `
            <tr>
                <td>
                    <a id="branch_${index}" data-branch-id=${branchObject["branchId"]} class="link btn  btn-outline-dark"   onclick="sendSelectedBranchIdToServer(${index})">${branchObject.branchName}</a>
                </td>
                <td>${branchObject.officeLocation}</td>
            </tr>
        `;
    });
    return html;
}

function sendSelectedBranchIdToServer(id){
    const element = document.getElementById(`branch_${id}`)
    const branchId = element.getAttribute("data-branch-id")
    fetch("/branch",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({"BranchId":branchId})
    })
    .then(response =>{
        if(!response.ok){
            throw new Error("error while sending selected branch id to server")
        }
        return response.json()
    })
    .then(data =>{
        if (data){
            window.location.href = "/branch"
        }
    })
    .catch(error =>{
        console.log(error)
    })
}

async function loadDetailsOnPage(){
    let numberOfBranches = await fetchNumberOfBranches();
    let data = await getBranchdetails();
    let generatedHtml =  generateHtml(data);
        
    document.getElementById("numberOfBranches")
        .innerHTML = numberOfBranches["branches"]
    document.getElementById("branchTableDetails")
        .innerHTML = generatedHtml


}

loadDetailsOnPage()