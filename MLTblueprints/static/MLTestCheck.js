document.getElementById('testModel').addEventListener("submit", function (event){
   let messageBuffer = ""   
   if(document.getElementById('MLmodel').files.length === 0){
      messageBuffer = "No model was uploaded.";
   }
   if(document.getElementById('testingData').files.length === 0){
      messageBuffer+= checkIfEmpty(messageBuffer) + "No testing data was uploaded.";
   }
   if(messageBuffer != ""){
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