# Punto 11 · Árbol de componentes y flujo de datos

```text
App
├── Header
├── Hero
│   ├── MovieSearch
│   ├── Button (Ver resultados)
│   └── Button (Limpiar filtro)
├── PremieresSection
│   ├── PremiereSkeleton (carga)
│   ├── PremieresCarousel (éxito)
│   │   ├── Button (Anterior)
│   │   └── Button (Siguiente)
│   └── Mensaje de error (fallo)
├── MovieList
│   └── MovieCard (una por película visible)
│       └── Button (Agregar a favoritas / Quitar de favoritas)
├── Footer
└── Aviso de favoritas
```

## Dónde vive cada dato

| Componente | Datos que guarda, recibe o calcula |
| --- | --- |
| `App` | Guarda `favoriteMovies`, `favoriteNotice` y `searchText`. Calcula `favoriteCount` con la longitud de la lista. Usa `useDebounce` para obtener el texto con el que se filtra la cartelera. |
| `Header` | Recibe `favoriteCount` y muestra el total. |
| `Hero` y `MovieSearch` | El banner recibe la película destacada y el texto actual. El buscador recibe ese texto como valor y avisa a `App` cuando cambia. El botón Limpiar filtro también llama a una función de `App`. |
| `PremieresSection` | Obtiene el estado, las películas o el mensaje de error con `usePremieres`. Decide qué mostrar según la respuesta. |
| `PremieresCarousel` | Recibe las películas de estreno y guarda el índice de la película visible. |
| `MovieList` | Recibe las películas, las favoritas y el texto con retardo. Filtra las tarjetas y usa el ancho de `useWindowSize` para calcular las columnas. |
| `MovieCard` | Recibe una película y el valor `isFavorite`. Al pulsar su botón, llama a `onToggleFavorite` con la película. |
| `Button`, `PremiereSkeleton` y `Footer` | Presentan controles, el indicador visual de carga o el contenido fijo del pie de página. |

## Por qué el contador se calcula en App

Las tarjetas son las que disparan los cambios y la cabecera muestra el total. Como `App` es el componente padre que ambos comparten, mantuve allí la lista de favoritas. Cada vez que se agrega o se quita una película, `App` actualiza la lista y calcula el total con `favoriteMovies.length`. A la cabecera le pasa solo el número mediante `favoriteCount`.

Si guardara un contador independiente en la cabecera, tendría que mantenerlo sincronizado con la lista que cambia en `App`. Al calcularlo a partir de esa lista, el número siempre corresponde a las favoritas actuales.
