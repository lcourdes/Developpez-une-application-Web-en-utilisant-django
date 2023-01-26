var loadFile = function(event){
    var output = document.getElementById('preview-img');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function(){
        URL.revokeObjectURL(output.src)
    }
};