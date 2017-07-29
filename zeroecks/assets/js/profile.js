var u2f = u2f || null; 

let module = document.querySelector('.u2f-flow'),
    form = module.querySelector('.u2f-form');

if (!u2f) {
    module.className = module.className + ' unavailable';
}
