$(document).ready(function(){
    var baseURL = '';

    document.getElementById("researchSelectId").addEventListener("change", function(){
        var selectedResearch = $(this).val();
        
        document.getElementById("aggregateSelectId").innerHTML = '';
        baseURL = window.location.href + selectedResearch + '/'
        $.ajax({
            type: "GET",
            url: baseURL,
            dataType: "json",
            success: function(response){
                var select = document.getElementById('aggregateSelectId');
                
                var defaultOption = document.createElement("option");
                defaultOption.value = "";
                defaultOption.innerHTML = "-------";
                select.appendChild(defaultOption);
                
                for (var i=0; i<response.aggregated_data.length; i++){
                    var option = document.createElement("option");
                    option.title = response.aggregated_data[i]["aggregate_name"];
                    option.value = response.aggregated_data[i]["aggregate_id"];
                    option.innerHTML = response.aggregated_data[i]["aggregate_name"].slice(0, 100);
                    select.appendChild(option);
                }
            },
            error: function(response){
                console.log("Error loading aggregate data.");
            }
        });
    });
    
    document.getElementById("aggregateSelectId").addEventListener("change", function(){
        var aggregateSelect = $(this).val();
        console.log(baseURL + aggregateSelect + "/")
        $.ajax({
            type: "GET",
            url: baseURL + aggregateSelect + "/",
            dataType: "json",
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log("Error loading aggregate data.");
            }
        });
    });
});