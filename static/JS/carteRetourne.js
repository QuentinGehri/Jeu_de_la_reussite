function faireFonctionnerLeJeu(listePosCorr) {
    document.addEventListener('DOMContentLoaded', function () {
        const cards = document.querySelectorAll('.card');
        let isFlipping = false;
        let cardsFlipped = [];
        let tour = 1;
        let cardFlipped = null;

        cards.forEach(card => {
            card.addEventListener('click', function () {
                // Vérifie si une animation est en cours
                if (!isFlipping) {
                    // Retourne la carte
                    if (tour !== 1) {
                        var carteAvant = cardFlipped;
                        var carte = carteAvant.querySelector('.back');
                        var imageCarte =  carte.querySelector('img');
                        var altImage = imageCarte.alt
                        var posCarteCliquee = parseInt(this.id);
                        //var listePosCorr = {{ liste_pos_correct|to_json }}
                        console.log(altImage + " " + listePosCorr[posCarteCliquee - 1]);
                        if (altImage === listePosCorr[posCarteCliquee - 1] ) {
                            cardFlipped = retournerCarte(cardFlipped, isFlipping, this)
                            var main = document.createElement("div");
                            main.id = "main";
                            main.appendChild(cardFlipped.cloneNode(true));
                            document.body.appendChild(main);
                            carte.remove();
                            nouvelleImage = document.createElement("img");
                            nouvelleImage.src(imageCarte);
                            nouvelleImage.alt(altImage);
                            this.querySelector('.back').appendChild(nouvelleImage);
                        } else {
                            messageErreur("Mauvaise carte !")
                        }
                    } else if (this.id === '36' && tour === 1) {
                        cardFlipped = retournerCarte(cardFlipped, isFlipping, this);
                        tour++;
                    } else {
                        messageErreur("Il faut retourner la carte en bas à droite !")
                    }
                }
            });
        });
    });
}

function retournerCarte(cardFlipped, isFlipping, carte){
    /*if (!cardsFlipped.includes(carte)) {*/
        isFlipping = true;
        carte.classList.toggle('flipped');
        cardFlipped = carte;
        //cardsFlipped.push(carte);
        setTimeout(() => {
            isFlipping = false;
        }, 500)
    /*}*/ /*else {
        // Si une carte est déjà retournée, réinitialisez la variable flippedCard après un délai
        isFlipping = true;
        i = cardsFlipped.indexOf(this);
        cardsFlipped.splice(i, 1);
        this.classList.remove('flipped');
        setTimeout(() => {
            isFlipping = false;
        }, 1000); // Ajustez le délai en fonction de la durée de votre transition
    }*/
    return cardFlipped;
}

function messageErreur(message) {
    var nouvelleDiv = document.createElement("div");
    nouvelleDiv.id = "erreur";
    var nouvelH1 = document.createElement("h1");
    nouvelH1.textContent = message;
    nouvelleDiv.appendChild(nouvelH1);
    document.body.appendChild(nouvelleDiv);
    setTimeout(function() {
        var div = document.getElementById("erreur");
        if (div) {
            div.remove();
        }
    }, 2000);
}