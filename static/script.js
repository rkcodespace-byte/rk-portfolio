
const themeToggle = document.getElementById("theme-toggle");

function updateThemeButton() {
    if (!themeToggle) return;

    const isLight = document.body.classList.contains("light-theme");
    themeToggle.textContent = isLight ? "🌙" : "☀️";
    themeToggle.setAttribute(
        "aria-label",
        isLight ? "Switch to dark theme" : "Switch to light theme"
    );
}

const savedTheme = localStorage.getItem("rk-theme");

if (savedTheme === "light") {
    document.body.classList.add("light-theme");
}

updateThemeButton();

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");

        const theme = document.body.classList.contains("light-theme")
            ? "light"
            : "dark";

        localStorage.setItem("rk-theme", theme);
        updateThemeButton();
    });
}

const contactForm = document.getElementById("contact-form");
const formStatus = document.getElementById("form-status");

if (contactForm && formStatus) {
    contactForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const submitButton = contactForm.querySelector(
            'button[type="submit"]'
        );

        const originalText = submitButton.textContent;

        submitButton.disabled = true;
        submitButton.textContent = "Sending...";
        formStatus.textContent = "";

        try {
            const response = await fetch("/api/contact", {
                method: "POST",
                body: new FormData(contactForm)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.message || "Please check your form details."
                );
            }

            formStatus.textContent = result.message;
            contactForm.reset();
        } catch (error) {
            formStatus.textContent =
                error.message || "Unable to send your message. Please try again.";
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
}
