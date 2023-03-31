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