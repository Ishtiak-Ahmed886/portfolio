// Mobile Menu Toggle
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

if (menuToggle && mobileMenu) {
  menuToggle.addEventListener('click', () => {
    const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('open');
  });

  // Close mobile menu on link click
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Animate Skill Bars on Scroll
const skillBars = document.querySelectorAll('.skill-bar-fill');

const animateSkills = () => {
  skillBars.forEach(bar => {
    const rect = bar.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      const width = bar.getAttribute('data-width');
      bar.style.width = width + '%';
    }
  });
};

window.addEventListener('scroll', animateSkills);
window.addEventListener('load', animateSkills);

// Working Contact Form Handler with FormSubmit AJAX & Mailto fallback
const contactForm = document.getElementById('contact-form');
const formSuccess = document.getElementById('form-success');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('contact-form-submit');
    const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Send Message';
    
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Sending...';
    }

    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('https://formsubmit.co/ajax/moonishtiak03@gmail.com', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        contactForm.reset();
        if (formSuccess) {
          formSuccess.hidden = false;
          formSuccess.textContent = '✅ Message sent successfully! I will get back to you shortly.';
          setTimeout(() => {
            formSuccess.hidden = true;
          }, 6000);
        }
      } else {
        throw new Error('Form submission failed');
      }
    } catch (err) {
      // Graceful fallback to mailto
      window.location.href = `mailto:moonishtiak03@gmail.com?subject=${encodeURIComponent(data.subject || 'Portfolio Contact')}&body=${encodeURIComponent(data.message || '')}%0A%0AFrom: ${encodeURIComponent(data.name || '')} (${encodeURIComponent(data.email || '')})`;
      if (formSuccess) {
        formSuccess.hidden = false;
        formSuccess.textContent = '✉️ Message prepared in your mail app. Click Send in your mail client!';
        setTimeout(() => {
          formSuccess.hidden = true;
        }, 6000);
      }
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    }
  });
}

// Navbar Shadow & Blur on Scroll
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});
