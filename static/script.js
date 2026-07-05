const imageInput = document.getElementById("imageInput");

const preview = document.getElementById("preview");

if(imageInput){

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(file){

preview.style.display="block";

preview.src=URL.createObjectURL(file);

}

});

}

document.querySelectorAll(".feature-card").forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-8px)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0px)";

});

});