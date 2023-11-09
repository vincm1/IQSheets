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
  } else {
      document.getElementById("result").innerHTML = "Trage deine Daten ein.";
  }
});

// End Calculator //

$(document).ready(function(){
  $('.accordion-item').on('click', function(){
      $(this).toggleClass('active');
  });
});

const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

searchBtn.addEventListener("click" , () =>{
    sidebar.classList.remove("close");
})

modeSwitch.addEventListener("click" , () =>{
    body.classList.toggle("dark");
    
    if(body.classList.contains("dark")){
        modeText.innerText = "Light mode";
    }else{
        modeText.innerText = "Dark mode";
        
    }
});

// Get the button:
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

const premium = document.getElementById('premium')
const premiumBtn = document.getElementById('premium-btn');

premium.addEventListener("mouseover", () => {
	premiumBtn.innerText = "Upgrade";
});

premium.addEventListener("mouseout", () => {
	premiumBtn.innerText = "Premium";
});

const premiumProfileBtn = document.getElementById('profile-premium-btn');

premiumProfileBtn.addEventListener("mouseover", () => {
	premiumProfileBtn.innerText = "Upgrade";
});

premiumProfileBtn.addEventListener("mouseout", () => {
	premiumProfileBtn.innerHTML = "<i class='bx bx-diamond icon pe-2'></i>Premium";
});

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

// // Initialize Stripe.js
// const stripe = Stripe('pk_test_51MpD8VHjForJHjCt0k588Bqt0avQVFo4mn7qLGdEcskklPj0hEds8uJNe6qbQFUtglDgcNR58dpUpAViJcL2iyqG00cDOktWn0');
// const aboButton = document.getElementById('abo-btn')

// aboButton.addEventListener("click", () => {
//   // Get Checkout Session ID
//   fetch("/create-checkout-session")
//   .then((result) => { return result.json(); })
//   .then((data) => {
//     console.log(data);
//     // Redirect to Stripe Checkout
//     return stripe.redirectToCheckout({sessionId: data.sessionId
//     });
//   })
//   .then((res) => {
//     console.log(res);
//   });
// });
