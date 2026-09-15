 //this controls whether to show a sklearn dataset to use or to show the option to upload your own dataset
  let dataChoice = document.getElementById('dataChoice')
  const defaultDataButton = document.getElementById("defaultData")
  const importDataButton = document.getElementById("importData")
  
  const userDataset = document.getElementById("userDataset")
  const sklearnData = document.getElementById("sklearnDataset")
  defaultDataButton.addEventListener("click", () =>{
    sklearnData.hidden = false
    userDataset.hidden = true
    dataChoice.value = "Sklearn Data"
  });
  importDataButton.addEventListener("click", () => {
    sklearnData.hidden = true
    userDataset.hidden = false
    dataChoice.value = "User Imported Data"
  });  

  //if the user has not selected any data, this prevents the form from being submitted
  document.getElementById('MLRegression').addEventListener("submit", function (event) {
    let x = 0
    let messageBuffer = ""
    if (dataChoice.value == ""){
      messageBuffer = "You have not selected whether to use a default dataset or your own data."
    }
    else if (document.getElementById('defaultDatasets').value == "" && dataChoice.value == "Sklearn Data"){
      messageBuffer = "You have selected the option to use a default dataset, but have not choosen one to use."
    }
    else if (document.getElementById('importedDataset').files.length === 0 && dataChoice.value == "User Imported Data"){
      messageBuffer = "You have selected a to submit your own data, but have not imported any."
    }
    if (document.querySelector('input[name = "headOrNo"]:checked') == null && dataChoice.value == "User Imported Data"){
      messageBuffer+= checkIfEmpty(messageBuffer) + "You have not verified if the data has headers or not." 
    }
    if (document.getElementById('MLmodel').value == ""){
      messageBuffer+= checkIfEmpty(messageBuffer) + "You have not selected a machine learning model."
    }
    if (messageBuffer != "")
    {
      event.preventDefault();
      alert(messageBuffer);
    }
  });

  function checkIfEmpty(messageBuffer){
    if(messageBuffer != ""){
      return "\n";
    }
    else{
      return "";
    }
  }