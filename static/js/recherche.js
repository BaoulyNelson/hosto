document.getElementById("search-button").addEventListener("click", function() {
    var form = document.getElementById("search-form");
    form.style.display = (form.style.display === "none" || form.style.display === "") ? "block" : "none";
    if (form.style.display === "block") {
        document.querySelector('input[name="q"]').focus(); // Met le focus sur le champ de recherche
    }
});