event_handlers["init-contract"] = (id, value, event_name) => {
    console.log("init-contract", id, value, event_name);
    const contract = document.getElementById(value.contract);
    contract.innerHTML = value.contract_content;
    const terms = document.querySelector(".terms-and-conditions");
    const termsLastElement = terms.lastElementChild;

    const acceptButton = document.getElementById(value.accept_btn);

    function obCallback(payload) {
        if (payload[0].isIntersecting) {
            acceptButton.classList.remove("hidden");
        } else {
            acceptButton.classList.add("hidden");
        }
    }
    
    const observer = new IntersectionObserver(obCallback, { root: terms, threshold: 0.9 });
    observer.observe(termsLastElement);
    acceptButton.addEventListener("click", () => {
                  
        if (event_handlers[value.func_name])
        {
        event_handlers[value.func_name](id, value, event_name);};

        const checkbox = document.getElementById("userAgreementCheck").firstChild;
        checkbox.checked = true;
        
    });
    
   
};