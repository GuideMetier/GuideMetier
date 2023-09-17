class GuideMetierAPI {
    // Récupérer des suggestions basées sur un message
    query(message) {
        return $.post('/api/query', {query: message});
    }

    // Récupérer des détails sur un métier spécifique par ID
    getMetierDetail(id) {
        return $.ajax({
            url: `/api/metiers/${id}`,
            method: 'GET'
        });
    }

    // Récupérer une liste de tous les métiers
    getAllMetiers() {
        return $.ajax({
            url: `/api/metiers`,
            method: 'GET'
        });
    }

    // Récupérer des offres d'emploi pour un métier spécifique par ID
    getJobOffersForMetier(id) {
        return $.ajax({
            url: `/api/emplois/${id}`,
            method: 'GET'
        });
    }
}

function nl2br (str, is_xhtml) {
    if (typeof str === 'undefined' || str === null) {
        return '';
    }
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}

$(document).on('click', '#send-btn', async function () {
    var message = $("#query").val();
    if (!message.length) return false;

    // Ajouter le message de l'utilisateur à la liste
    renderUserMessage(message);

    // Traiter les messages de salutation
    if (message.toLowerCase() === 'bonjour' || message.toLowerCase() === 'salut' || message.toLowerCase() === 'coucou') {
        renderBotMessage("Bonjour ! Comment puis-je vous aider ?");
        return;
    }

    // Traiter les messages de remerciement
    if (message.toLowerCase() === 'merci' || message.toLowerCase() === 'mercii'|| message.toLowerCase() === 'merci beaucoup') {
        renderBotMessage("De rien ! N'hésitez pas si vous avez d'autres questions.");
        return;
    }

    // Traiter les messages d'au revoir
    if (message.toLowerCase() === 'au revoir' || message.toLowerCase() === 'bye') {
        renderBotMessage("Au revoir ! À bientôt.");
        return;
    }


    // Scroll en bas du chat
    $('.form').scrollTop($(".form")[0].scrollHeight);

    // On envoie la requête à l'GuideMetierAPI
    let api = new GuideMetierAPI();
    let response = await api.query(message)
    $('.loading-icon').remove();

    if (response.result.length === 0) {
        return renderBotMessage(response.message);
    }

    renderJobList(response.result)

    scrollDown()
});

function renderBotMessage(message) {
    $('.form').append(
        '<div class="bot-inbox inbox">' +
        '<div class="msg-header"><p>' + message + '</p></div>' +
        '</div>'
    );
    $('#query').val('');
    $('.loading-icon').remove();
    scrollDown()

}

$(document).on('click', '.list-group li', async function() {
    $(this).parent().find('.active').removeClass('active')
    $(this).addClass('active')
})

$(document).on('click', '[data-role="job-list"]', async function() {
    renderUserMessage('Je souhaite voir la liste des métiers');

    // On envoie la requête à l'GuideMetierAPI
    let api = new GuideMetierAPI();
    let response = await api.getAllMetiers()

    // On affiche côté client le message transmis
    $('.loading-icon').remove();

    if (response.result.length === 0) return notFound();

    renderAllJobList(response.result, false)
})

