function validateInput(input) {
    var errorMsg = "";
    var value = input.value;
    
    if (isNaN(value)) {
      errorMsg = "Please enter a number.";
    } else if (value < 0 || value > 1) {
      errorMsg = "Value must be between 0 and 1.";
    }
    
    var errorField = input.nextElementSibling;
    errorField.innerHTML = errorMsg;
    if (errorMsg) {
      input.style.border = "2px solid red";
    } else {
      input.style.border = "1px solid black";
    }
  }
  
  function validateInputLift(input) 
  {
    var errorMsg = "";
    var value = input.value;
    
    if (isNaN(value)) 
    {
      errorMsg = "Please enter a number.";
    } else if (value <1) {
      errorMsg = "Value must be greater than 1.";
    }
    
    var errorField = input.nextElementSibling;
    errorField.innerHTML = errorMsg;
    if (errorMsg) {
      input.style.border = "2px solid red";
    } else {
      input.style.border = "1px solid black";
    }
  }

  