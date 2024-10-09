function toggleFields() {
    var tipo = document.getElementById("id_product_type")
    var cpu = document.getElementById("id_cpu")
    var ram = document.getElementById("id_ram")
    var storage = document.getElementById("id_storage_size")
    var cpulabel = cpu.labels[0]
    var ramlabel = ram.labels[0]
    var storagelabel = storage.labels[0]

    if(tipo.value === 'Accessory' ) {
        cpu.style.display = "none"
        ram.style.display = "none"
        storage.style.display = "none"
        cpulabel.style.display = "none"
        ramlabel.style.display = "none"
        storagelabel.style.display = "none"
    }
    else {
        cpu.style.display = "block"
        ram.style.display = "block"
        storage.style.display = "block"
        cpulabel.style.display = "block"
        ramlabel.style.display = "block"
        storagelabel.style.display = "block"
    }
}
document.addEventListener("DOMContentLoaded", function() {
    toggleFields()
    document.getElementById("id_product_type").addEventListener("change", toggleFields)
});