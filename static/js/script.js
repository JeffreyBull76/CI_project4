document.addEventListener("DOMContentLoaded", function() {

  const cards = document.querySelectorAll(".img-card");

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.5
  });

  cards.forEach(card => {
    const img = card.querySelector('img');
    if (img.complete) {
      observer.observe(card);
    } else {
      img.addEventListener('load', function() {
        observer.observe(card);
      });
    }
  });

});

function copyToClipboard(id, message) {
  const promptText = document.getElementById(id).innerText;
  navigator.clipboard.writeText(promptText);
  alert(message);
}