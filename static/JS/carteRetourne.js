document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.card');
    let isFlipping = false;
    let cardsFlipped = [];

    cards.forEach(card => {
        card.addEventListener('click', function () {
            // Vérifie si une animation est en cours
            if (!isFlipping) {
                // Retourne la carte
                if (!cardsFlipped.includes(this)) {
                    isFlipping = true;
                    this.classList.toggle('flipped');
                    // Si aucune carte n'est déjà retournée, enregistrez celle-ci comme la carte actuellement retournée
                    cardsFlipped.push(this);
                    setTimeout(() => {
                        isFlipping = false;
                    }, 500)
                } else {
                    // Si une carte est déjà retournée, réinitialisez la variable flippedCard après un délai
                    isFlipping = true;
                    i = cardsFlipped.indexOf(this);
                    cardsFlipped.splice(i, 1);
                    this.classList.remove('flipped');
                    setTimeout(() => {
                        isFlipping = false;
                    }, 1000); // Ajustez le délai en fonction de la durée de votre transition
                }
            }
        });
    });
});
