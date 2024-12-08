$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})




$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString(); // Get the product ID
    var eml = this.parentNode.children[2]; // Select the third child (quantity display)

    $.ajax({
        type: "GET",
        url: "/pluscart/", // Ensure this URL is correctly mapped in your Django `urls.py`
        data: {
            prod_id: id
        },
        success: function (data) {
            // Update the quantity display with the response data
            eml.innerText = data.quantity; // Update quantity dynamically
            document.getElementById("amount").innerText = data.amount; // Update amount dynamically
            document.getElementById("total_amount").innerText = data.total_amount; // Update total amount dynamically
        },
        error: function (error) {
            console.log("Error:", error); // Log any errors for debugging
        }
    });
});



$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString(); // Get the product ID
    var eml = this.parentNode.children[2]; // Select the third child (quantity display)

    $.ajax({
        type: "GET",
        url: "/minuscart/", // Ensure this URL is correctly mapped in your Django `urls.py`
        data: {
            prod_id: id
        },
        success: function (data) {
            // Update the quantity display with the response data
            eml.innerText = data.quantity; // Update quantity dynamically
            document.getElementById("amount").innerText = data.amount; // Update amount dynamically
            document.getElementById("total_amount").innerText = data.total_amount; // Update total amount dynamically
        },
        error: function (error) {
            console.log("Error:", error); // Log any errors for debugging
        }
    });
});





$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString(); // Get the product ID
    var eml = this

    $.ajax({
        type: "GET",
        url: "/removecart/", // Ensure this URL is correctly mapped in your Django `urls.py`
        data: {
            prod_id: id
        },
        success: function (data) {
            // Update the quantity display with the response data
            document.getElementById("amount").innerText = data.amount; // Update amount dynamically
            document.getElementById("total_amount").innerText = data.total_amount; // Update total amount dynamically
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        },
        error: function (error) {
            console.log("Error:", error); // Log any errors for debugging
        }
    });
});