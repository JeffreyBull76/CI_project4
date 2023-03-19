/** https://www.youtube.com/watch?v=2IbRtjez6ag **/
document.addEventListener("DOMContentLoaded", function(){

    const cards = document.querySelectorAll(".img-card")
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add("show");
            entry.target.style.animationPlayState = "running";
            observer.unobserve(entry.target);
          }
        })
      }, {once: true});
      
    cards.forEach(card => {
        observer.observe(card)
    })
        
})

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