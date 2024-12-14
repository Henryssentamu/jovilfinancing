const loader = document.getElementById("loader")
async function getclientlist() {
    loader.style.display = "flex";
    return await fetch("allClientList?type=allclientslist")
        .then(response =>{
            if(!response.ok){
                throw new Error("error while fetching all client list in all client list route")
            }
            return response.json()
        })
        .then(data => {
            if(data){
                loader.style.display = "none";
                return data
            }
            
        })
        .catch(error =>{
            loader.style.display = "none";
            console.log(error)
        })
    
}



function generateHtml(data){
    const number = data.length;
    let html = ""
    data.forEach((clientObject,index) =>{
        html += `
            <tr>
                <td>${index + 1}</td>
                <td>
                    <a class="clientLink" data-client-id="${clientObject["AccountNumber"]}" style="cursor: pointer;" >${clientObject["FirstName"]} <span style="margin-left:3px"> ${clientObject["SirName"]}</span> </a>
                </td>
                <td> ${clientObject["CurrentAddressDetails"]["PhoneNumber"]}</td>
                <td> ${clientObject["Gender"]}</td>
            </tr>
        `

    })
    return {"html":html,"total":number}
}

async function sendClientIdToserver(){
    let clientElements = document.querySelectorAll(".clientLink");
    clientElements.forEach((clientElement)=>{
        clientElement.addEventListener("click",(event)=>{
            event.preventDefault();
            let id = clientElement.getAttribute("data-client-id");
            let data = {"type":"clientID","data":id}

            fetch("/clientProfile",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify(data)
            })
            .then(response =>{
                if(!response.ok){
                    throw new Error("error while sending clicked client")
                }
                return response.json()
            })
            .then(data =>{
                window.location.href = "/clientProfile"
            } )
            .catch(error =>{
                alert(error)
    
            })


        })
    })
    
    
}

async function loadhtml() {
    const data = await getclientlist();
    const Datadetails =   await generateHtml(data);
    document.getElementById("employeeDetails")
        .innerHTML = Datadetails["html"];
    document.getElementById("totalNumber")
        .innerHTML = Datadetails["total"]
    sendClientIdToserver();
    
}

loadhtml()