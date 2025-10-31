function show(){
    const applicationForm = document.querySelector(".appointment-form");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.transform = "translateX(0)";
            applicationForm.classList.remove("hide");
            setTimeout(()=>{
                applicationForm.style.opacity = "1";
            }, 500);
        }, 100);
    }
}

function hide(){
    const applicationForm = document.querySelector(".appointment-form");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.opacity = "0";
            setTimeout(()=>{
                applicationForm.style.transform = "translateX(200%)";
                applicationForm.classList.add("hide");
            }, 500);
        }, 100);
    }
}

function showTablet(){
    const applicationForm = document.querySelector(".appointment-formTablet");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.transform = "translateX(0)";
            applicationForm.classList.remove("hide");
            setTimeout(()=>{
                applicationForm.style.opacity = "1";
            }, 500);
        }, 100);
    }
}

function hideTablet(){
    const applicationForm = document.querySelector(".appointment-formTablet");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.opacity = "0";
            setTimeout(()=>{
                applicationForm.style.transform = "translateX(200%)";
                applicationForm.classList.add("hide");
            }, 500);
        }, 100);
    }
}

function showMobile(){
    const applicationForm = document.querySelector(".appointment-formMobile");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.transform = "translateX(0)";
            applicationForm.classList.remove("hide");
            setTimeout(()=>{
                applicationForm.style.opacity = "1";
            }, 500);
        }, 100);
    }
}

function hideMobile(){
    const applicationForm = document.querySelector(".appointment-formMobile");
    if (applicationForm) {
        setTimeout(()=>{
            applicationForm.style.opacity = "0";
            setTimeout(()=>{
                applicationForm.style.transform = "translateX(200%)";
                applicationForm.classList.add("hide");
            }, 500);
        }, 100);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var onlinePayment = document.getElementById('option8');
    var cashPayment = document.getElementById('option5');
    var makeAppointmentBtn = document.querySelector('.sub');
    
    if (onlinePayment && cashPayment && makeAppointmentBtn) {
        onlinePayment.addEventListener('change', function () {
            if (onlinePayment.checked) {
                makeAppointmentBtn.disabled = true;
            } else {
                makeAppointmentBtn.textContent = 'Make an Appointment';
            }
        });

        cashPayment.addEventListener('change', function () {
            if (cashPayment.checked) {
                makeAppointmentBtn.textContent = 'Make An Appointment';
                makeAppointmentBtn.disabled = false;
            } 
        });
    }
});

const selectElement = document.querySelector('.form-select');
const priceInput = document.getElementById('selectedPrice');

if (selectElement && priceInput) {
    selectElement.addEventListener('change', (event) => {
        const selectedOption = event.target.selectedOptions[0];
        const price = selectedOption.dataset.price;
        console.log(price);
        priceInput.value = price;
    });
}

// Form submission handling is now handled in the templates directly