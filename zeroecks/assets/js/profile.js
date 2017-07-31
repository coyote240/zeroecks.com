var u2f = u2f || null; 

let module = document.querySelector('.u2f-flow'),
    form = module.querySelector('.u2f-form');

if (!u2f) {
    module.className = module.className + ' unavailable';
}

let registerButton = document.querySelector('.enroll');
registerButton.addEventListener('click', (event) => {
    'use strict';

    onEnroll().then((data) => {
        return getTokenResponse(data);
    }).then((tokenResponse) => {
        console.log(tokenResponse);
    });
});

function getTokenResponse (registerData) {
    'use strict';

    return new Promise((resolve, reject) => {
        u2f.register(
            registerData.appId,
            registerData.registerRequests,
            registerData.registeredKeys,
            (data) => {
                if (data.errorCode) {
                    reject(data);
                } else {
                    resolve(data);
                }
            });
    });
}

function onEnroll () {
    'use strict';

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.addEventListener('load', (event) => {
            let res = JSON.parse(xhr.responseText);
            resolve(res);
        }, false);

        xhr.addEventListener('error', (event) => {
            reject(event);
        }, false);

        xhr.open('GET', '/enroll');
        xhr.send();
    });
}

