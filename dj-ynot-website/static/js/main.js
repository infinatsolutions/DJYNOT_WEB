(() => {
  const menuToggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.menu');
  const links = document.querySelectorAll('.menu a[href^="#"]');
  const form = document.getElementById('booking-form');
  const status = document.getElementById('form-status');
  const currentYear = document.getElementById('current-year');

  if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
  }

  if (menuToggle && menu) {
    menuToggle.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', String(isOpen));
      menuToggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    });

    links.forEach((link) => {
      link.addEventListener('click', () => {
        menu.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', 'Open navigation menu');
      });
    });
  }

  const setStatus = (message, isError = false) => {
    if (!status) return;
    status.textContent = message;
    status.style.color = isError ? '#ff8b8b' : '#e6b766';
  };

  const validate = (data) => {
    if (!data.fullName.trim()) return 'Full Name is required.';
    if (!/^\S+@\S+\.\S+$/.test(data.email)) return 'Please enter a valid email address.';
    if (!data.preferredService) return 'Please choose a preferred service.';
    if (!data.preferredContactMethod) return 'Please choose a preferred contact method.';
    if (!data.message.trim()) return 'Please tell us about your event.';
    return '';
  };

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();

      const formData = new FormData(form);
      const payload = {
        fullName: String(formData.get('fullName') || '').trim(),
        email: String(formData.get('email') || '').trim(),
        phone: String(formData.get('phone') || '').trim(),
        eventDate: String(formData.get('eventDate') || '').trim(),
        eventType: String(formData.get('eventType') || '').trim(),
        eventLocation: String(formData.get('eventLocation') || '').trim(),
        guestCount: String(formData.get('guestCount') || '').trim(),
        preferredService: String(formData.get('preferredService') || '').trim(),
        preferredContactMethod: String(formData.get('preferredContactMethod') || '').trim(),
        message: String(formData.get('message') || '').trim(),
        website: String(formData.get('website') || '').trim()
      };

      const validationError = validate(payload);
      if (validationError) {
        setStatus(validationError, true);
        return;
      }

      if (payload.website) {
        setStatus('Submission blocked.', true);
        return;
      }

      const submitButton = form.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      const originalText = submitButton.textContent;
      submitButton.textContent = 'Sending...';
      setStatus('');

      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.message || 'Request failed. Please try again.');
        }

        form.reset();
        setStatus(result.message || 'Booking request sent successfully.');
      } catch (error) {
        setStatus(error.message || 'Unable to send your booking request right now.', true);
      } finally {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
      }
    });
  }
})();
