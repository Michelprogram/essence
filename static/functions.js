function html_popup(adresse,ville,gasoil){

  let chaine = "<div class='popup'><h3>Info station</h3>-Adresse :  "+adresse+" <br>-Ville : "+ville+" <h3>Gasoils</h3><ul>"

  for (var [key,value] of Object.entries(Object(gasoil))) {

      chaine += "<li>"+key+" : "+value+" €"
  }

  chaine += "</ul></div>"
  return chaine
}

function color(liste){
  let vert = 24
  let rouge = 194
  let color_list = []
  let median = ((liste.length %2) == 0) ?  liste.length /2 : ((liste.length)+1)/2

  let facteur = Math.ceil(170/liste.length)

  liste.forEach((item, i) => {
    if ( i <= (median -1)){
      vert += facteur
      color_list.push(rgbToHex(vert,194,23))
    }else{
      rouge -= facteur
      color_list.push(rgbToHex(194,rouge,23))
    }
  })

  return color_list
}


function rgbToHex(r, g, b) {
return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

export {html_popup,color,rgbToHex}
