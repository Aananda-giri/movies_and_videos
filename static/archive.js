
form.addEventListener('submit', (e) => {
  window.location.redirect('https://google.com');
  console.log('searching')  
  e.preventDefault();

    const searchTerm = search.value;
    selectedGenre=[];
    setGenre();
    if(searchTerm) {
        getMovies(searchTerm)
    }else{
        // getMovies(API_URL);
    }

})