$(document).on('click', '[data-role="job-detail"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite en savoir plus sur le metier de ' + $(this).text());

    let api = new GuideMetierAPI();
    let data = await api.getMetierDetail(id);
    let item = data.result;

    let container = '<div class="item-container">';

    container += '<h6>' + item.metier.mainName + '</h6>';
    container += '<p>' + item.label + '</p>';
    if (item.metier.domain) {
        container += '<h7>Domaine :</h7><p>' + item.metier.domain.label + '</p>';
    }

    container += '<h7>Les missions principales:</h7>';
    container += '<p class="desc">' + nl2br(item.metier.description).split("\\n").join('<br>') + '</p>';

    if (item.metier.accessText && item.metier.accessText.length > 0) {
        container += '<h7>Comment y accéder</h7> ' + item.metier.accessText.split("\\n").join('<br>') + '</p>';
    }

    let skillsList = '<ul>';
    $.each(item.skills.domainsSkills, function (i, domainSkill) {
        if (domainSkill.score > 13) {
            skillsList += '<li>' + domainSkill.label + ' (' + domainSkill.score + '%)</li>';
            let stakesList = '<ul>';
            $.each(domainSkill.stakes, function (j, stake) {
                stakesList += '<li>' + stake.label + '</li>';
            });
            skillsList += stakesList + '</ul>';
        }
    });
    skillsList += '</ul>';
    container += '<h7>Ce qu’il faut savoir faire:</h7>' + skillsList;
    container += '</div>';

    $.each(item.workConditionsCategories, function(i, category) {
        let workConditionsList = $('<ul></ul>');
        $.each(category.workConditions, function(j, condition) {
            workConditionsList.append('<li>' + condition.label + '</li>');
        });
        container += '<h7>' + translateLabel(category.label) + ':</h7>' + workConditionsList.prop('outerHTML');
    });

    console.log(item)
    if (item.skills.professionalSoftSkills && item.skills.professionalSoftSkills.length > 0) {
        let professionalSoftSkills = $('<ul></ul>');
        $.each(item.skills.professionalSoftSkills, function(j, condition) {
            professionalSoftSkills.append('<li>' + condition.label + '</li>');
        });
        container += '<h7>Savoir-être professionnels</h7>' + professionalSoftSkills.prop('outerHTML');
    }

    container +=
    `
    <h7>Vidéo de présentation :</h7>
    <div class="text-center">
        <iframe class="embed-responsive-item" id="ytplayer" type="text/html" width="640" height="360" src="${item.metier.videoUrl}" allowfullscreen=""></iframe>
    </div>`

    await renderMessage(container);
    await renderJobDetailActions(id);
    scrollDown();
});

function translateLabel(label) {
    switch(label) {
        case "CONDITIONS_TRAVAIL":
            return "Conditions de travail";
        case "HORAIRE_ET_DUREE_TRAVAIL":
            return "Horaires et durée de travail";
        default:
            return label;
    }
}

function renderJobDetailActions(id) {
    let html =
        'Souhaitez en savoir plus sur ce metier ?' +
        '<button class="btn btn-primary" data-role="job-detail-knowledgeCategories" data-rome="' + id + '">Ce qu\'il faut savoir</button>' +
        '<button class="btn btn-primary" data-role="job-detail-appellations" data-rome="' + id + '">Métiers possibles</button>' +
        '<button class="btn btn-primary" data-role="job-detail-jobOffers" data-rome="' + id + '">Offres d\'emploi</button>' +
        '<button class="btn btn-primary" data-role="job-detail-relatedJobs" data-rome="' + id + '">Métiers proches</button>' +
        '<button class="btn btn-primary" data-role="job-detail-labourMarket" data-rome="' + id + '">Marché du travail</button>'
    return renderMessage(html);
}

$(document).off('click', '[data-role="job-detail-labourMarket"]');
$(document).on('click', '[data-role="job-detail-labourMarket"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite en savoir plus sur le marché du travail pour ce métier');

    let api = new GuideMetierAPI();
    let data = await api.getMetierDetail(id);
    let item = data.result;

    let container = '<div class="item-container card">';

    // Ajout du titre
    container += '<div class="card-header">Le marché du travail</div>'; // Utiliser le composant "card-header" de Bootstrap pour le titre

    container += '<div class="card-body">'; // Contenu principal de la carte

    if (!item.labourMarket) {
        return await renderMessage('Aucune information sur le marché du travail disponible');
    }

    // Affiche les offres d'emploi avec une icône (exemple)
    if (item.labourMarket.jobOffers) {
        container += '<p class="mb-2"><i class="bi bi-briefcase-fill me-2"></i>Offres d\'emploi: <span class="badge bg-primary">' + item.labourMarket.jobOffers +
            '</span> déposées sur Pôle emploi au cours des 12 derniers mois.</p>';
    }

    // Affiche les demandeurs d'emploi avec une icône (exemple)
    if (item.labourMarket.jobSeekers) {
        container += '<p class="mb-2"><i class="bi bi-person-fill me-2"></i>Demandeurs d\'emploi: <span class="badge bg-warning">' + item.labourMarket.jobSeekers + '</span></p>';
    }

    container += '</div>'; // Fin du contenu principal de la carte
    container += '</div>'; // Fin de la carte


    if (item.labourMarket.jobOffers && item.labourMarket.jobSeekers) {
        let alertClass;
        let ratioMessage;
        let ratio = item.labourMarket.jobOffers / item.labourMarket.jobSeekers;

        if (ratio > 1) {
            alertClass = "alert-success";
            ratioMessage = `Bonne nouvelle ! Ce métier dispose de ${Math.round(ratio)}x plus d'offres d'emploi que de demandeurs d'emploi.`;
        } else if (ratio < 1) {
            alertClass = "alert-danger";
            ratioMessage = `Ce métier dispose de ${Math.round(1/ratio)}x plus de demandeurs d'emploi que d'offres d'emploi.`;
        } else {
            alertClass = "alert-info";
            ratioMessage = `Le nombre d'offres d'emploi est égal au nombre de demandeurs d'emploi pour ce métier.`;
        }

        container += `
            <div class="alert ${alertClass} mt-3">
                ${ratioMessage}
            </div>
        `;
    }


    await renderMessage(container);
    scrollDown();
});

