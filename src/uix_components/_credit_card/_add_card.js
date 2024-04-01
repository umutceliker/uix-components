event_handlers["addCard-js"] = (id, value, event_name) => {
    const form = document.getElementById("paymentForm");
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Formun otomatik olarak submit olmasını engelle

        // Formdaki bilgileri al
        const name = document.getElementById("name").value;
        const cardNumber = document.getElementById("cardnumber").value;
        const expDate = document.getElementById("expirationdate").value;
        const cvv = document.getElementById("securitycode").value;
        
        const inputDate = new Date('20' + expDate.split('/')[1], expDate.split('/')[0] - 1);
        const currentDate = new Date();
    
        if (inputDate < currentDate) {
            alert('Expiration date cannot be in the past');
            return;
        }

       
        clientEmit("payment-button",{
            "name": name,
            "cardNumber": cardNumber,
            "expDate": expDate,
            "cvv": cvv
            }, "add_card");
        
       
    //     try {
    //         // Burada sunucudan dönen cevabı kontrol edin 
    //         const isSuccessful = true;

    //         if (isSuccessful) {
    //             // Başarılı durum
    //             displayMessage("success", "success");
    //         } else {
    //             // Başarısız durum
    //             displayMessage("error", "error");
    //         }
    //     } catch (error) {
    //         console.error("Hata oluştu:", error);
    //         displayMessage("error", "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.");
    //     }
    });

    // function displayMessage(type, message) {
    //         window.location.href = '/add-card?msg='+message;
    // }
    
};