document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');  // Il tuo formset
    const formFields = form.querySelectorAll('input');   // Tutti i campi input del formset

    // Previeni l'invio del form se non tutti i campi sono completati
    form.addEventListener('submit', function(event) {
        let allFieldsFilled = true;

        // Controlla che ogni campo del form sia compilato
        formFields.forEach(function(input) {
            if (!input.value.trim()) {
                allFieldsFilled = false;
                input.classList.add('is-invalid');  // Evidenzia i campi vuoti
            } else {
                input.classList.remove('is-invalid');
            }
        });

        // Se non tutti i campi sono riempiti, blocca l'invio del form
        if (!allFieldsFilled) {
            event.preventDefault();
            alert("Tutti i campi devono essere compilati prima di inviare!");
        }
    });

    // Prevenire l'invio del form quando il codice a barre inserisce qualcosa e preme invio
    formFields.forEach(function(input) {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();  // Impedisce l'invio automatico del form
            }
        });
    });
});