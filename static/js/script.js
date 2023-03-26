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

function copyToClipboard() {
    const promptText = document.getElementById("prompt-text").innerText;
    navigator.clipboard.writeText(promptText);
    alert("Prompt copied to clipboard!");
}

function copyToClipboard() {
    const promptText = document.getElementById("negprompt-text").innerText;
    navigator.clipboard.writeText(promptText);
    alert("Negative prompt copied to clipboard!");
}

function copyToClipboard() {
    const promptText = document.getElementById("method-text").innerText;
    navigator.clipboard.writeText(promptText);
    alert("Method copied to clipboard!");
}