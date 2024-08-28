

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
    data.forEach((branchObject) => {
        html += `
            <tr>
                <td>
                    <a data-branch-id=${branchObject["branchId"]} class="link btn  btn-outline-dark" href="/branch">${branchObject.branchName}</a>
                </td>
                <td>${branchObject.officeLocation}</td>
            </tr>
        `;
    });
    return html;
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