$(document).off('click', '[data-role="job-detail-knowledgeCategories"]');
$(document).on('click', '[data-role="job-detail-knowledgeCategories"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite en savoir plus sur ce qu\'il faut savoir dans ce métier');

    let api = new GuideMetierAPI();
    let data = await api.getMetierDetail(id);
    let item = data.result;

    let container = '<div class="item-container">';

    if (!item.skills || !item.skills.knowledgeCategories || item.skills.knowledgeCategories.length == 0) {
        return await renderMessage('Aucune information disponible');
    }

    $.each(item.skills.knowledgeCategories, function(i, category) {
        let knowledgeList = $('<ul></ul>');
        $.each(category.knowledges, function(j, knowledge) {
            knowledgeList.append('<li>' + knowledge.label + '</li>');
        });
        container += '<h7>' + category.label + ':</h7>' + knowledgeList.prop('outerHTML');
    });

    container += '</div>';

    await renderMessage(container);
    scrollDown();
});
;


$(document).on('click', '[data-role="job-detail-jobOffers"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite voir les offres d\'emploi récentes pour ce métier');

    await renderJobOffers(id);
});


$(document).on('click', '[data-role="job-detail-appellations"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite en savoir plus sur les métiers possibles');

    let api = new GuideMetierAPI();
    let data = await api.getMetierDetail(id);
    let item = data.result;

    let container = '<div class="item-container">';

    // Code pour afficher les appellations
    if (item.metier.appellations && item.metier.appellations.length > 0) {
        let appellationList = $('<ul></ul>');
        $.each(item.metier.appellations, function(i, appellation) {
            appellationList.append('<li>' + appellation.label + '</li>');
        });
        container += '<h7>Métiers possibles:</h7>' + appellationList.prop('outerHTML');
    }

    container += '</div>';

    await renderMessage(container);
    scrollDown();
});

$(document).on('click', '[data-role="job-detail-relatedJobs"]', async function() {
    let id = $(this).data('rome');
    renderUserMessage('Je souhaite en savoir plus sur les métiers proches');

    let api = new GuideMetierAPI();
    let data = await api.getMetierDetail(id);
    let item = data.result;

    let container = '<div class="item-container">';

    if (item.relatedJobs && item.relatedJobs.length > 0) {
        let relatedJobsList = $('<ul></ul>');
        $.each(item.relatedJobs, function(i, relatedJob) {
            relatedJobsList.append('<li>' + relatedJob.label + '</li>');
        });
        container += '<h7>Métiers proches:</h7>' + relatedJobsList.prop('outerHTML');
    }

    container += '</div>';

    await renderMessage(container);
    scrollDown();
});




function scrollDown() {
    setTimeout(function() {
        // scroll en bas du chat une fois l'animation CSS terminée
        $('.form').scrollTop($(".form")[0].scrollHeight);
    }, 200);

}

function notFound(item) {
    return $('.form').append(
        '<div class="bot-inbox inbox">' +
            '<div class="msg-header"><p>Désolé, je n\'ai pas compris votre question.</p></div>' +
        '</div>'
    );
}

