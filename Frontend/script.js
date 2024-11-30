document.addEventListener('DOMContentLoaded', () => {
    const typewriter = document.getElementById('typewriter');
    const phrases = ['EquiPay', 'Pay It Equal', 'Split and Settle'];
    let phraseIndex = 0;
    let charIndex = 0;
  
    const type = () => {
      if (charIndex < phrases[phraseIndex].length) {
        typewriter.textContent += phrases[phraseIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, 150);
      } else {
        setTimeout(erase, 1000);
      }
    };
  
    const erase = () => {
      if (charIndex > 0) {
        typewriter.textContent = phrases[phraseIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, 100);
      } else {
        phraseIndex = (phraseIndex + 1) % phrases.length;
        setTimeout(type, 500);
      }
    };
  
    type();
  
    // Login form submission
    document.getElementById('loginForm')?.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Calling /login API...');
      // Add API call logic here
    });
  
    // Signup form submission
    document.getElementById('signupForm')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm_password').value;
  
      if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
      }
  
      alert('Calling /registerUser API...');
      // Add API call logic here
    });
  });