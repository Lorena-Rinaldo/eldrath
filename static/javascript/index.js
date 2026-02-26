const sections = document.querySelectorAll("section");
let current = 0;
let isScrolling = false;

function updateActive() {
    sections.forEach(s => s.classList.remove("active"));
    sections[current].classList.add("active");
}

function scrollToSection(index) {
    if (index < 0 || index >= sections.length) return;
    isScrolling = true;
    current = index;
    updateActive();

    sections[current].scrollIntoView({
        behavior: "smooth"
    });

    setTimeout(() => {
        isScrolling = false;
    }, 1200);
}

window.addEventListener("wheel", (e) => {
    if (isScrolling) return;

    if (e.deltaY > 0) {
        scrollToSection(current + 1);
    } else {
        scrollToSection(current - 1);
    }
});

updateActive();