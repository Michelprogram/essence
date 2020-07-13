import {html_popup,color,rgbToHex} from "./functions.js"

mapboxgl.accessToken = 'pk.eyJ1IjoibWljaGVsamFyZGluaWVyIiwiYSI6ImNrY2drYXAxZzA0NWQyc28zcXFmbTA3NDgifQ.LiWPoLzDu9cac9idtziWkQ'

let data = null

let request = new XMLHttpRequest()
request.onreadystatechange = () =>{
if(request.readyState == 4 && request.status == 200){
   data = JSON.parse(request.responseText)
   let liste_color = color(data)
   data.forEach((station,index) => {
     let popup = new mapboxgl.Popup({ offset: 25 })
                       .setHTML(html_popup(station.adresse,station.ville,station.gasoil))

     new mapboxgl.Marker({"color":liste_color[index]})
     .setLngLat([station.longitude, station.latitude])
     .setPopup(popup)
     .addTo(map)
   })

  }
}
request.open("GET","http://localhost:5000/data")
request.send()



let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [lattitude,longittude],
    zoom:14
})

let popup_center = new mapboxgl.Popup({ offset: 25 })
                  .setText("Votre position")

let center = new mapboxgl.Marker({"color":"26,194,23"})
            .setLngLat([lattitude, longittude])
            .setPopup(popup_center)
            .addTo(map)
