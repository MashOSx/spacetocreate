var isDivHidden = true;

function btnClick_showDiv() {
    e = document.getElementById("divHiddenText");
    if (isDivHidden === true) {
        console.log('Showing divHiddenText');        
        e.style.display="block";
        isDivHidden = false;
    } else {
        console.log('Hiding divHiddenText.');
        e.style.display="none";
        isDivHidden = true;
    }    
}