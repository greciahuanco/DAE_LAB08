const imageBaseUrl = 'https://image.tmdb.org/t/p/w500'

export function adaptMovie(movie) {
  return {
    id: movie.id,
    title: movie.title,
    image: `${imageBaseUrl}${movie.poster_path}`,
    synopsis: movie.overview,
    classification: movie.age_rating,
    rating: movie.vote_average,
    showtimes: [...movie.screenings],
  }
}
