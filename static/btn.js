
// Para ver el slidebar
function slide(){
    var slides = document.getElementById("slides");
    if(slides.classList.contains("hidden")){
        slides.classList.remove("hidden")
    } else {
        slides.classList.add("hidden")
    }
}

function menuUser(){
    var menuUser = document.getElementById("menuUser");
    if(menuUser.classList.contains("hidden")){
        menuUser.classList.remove("hidden")
    } else {
        menuUser.classList.add("hidden")
    }
}

// para el boton de agregar nuevo gasto
function add_gasto(){
    var addGasto = document.getElementById("addGasto");
    var closeGasto = document.getElementById("closeGasto");

    if(addGasto.classList.contains("hidden")){
        addGasto.classList.remove("hidden")
        closeGasto.classList.add("hidden")
    } else {
        addGasto.classList.add("hidden")
        closeGasto.classList.remove("hidden")
    }
    
}

// para el boton de agregar nuevo ingreso
function add_ingreso(){
    var addIngreso = document.getElementById("addIngreso");
    var closeIngreso = document.getElementById("closeIngreso");

    if(addIngreso.classList.contains("hidden")){
        addIngreso.classList.remove("hidden")
        closeIngreso.classList.add("hidden")
    } else {
        addIngreso.classList.add("hidden")
        closeIngreso.classList.remove("hidden")
    }
    
}

// para el boton de agregar nuevo ahorro
function add_ahorro(){
    var addAhorro = document.getElementById("addAhorro");
    var closeAhorro = document.getElementById("closeAhorro");

    if(addAhorro.classList.contains("hidden")){
        addAhorro.classList.remove("hidden")
        closeAhorro.classList.add("hidden")
    } else {
        addAhorro.classList.add("hidden")
        closeAhorro.classList.remove("hidden")
    }
    
}