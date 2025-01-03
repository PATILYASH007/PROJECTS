const $ = (selector) => {
    return document.querySelector(selector);
}
const Hour = $('.Hour');
const Dot = $('.Dot');
const Min = $('.Min');
const week = $('.week');
let showDot = true;

function update() {
    showDot = !showDot;
    const now = new Date();

    if (showDot) {
        Dot.classList.add('invisible');
    }
    else {
        Dot.classList.remove('invisible');
    }
    Hour.textContent = String(now.getHours()).padStart(2, '0');
    Min.textContent = String(now.getMinutes()).padStart(2, '0');

    Array
        .from(week.children)
        .forEach(
            (ele) => {
                ele.classList.remove('active');
            }
        );
    week
        .children[now.getDay()]
        .classList
        .add('active');
};

setInterval(update, 500);