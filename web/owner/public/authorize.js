(() => {
  const form = document.getElementById("oauth-authorize-form");
  if (!form) return;

  const button = document.getElementById("oauth-authorize-button");
  const status = document.getElementById("oauth-authorize-status");
  let submitting = false;

  const reset = () => {
    submitting = false;
    button.disabled = false;
    button.textContent = "Authorize agent";
    status.hidden = true;
  };

  window.addEventListener("pageshow", reset);
  form.addEventListener("submit", (event) => {
    if (submitting) {
      event.preventDefault();
      return;
    }
    if (!form.checkValidity()) return;
    submitting = true;
    button.disabled = true;
    button.textContent = "Authorizing…";
    status.hidden = false;
  });
})();
