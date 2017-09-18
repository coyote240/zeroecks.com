import xs from 'xstream';
import {run} from '@cycle/run';
import {a, div, h2, ul, li, button, span, strong, makeDOMDriver} from '@cycle/dom';
import {makeHTTPDriver} from '@cycle/http';
import './u2f-api.js';

// READ DOM: registration button
// WRITE HTTP: request registration
// READ HTTP: registration response
// WRITE DOM: display registration form
// WRITE U2F: u2f registration
// READ U2F: u2f device response


function renderDevice (device) {
    'use strict';

    return li('.registered_device', [
        strong(device.key_nick)//,
        //'&mdash;',
        //span('registered on ' + device.registration_date),
        //a('.delete', '&#128465;')
    ]);
}

function main (sources) {
    'use strict';

    const register$ = sources.DOM.select('.enroll').events('click')
        .map(event =>
            console.log('clicked', event)
        );

    const deviceRequest$ = xs.of({
        url: '/devices',
        category: 'registeredDevices'});

    const deviceResponse$ = sources.HTTP
        .select('registeredDevices')
        .flatten();

    const vdom$ = xs.combine(register$, deviceResponse$)
        .startWith(null)
        .map(({register, deviceResponse}) =>
            div([
                h2('U2F'),
                ul('.registered-device-list', deviceResponse.map(dev => {
                    console.log(dev);
                    renderDevice(dev);
                })),
                button('.enroll', 'Register a new device'),
                span('.error')
            ]));

    return {
        DOM: vdom$,
        HTTP: deviceRequest$
    };
}

const drivers = {
    DOM: makeDOMDriver('#u2f-registration'),
    HTTP: makeHTTPDriver()
};

run(main, drivers);

class U2FModule {

    constructor () {
        if(!this.detectU2F()) {
            let module = document.querySelector('#u2f-registration');
            module.className = module.className + ' unavailable';
            return;
        }

        this.registrationForm = new RegistrationForm();
        this.initRegisterButton();

        this.errors = {
            4: 'You have already registered this device.',
            5: 'Request has timed out.'
        };
    }

    detectU2F () {
        this.u2f = u2f || window.u2f;
        if(this.u2f) {
            return true;
        }
        return false;
    }

    initRegisterButton () {
        let registerButton = document.querySelector('.enroll');

        registerButton.addEventListener('click', event => {
            this.clearError();
            this.requestRegistration().then(data => {
                return this.getTokenResponse(data);
            }).then(tokenResponse => {
                if (!tokenResponse.version) {
                    tokenResponse.version = 'U2F_V2';
                }
                this.registrationForm.presentKeyForm(tokenResponse);
            }).catch(error => {
                console.log(error);
                this.displayError(error);
            });
        });
    }

    requestRegistration () {
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

    getTokenResponse (registerData) {
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

    displayError (error) {
        let message = this.errors[error.errorCode] || 'An error has occurred',
            errorDisplay = document.querySelector('.error');

        this.clearError();
        errorDisplay.appendChild(
            document.createTextNode(message));
    }

    clearError () {
        let errorDisplay = document.querySelector('.error');
        errorDisplay.childNodes.forEach(node => {
            errorDisplay.removeChild(node);
        });
    }
}

class DeviceList {

    constructor () {
        this.deviceList = document.querySelector('.registered-device-list');
        this.xsrf_token = this.deviceList.dataset.xsrfToken;

        this.deviceList.querySelectorAll('.registered-device').forEach((item) => {
            let deleteLink = item.querySelector('.delete');

            deleteLink.addEventListener('click', event => {
                let target = event.target,
                    key = target.dataset.key;

                this.removeDevice({keynick: key}).then(() => {
                    this.deviceList.removeChild(item);
                });
            });
        });
    }

    addDevice (device) {
        let item = document.createElement('li'),
            name = document.createElement('strong');

        name.appendChild(document.createTextNode(device.keynick));
        item.appendChild(name);
        item.appendChild(document.createTextNode(' — '));

        let regDate = document.createElement('time');
        regDate.appendChild(document.createTextNode('registered on '));
        regDate.appendChild(document.createTextNode(device.registration_date));
        item.appendChild(regDate);

        let deleteLink = document.createElement('a');
        deleteLink.setAttribute('href', '');
        deleteLink.setAttribute('class', 'delete');
        deleteLink.addEventListener('click', event => {
            event.preventDefault();
            this.removeDevice(device).then(() => {
                this.deviceList.removeChild(item);
            });
        });
        deleteLink.appendChild(document.createTextNode(' 🗑'));
        item.appendChild(deleteLink);

        this.deviceList.appendChild(item);
    }

    removeDevice (device) {
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
            xhr.setRequestHeader('Content-type',
                'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-XSRFToken', this.xsrf_token);
            xhr.send(`key_nick=${device.keynick}`);
        });
    }
}

class RegistrationForm {

    constructor () {
        this.deviceList = new DeviceList();

        this.initForm();
    }

    initForm () {
        this.form = document.getElementById('u2f-form');
        this.form.addEventListener('submit', event => {
            event.preventDefault();
            let data = new FormData(this.form);
            this.registerDevice(data).then(device => {
                this.deviceList.addDevice(device);
            });
        });
    }

    presentKeyForm (tokenResponse) {
        let deviceResponseField = document.getElementById('deviceResponse');
        deviceResponseField.setAttribute('value', JSON.stringify(tokenResponse));

        this.form.setAttribute('in-progress');
    }

    registerDevice (formData) {
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();

            xhr.addEventListener('load', event => {
                let res = JSON.parse(xhr.responseText);
                resolve(res);
            }, false);

            xhr.addEventListener('error', event => {
                reject(event);
            }, false);

            xhr.open('POST', '/register');
            xhr.send(formData);
        });
    }
}

//new U2FModule();
