document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".image");

    elements.forEach(element => {
        element.addEventListener("mouseover", function () {
            elements.forEach(el => el.classList.remove("hover"));
            element.classList.add("hover");
        });

        element.addEventListener("click", function (event) {
            event.stopPropagation();
            element.classList.add("hover");
        });
    });

    document.addEventListener("click", function () {
        elements.forEach(element => element.classList.remove("hover"));
    });
});
