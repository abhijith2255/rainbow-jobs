document.addEventListener('DOMContentLoaded', () => {
    const authSlider = document.getElementById('authSlider');
    const showRegisterBtn = document.getElementById('showRegister');
    const showLoginBtn = document.getElementById('showLogin');

    if (showRegisterBtn && showLoginBtn && authSlider) {
        // Slide left to show Register form
        showRegisterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            authSlider.classList.add('slide-to-register');
        });

        // Slide right to show Login form
        showLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            authSlider.classList.remove('slide-to-register');
        });
    }
});