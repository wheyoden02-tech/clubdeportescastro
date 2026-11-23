// COMPLEMENTOS DE LA PLANTILLA (opcional)
// La lista de jugadores se actualiza sola desde la ficha oficial de la LNB (public/datos/liga.js).
// La liga solo entrega el número y el nombre abreviado ("ALVAREZ, N."). Este archivo agrega:
//   - entrenador: la liga no lo publica en la ficha.
//   - nombres: nombre completo con tildes y posición, usando el identificador del jugador en la
//     LNB (el "id" que aparece en liga.js). Un jugador sin entrada aquí se muestra como "N. Alvarez".
// Las entradas de jugadores que ya no están en el club no molestan: simplemente no se usan.
// Posiciones: Base, Escolta, Alero, Ala-pívot, Pívot.

window.PLANTILLA = {
  entrenador: "Ángel Labrín Barría",
  nombres: {
    "418": { nombre: "Marco Ugalde Gazzo", posicion: "Base" },
    "185": { nombre: "Emilio Maldonado Cadín", posicion: "Base" },
    "327": { nombre: "José Ignacio Sepúlveda Ulloa", posicion: "Base" },
    "44": { nombre: "Gabriel Beltrán Peña", posicion: "Ala-pívot" },
    "293": { nombre: "Ignacio Cáceres Cerda", posicion: "Ala-pívot" },
    "358": { nombre: "Pablo Niklitschek Sarrat", posicion: "Escolta" },
    "628": { nombre: "Augusto Barbieri", posicion: "Ala-pívot" },
    "416": { nombre: "Nicolás Álvarez Valenzuela", posicion: "Escolta" },
    "629": { nombre: "Gianfranco Grafals" },
    "19": { nombre: "Diego Barría Roa", posicion: "Base" },
    "479": { nombre: "Halen Aragón Rodríguez", posicion: "Ala-pívot" },
    "292": { nombre: "Ricardo Armijo Lagos", posicion: "Alero" },
    "196": { nombre: "Kevin Ortega Constanzo", posicion: "Base" },
    "676": { nombre: "Nick Farrar", posicion: "Pívot" },
    "689": { nombre: "Marcell McCreary", posicion: "Escolta" },
  },
};
