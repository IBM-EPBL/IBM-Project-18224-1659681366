function pdf(){
    const element = document.getElementById("resume");
    html2pdf().from(element).save();    
}

/*<script src="https://raw.githack.com/eKoopmans/html2pdf/master/dist/html2pdf.bundle.js"></script> */