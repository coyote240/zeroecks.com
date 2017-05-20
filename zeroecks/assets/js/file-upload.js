/**************************************************
 *
 *  File Dropzone
 *
 ***************************************************/
let dropZone = document.querySelector('.dropzone'),
    xsrf_token = dropZone.getAttribute('token');

dropZone.addEventListener('drop', (event) => {
    'use strict';
    event.preventDefault();

    let transfer = event.dataTransfer;

    if (transfer.items) {
        for (let i = 0; i < transfer.items.length; i++) {
            let item = transfer.items[i];

            if (item.kind === 'file') {
                let f = item.getAsFile();
                let article = new Article('/articles/new');
                article.uploadArticle(f).then((res) => {
                    window.location = `/articles/${res.id}`;
                });
            }
        }
    }
});

dropZone.addEventListener('dragover', (event) => {
    'use strict';
    event.preventDefault();
}, false);

dropZone.addEventListener('dragend', (event) => {
    'use strict';
    event.preventDefault();

    let transfer = event.dataTransfer;

    if (transfer.items) {
        for (let i = 0; i < transfer.items.length; i++ ) {
            let item = transfer.items[i];
            item.remove();
        }
    }
}, false);

/**************************************************
 *
 *  Article Item Events
 *
 ***************************************************/

let publishers = document.querySelectorAll('tr.article-info input[type="checkbox"]');
publishers.forEach((publisher) => {
    'use strict';
    publisher.addEventListener('change', (event) => {
        let target = event.target,
            value = target.value,
            checked = target.checked;

        console.log(value, checked);
    });
});

/**************************************************
 *
 *  Article API
 *
 ***************************************************/
class Article {

    constructor (path) {
        this.reader = new FileReader();
        this.xhr = new XMLHttpRequest();
        this.path = path;
    }

    uploadArticle (file) {
        return new Promise((resolve, reject) => {
            this.xhr.addEventListener('load', (event) => {
                let res = JSON.parse(this.xhr.responseText);
                resolve(res);
            }, false);

            this.xhr.addEventListener('error', (event) => {
                reject(event);
            }, false);

            this.xhr.open('POST', this.path);
            this.reader.onload = (event) => {
                this.xhr.setRequestHeader('X-XSRFToken', xsrf_token);
                this.xhr.send(event.target.result);
            };
            this.reader.readAsText(file);
        });
    }

    publishArticle (id, published) {

    }

    deleteArticle (id) {
    }
}
