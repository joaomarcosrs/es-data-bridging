$(document).ready(function(){

    $('#researchSelectId').change(function(){
        var selectedResearch = $(this).val();
        $.ajax({
            type: 'GET',
            url:'' + selectedResearch,
            success: function(response){
                $('#aggregateResultContainer').html(response);
            },
            error: function(response){
                console.log("Error loading research data.");
            }
        });
    });
});