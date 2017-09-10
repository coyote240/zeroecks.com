class U2FModule {

    constructor () {
        if(!this.detectU2F()) {
            let module = document.querySelector('.u2f-registration');
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

let module = new U2FModule();
