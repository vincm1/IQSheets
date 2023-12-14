// Get the element where you want to change the text
var changingTextElement = document.getElementById("changing-text");

// Define an array of text messages to cycle through
var textMessages = ["Logistiker.", "Vertriebler.", "Einkäufer.", "Alle."];

// Initialize an index to track the current message
var currentIndex = 0;

// Function to update the text
function updateText() {
    changingTextElement.textContent = textMessages[currentIndex];
    currentIndex = (currentIndex + 1) % textMessages.length;
}

// Change the text every 3 seconds (3000 milliseconds)
var interval = setInterval(updateText, 3000);


// Calculator Landing Page // 

document.getElementById("calculate").addEventListener("click", function() {
  var hours = parseFloat(document.getElementById("hours").value);
  var hourlyWage = parseFloat(document.getElementById("hourly-wage").value);
  
  if (!isNaN(hours) && !isNaN(hourlyWage)) {
      var totalEarnings = hours * hourlyWage;
      document.getElementById("result").innerHTML = totalEarnings.toFixed(2) + "€";
      document.getElementById("result2").innerHTML = hours * 0.25;
  } else {
      document.getElementById("result").innerHTML = "Trage deine Daten ein.";
  }
});

// End Calculator //

function copyToClipboard() {
    /* Get the text from the element with the ID "copy-target" */
    var copyText = document.getElementById("copy-target").innerText;
  
    /* Create a temporary input element */
    var tempInput = document.createElement("input");
  
    /* Set the value of the input element to the text to be copied */
    tempInput.value = copyText;
  
    /* Add the input element to the document */
    document.body.appendChild(tempInput);
  
    /* Select the text in the input element */
    tempInput.select();
  
    /* Copy the selected text to the clipboard */
    document.execCommand("copy");
  
    /* Remove the input element from the document */
    document.body.removeChild(tempInput);
  }

const filterBtn = document.getElementById("filter-btn");
filterBtn.addEventListener("click", () => {
    filterBtn.classList.add("active");
  });

$(document).ready(function() {
    $('#formula-form').submit(function(event) {
      event.preventDefault(); // prevent form submission
      if ($('#formel-btn').data('clicked')) { // check if button is clicked
        this.submit(); // submit the form
      }
    });
    $('#formel-btn').click(function() {
      $(this).data('clicked', true); // set button clicked flag
    });
  });

$(document).ready(function() {
  $('#incorrect-btn').click(function(event) {
    event.preventDefault();
    $.post('/submit-form', {buttonName: 'incorrect-btn'});
      // Or you can submit a form with the button name as a hidden input field
      // $('#my-form').append('<input type="hidden" name="buttonName" value="incorrect-btn">').submit();
  });
});

