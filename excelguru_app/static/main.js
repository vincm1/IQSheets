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


const submitButton2 = document.getElementById('favorite-btn');
        submitButton2.addEventListener('click', () => {
            submitButton2.disabled = true;
        });