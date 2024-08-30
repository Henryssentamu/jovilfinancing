async function fetchAccademicDocument(){
    await fetch("/employeeProfile?type=accademicDocument")
        .then(response =>{
            if(!response.ok){
                throw new Error("server error while fetch employee accademic documents")
            }
            return response.blob()
        })
        .then(data =>{
            return URL.createObjectURL(data)
        })
        .catch(error =>{
            console.log(error)
        })
}

async function loadPdf() {
    const pdf = await fetchAccademicDocument()
    document.getElementById("accademicBody")
        .innerHTML = `<iframe src="${pdf}" id="pdfViewer" width="600" height="800" style="border: none;"></iframe>`
}

loadPdf()