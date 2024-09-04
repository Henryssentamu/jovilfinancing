


function getRegistrationDetails(){
    const formdata = new FormData(); // Create a new FormData object

    formdata.append("firstName", document.getElementById("firstName").value)
    formdata.append("sirName", document.getElementById("surName").value)
    formdata.append("dateOfBirth", document.getElementById("dob").value)
    formdata.append("religion", document.getElementById("religion").value)
    formdata.append("gender", document.getElementById("gender").value)
    formdata.append("ninNumber", document.getElementById("ssn").value)
    formdata.append("phonenumber",  document.getElementById("contact").value)
    formdata.append("address", document.getElementById("address").value)
    formdata.append("city", document.getElementById("city").value)
    formdata.append("state", document.getElementById("state").value)
    formdata.append("nextOfKinFirstName", document.getElementById("nextofKinfirstName").value)
    formdata.append("nextOfKinSirName", document.getElementById("nextofKinsirName").value)
    formdata.append("nextOfKinPhone", document.getElementById("nextofKinPhone").value)
    formdata.append("nextOfKinLocation", document.getElementById("nextOfKinLocation").value)
    formdata.append("ownerPic", document.getElementById("ownerPic").files[0]);
    formdata.append("idpic", document.getElementById("Idpic").files[0])
    
   
    return formdata
}

function sendInputToServer() {
    document.getElementById("submitt").addEventListener("click", async (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
        const Details = getRegistrationDetails()

        await fetch("/registerClient",{
            method:"POST",
            body:Details
        })
        .then(response =>{
            if(!response.ok){
                throw new Error("error while sending client's pictures on the server")
            }
            return response.json()
        })
        .then(data =>{
            alert(data)
            location.reload()
            
        })
        .catch(error =>{
            alert(error)
        })
        
    });
}

sendInputToServer();
