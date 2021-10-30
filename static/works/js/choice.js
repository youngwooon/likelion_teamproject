let refs2 = [];
let temp = [];
let recovery = [];

function select1() {
    if (refs1.length == 2 && refs2.length != 0) {
        refs2 = refs2.concat(refs1.slice(0, 1));
        to_recovery();
        exchange();
        input_images();
    } else if (refs1.length == 2 && refs2.length == 0) {
        selected_photo_ref = refs1.slice(0, 1)
        document.getElementById('selected_photo_ref').value = selected_photo_ref;
        document.getElementById('end').submit();
    } else {
        refs2 = refs2.concat(refs1.slice(0, 1));
        to_recovery();
        input_images();
    }
}

function select2() { 
    if (refs1.length == 2 && refs2.length != 0) {
        refs2 = refs2.concat(refs1.slice(-1));
        to_recovery();
        exchange();
        input_images();
    } else if (refs1.length == 2 && refs2.length == 0) {
        selected_photo_ref = refs1.slice(-1)
        document.getElementById('selected_photo_ref').value = selected_photo_ref;
        document.getElementById('end').submit();
    } else {
        refs2 = refs2.concat(refs1.slice(-1));
        to_recovery();
        input_images();
    }
}

function cancel() {
    if (refs2.length == 0) {
        exchange();
        from_recovery();
        refs2.pop();
        input_images();
    } else {
        from_recovery();
        refs2.pop();
        input_images();
    }
}

function exchange () {
    temp = refs1;
    refs1 = refs2;
    refs2 = temp;
}

function input_images () {
    document.getElementById('img1').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(0,1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
    document.getElementById('img2').src = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + refs1.slice(-1) + '&maxwidth=600&key=AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8';
}

function to_recovery () {
    recovery.unshift(refs1.slice(0,1));
    recovery = recovery.concat(refs1.slice(-1));
    refs1.shift();
    refs1.pop();
}

function from_recovery () {
    refs1.unshift(recovery.slice(0,1));
    refs1 = refs1.concat(recovery.slice(-1));
    recovery.shift();
    recovery.pop();
}