function faireFonctionnerLeJeu(listePosCorr, form, action) {
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
                        if (tour === 2) {
                            var carteAvant = cardFlipped; // recupere la carte avant
                        } else {
                            var carteAvant = document.getElementById("main");
                        }
                        var carte = carteAvant.querySelector('.back'); // recup la carte en elle meme
                        var imageCarte = carte.querySelector('img'); //  recup l'image de la carte
                        var lienImage = imageCarte.getAttribute('src'); // recup le lien de l'image
                        var altImage = imageCarte.getAttribute('alt'); //  recup son alt
                        var posCarteCliquee = parseInt(this.id); // par la posititon
                        console.log(altImage + " " + listePosCorr[posCarteCliquee - 1]); // debug
                        if (altImage === listePosCorr[posCarteCliquee - 1]) { // si la carte est à la meme position que le clic du joueur
                            let main = document.getElementById("main");
                            if (!main) {
                                main = document.createElement("div");
                                main.id = "main";
                                document.body.appendChild(main);
                            } else {
                                main.innerHTML = "";
                            }
                            cardFlipped = retournerCarte(cardFlipped, isFlipping, this) // retourne la bonne carte
                            main.appendChild(cardFlipped.cloneNode(true)); // rajoute la carte retournée dans la main
                            carte.remove(); // enleve la carte de ou elle etait car elle est maintenant dans la main
                            let nouvelleImage = document.createElement("img"); // creer un nouvelle img
                            nouvelleImage.src = lienImage; // rajoute le lien de l'image de la carte choisie
                            nouvelleImage.alt = altImage; // rajoute son alt
                            this.querySelector('.back').querySelector('img').remove(); // enleve l'ancienne
                            this.querySelector('.back').appendChild(nouvelleImage); // rajoute la nouvelle
                            if (main.querySelector('td').querySelector('.back')
                                .querySelector('img').getAttribute('alt') === '6C') {
                                gameOver(tour, form, action);
                            }
                            tour++; // passe au tour suivant
                        } else {
                            messageErreur("Mauvaise carte !");
                        }
                    } else if (this.id === '36' && tour === 1) {
                        cardFlipped = retournerCarte(cardFlipped, isFlipping, this);
                        if (cardFlipped.querySelector('.back').querySelector('img')
                            .getAttribute('alt') === '6C') {
                            gameOver(tour, form, action);
                        }
                        tour++;
                    } else {
                        messageErreur("Il faut retourner la carte en bas à droite !");
                    }
                }
            });
        });
    });
}

function gameOver(tour, form, action) {
    let pointsPhrase = " point";
    if (tour > 1) {
        pointsPhrase += "s"
    }
    //messageErreur("Game over ! " + tour + pointsPhrase);
    createModal(tour, pointsPhrase, form, action);
}

function createModal(points, pointsPhrase, form, action) {
        var modal = document.createElement("div");
        modal.classList.add("modal");

        var modalContent = document.createElement("div");
        modalContent.classList.add("modal-content");

        var closeBtn = document.createElement("span");
        closeBtn.classList.add("close");
        closeBtn.innerHTML = "&times;";

        closeBtn.addEventListener("click", function () {
            document.body.removeChild(modal);
        });

        modalContent.appendChild(closeBtn);

        var modalTitle = document.createElement("h2");
        modalTitle.textContent = "Game over";
        modalContent.appendChild(modalTitle);

        var modalText = document.createElement("p");
        modalText.textContent = "Vous avez fait " + points + pointsPhrase;
        modalContent.appendChild(modalText);

        // Créer un formulaire
        var formElement = document.createElement("form");
        formElement.method = "POST";
        action = action.replace(/^"|"$/g, '');
        action = action.replace(/\//g, '');
        formElement.action = action;


        // Ajouter les champs cachés au formulaire
        formElement.appendChild(createHiddenInput("csrf_token", form.csrf_token.value));
        formElement.appendChild(createHiddenInput("points", points));

        // Créer le bouton de soumission du formulaire
        var submitButton = document.createElement("button");
        submitButton.type = "submit";
        submitButton.textContent = form.submit_label;
        formElement.appendChild(submitButton);

        // Ajouter le formulaire au contenu du modal
        modalContent.appendChild(formElement);

        modal.appendChild(modalContent);
        document.body.appendChild(modal);
}

function createHiddenInput(name, value) {
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = name;
    input.value = value;
    return input;
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
    let nouvelleDiv = document.createElement("div");
    nouvelleDiv.id = "erreur";
    let nouvelH1 = document.createElement("h1");
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