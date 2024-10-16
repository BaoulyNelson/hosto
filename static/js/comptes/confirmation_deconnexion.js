// Ouvrir le modal : Dans ce cas, le modal est déjà ouvert, donc pas besoin d'événement de clic
const modal = document.getElementById("logoutModal");
const closeModal = document.getElementsByClassName("close")[0];

// Fermer le modal quand on clique sur "X"
closeModal.onclick = function() {
    modal.style.display = "none"; // Ferme le modal
}

// Fermer le modal quand on clique à l'extérieur
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none"; // Ferme le modal
    }
}
