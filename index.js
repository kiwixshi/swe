disease_info = {
    'corn_healthy':{
        'symptoms': "Healthy corn plants have tall, green stalks with no lesions or discoloration on the leaves.",
        'treatment': "Ensure proper watering, fertilization, and pest management.",
        'more info': "Healthy corn plants grow well in fertile, well-drained soils with adequate sunlight."
    },
    'corn_common_rust':{
        'symptoms': "Reddish-brown pustules on both sides of the leaves. Severe infections may cause leaves to yellow and die early.",
        'treatment': "Apply fungicides, use rust-resistant hybrids, and rotate crops",
        'more info': "Caused by the fungus Puccinia sorghi, it thrives in cool, moist environments."
    },
    'corn_northern_leaf_blight':{
        'symptoms': " Long, elliptical, gray-green lesions on leaves, which later turn tan. Severe infections can cause premature leaf death.",
        'treatment': " Use resistant hybrids, apply fungicides, and rotate crops to reduce the presence of the fungus in soil.",
        'more info': "Caused by the fungus Setosphaeria turcica, it thrives in humid environments."
    },
    'corn_gray_leaf_spot':{
        'symptoms': "Small, rectangular lesions that start off yellow and turn gray on corn leaves. Over time, they can merge, leading to leaf death.",
        'treatment': "Use resistant hybrids, apply fungicides, and rotate crops.",
        'more info': "Caused by the fungus Cercospora zeae-maydis, it can lead to significant yield loss if not controlled."
    },
    'potato_healthy':{
        'symptoms': "Healthy potato plants have strong, green leaves with no discoloration or lesions.",
        'treatment': "Regular care includes proper watering, balanced fertilization, and good pest control practices.",
        'more info': "Healthy potatoes can grow in well-drained, slightly acidic soils with good crop rotation to avoid disease buildup."
    },
    'potato_early_blight':{
        'symptoms': "Dark, concentric rings (target-like spots) on older leaves. Lesions can also appear on stems and tubers, leading to rot.",
        'treatment': "Apply fungicides, remove infected plant debris, and avoid overhead watering to reduce humidity.",
        'more info': "Caused by Alternaria solani, this disease thrives in warm, humid conditions."
    },
    'potato_late_blight':{
        'symptoms': "Dark, water-soaked lesions on leaves, stems, and tubers. Leaves may dry up and turn brown, while tubers develop dark, sunken spots.",
        'treatment': "Apply fungicides, remove and destroy infected plants, and improve air circulation. Use blight-resistant potato varieties.",
        'more info': "Caused by Phytophthora infestans, it spreads rapidly in cool, wet conditions."
    }
}




$(document).ready(function () {
    $('#upload-form').on('submit', function (e) {
        e.preventDefault(); // Prevent form submission

        var formData = new FormData(this);

        $.ajax({
            url: 'http://127.0.0.1:5000/predict', // Update to your Flask app's prediction endpoint
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.prediction) {
                    console.log('woah');
                    // $('#img-upl').html('<img src="'+m+'"></img>');
                    $('#result').html('<h3>Prediction: ' + data.prediction + '</h3>'+
                        '<h5>Symptoms: </h5>'+'<p>'+ disease_info[data.prediction]['symptoms']+'</p>'+
                        '<h5>Treatment: </h5>'+'<p>'+ disease_info[data.prediction]['treatment']+'</p>'+
                        '<h5>More Information: </h5>'+'<p>'+ disease_info[data.prediction]['more info']+'</p>'
                    );
                } else {
                    $('#result').html('<h5>' + data.error + '</h5>');
                }
            },
            error: function () {
                $('#result').html('<h5>Error: Could not process the request</h4>');
            }
        });
    });


    $('#file').change(function(e){
        const file = e.target.files[0];  // Get the file from the input
        if (file) {
            const reader = new FileReader();  
            reader.onload = function(event) {
                $('#preview').attr('src', event.target.result);  // Set the image src to the file data URL
                $('#preview').show();  // Show the image preview
            }
            reader.readAsDataURL(file);  // Read the file as a data URL (base64-encoded string)
        }
    });

    // Handle dummy API request
    $('#hello-form').on('submit', function (e) {
        e.preventDefault(); // Prevent form submission

        $.ajax({
            url: 'http://127.0.0.1:5000/hello', // Backend endpoint for dummy API
            type: 'POST',
            success: function (data) {
                $('#hello-result').html('<h5>' + data.message + ' from the frontend</h4>');
            },
            error: function () {
                $('#hello-result').html('<h5>Error: Could not process the request</h4>');
            }
        });
    });
});

