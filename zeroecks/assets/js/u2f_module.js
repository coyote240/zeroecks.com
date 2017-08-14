var u2f = u2f || window.u2f || {};

let module = document.querySelector('.u2f-flow'),
    form = module.querySelector('.u2f-form');

if (!u2f) {
    module.className = module.className + ' unavailable';
}

let registerButton = document.querySelector('.enroll');
registerButton.addEventListener('click', event => {
    'use strict';

    makeRegisterRequest().then((data) => {
        return getTokenResponse(data);
    }).then(
        tokenResponse => {
            presentKeyForm(tokenResponse);
        },
        error => {
            if (error.errorCode === 4) {
                console.log('Device already registered.');
            }
        }
    );
});

let registeredDevices = document.querySelectorAll('.registered-device .delete'),
    registeredDeviceList = document.querySelector('.registered-device-list'),
    xsrf_token = registeredDeviceList.dataset.xsrfToken;
registeredDevices.forEach(dev => {
    'use strict';
    dev.addEventListener('click', event => {
        let target = event.target;
        deleteRegisteredDevice(target.dataset.key);
    });
});

function makeRegisterRequest () {
    'use strict';

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.addEventListener('load', event => {
            let res = JSON.parse(xhr.responseText);
            resolve(res);
        }, false);

        xhr.addEventListener('error', event => {
            reject(event);
        }, false);

        xhr.open('GET', '/register');
        xhr.send();
    });
}

function getTokenResponse (registerData) {
    'use strict';

    console.log(registerData);

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

function presentKeyForm (tokenResponse) {
    'use strict';

    // Workaround for Mozilla plugin that fails to provide a protocol version.
    if (!tokenResponse.version) {
        tokenResponse.version = 'U2F_V2';
    }

    console.log(tokenResponse);

    let deviceResponseField = document.getElementById('deviceResponse');
    deviceResponseField.setAttribute('value', JSON.stringify(tokenResponse));
}

function completeRegisterRequest (tokenResponse) {
    'use strict';
}

function deleteRegisteredDevice (keynick) {
    'use strict';

    console.log(keynick);

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.addEventListener('load', event => {
            let res = JSON.parse(xhr.responseText);
            resolve(res);
        }, false);

        xhr.addEventListener('error', event => {
            reject(event);
        }, false);

        xhr.open('DELETE', '/register');
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-XSRFToken', xsrf_token);
        xhr.send(`key_nick=${keynick}`);
    });
}