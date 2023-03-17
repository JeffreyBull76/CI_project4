/** https://www.youtube.com/watch?v=2IbRtjez6ag **/
document.addEventListener("DOMContentLoaded", function(){

    const cards = document.querySelectorAll(".card")
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            entry.target.classList.toggle("show", entry.isIntersecting)
        })
    },
    )
    
    cards.forEach(card => {
        observer.observe(card)
    })
})