function renderMessage(message, speed = 3) {
    return new Promise((resolve, reject) => {
        $('.loading-icon').remove();
        let containerHtml =
            '<div class="bot-inbox inbox">' +
            '<div class="msg-header"></div>' +
            '</div>';

        $('.form').append(containerHtml);

        // Select the last ".msg-header" element added
        let $messageBox = $('.form .msg-header').last();

        if (speed === false) {
            $messageBox.html(message);
            scrollDown()
            resolve();
            return;
        }
        // Store the current content of the message
        let currentContent = "";

        // Function that types the message character by character
        function typeMessage(index, speed) {
            if (index < message.length) {
                currentContent += message[index];
                $messageBox.html(currentContent);  // Update with the current content

                setTimeout(() => {
                    typeMessage(index + 1);  // Move to the next character after a delay
                    scrollDown()
                }, speed);  // You can adjust the delay as desired
            } else {
                resolve();  // Resolve the promise when the typing is done
            }
        }

        // Start typing the message
        typeMessage(0, speed);
    });
}

function renderUserMessage(message) {
    // On rajoute le message saisi
    $('.form').append(
        '<div class="user-inbox inbox">' +
        '<div class="msg-header"><p>' + message + '</p></div>' +
        '</div>'
    );

    $('#query').val('');

    // Petit loader en attente de la réponse AJAX
    $('.form').append(
        '<div class="loading-icon lds-ellipsis"><div></div><div></div><div></div><div></div></div>'
    );
}

function renderJobList(jobs) {
    let message = "Voici les métiers qui pourraient vous correspondre :";

    $.each(jobs, function(index, item) {
        message += `<button class="btn btn-primary" data-role="job-detail" data-rome="${item.code || item.romeCode}">${item.mainName || item.label}</button>`;
    });

    renderMessage(message);
}

function renderAllJobList(jobs) {
    let message = "Voici la liste de tous les métiers :";

    $.each(jobs, function(index, item) {
        message += `<button class="btn btn-primary" data-role="job-detail" data-rome="${item.code || item.romeCode}">${item.mainName || item.label}</button>`;
    });

    renderMessage(message, false);
}

async function renderAllMetiers() {
    let api = new GuideMetierAPI();
    let data = await api.getAllMetiers();

    let message = '<ul class="metiers-list">';

    $.each(data.result, function(index, item) {
        message += `<button class="btn btn-primary" data-role="job-detail" data-rome="${item.romeCode}">${item.mainName || item.label}</button>`;
    });

    message += '</ul>';
    renderMessage(message);
}

async function renderJobOffers(id) {
    let api = new GuideMetierAPI();
    let offersResponse = await api.getJobOffersForMetier(id);
    let offers = offersResponse.result;

    if(offersResponse.count === 0) {
        renderMessage('<div class="guide-inbox inbox">Aucune offre d\'emploi disponible pour ce métier.</div>');
        return;
    }


    let message = 'Voici les recentes offres d\'emploi disponibles pour ce métier :';

    let table = '<table class="offers-table">';
    table += '<thead><tr>' +
        '<th width="130px">Date</th>' +
        '<th>Titre</th>' +
        '<th width="130px">Localisation</th>' +
        '<th width="180px">Contrat</th>' +
        '<th>Description</th>' +
        '<th width="100px"></th>' +
        '</tr></thead><tbody>';

    $.each(offers, function(index, offer) {
        let detailUrl = 'https://candidat.pole-emploi.fr/offres/recherche/detail/';
        let shortDescription = offer.description.length > 150 ? offer.description.substr(0, 147) + "..." : offer.description;

        var date = offer.creationDate
        var m = moment(date);
        table += `<tr>
            <td>${m.fromNow()}</td>
            <td>${offer.title}</td>
            <td>${offer.location}</td>
            <td>${offer.contractType}</td>
            <td>${shortDescription}</td>
            <td>
                <a target="_blank" href="${detailUrl + offer.referenceOffre}" class="btn btn-primary btn-sm">
                    Voir l'offre
                </a>
            </td>
        </tr>`;
    });

    table += '</tbody></table>';

    await renderMessage(message);
    await renderMessage(table);
}


$(document).on('keyup', '#query', function(e) {
    // Envoi de la pquête lorsqu'on appuie sur Entrée dans le contexte du chat
    if ((e.keyCode || e.which) === 13) {
        $('#send-btn').trigger('click')
    }
});
    