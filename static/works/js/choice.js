let refs2 = [];
let temp = [];
let final;

function start() {
    document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
}

function select1() {
    if (refs1.length == 2 && refs2.length != 0) {
        refs2 = refs2.concat(refs1.slice(0, 1));
        refs1.shift();
        refs1.pop();
        temp = refs1;
        refs1 = refs2;
        refs2 = temp;
        console.log(refs1, refs2)
        document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
        document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    } else if (refs1.length == 2 && refs2.length == 0) {
        selected_photo_ref = refs1.slice(0, 1)
        document.getElementById('selected_photo_ref').value = selected_photo_ref;
        document.getElementById('end').submit();
    } else {
        refs2 = refs2.concat(refs1.slice(0, 1));
        refs1.shift();
        refs1.pop();
        console.log(refs1, refs2)
        document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
        document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    }
}

function select2() { 
    if (refs1.length == 2 && refs2.length != 0) {
        refs2 = refs2.concat(refs1.slice(-1));
        refs1.shift();
        refs1.pop();
        temp = refs1;
        refs1 = refs2;
        refs2 = temp;
        console.log(refs1, refs2)
        document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
        document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    } else if (refs1.length == 2 && refs2.length == 0) {
        selected_photo_ref = refs1.slice(-1)
        document.getElementById('selected_photo_ref').value = selected_photo_ref;
        document.getElementById('end').submit();
    } else {
        refs2 = refs2.concat(refs1.slice(-1));
        refs1.shift();
        refs1.pop();
        console.log(refs1, refs2)
        document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
        document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    }
}