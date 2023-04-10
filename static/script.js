// // search movies:
// getMovies(searchURL+'&query='+searchTerm)

// // get movies
// getMovies(API_URL + '&with_genres='+encodeURI(selectedGenre.join(',')))
// getMovies(API_URL);

// // when someone click span element
// BASE_URL + '/movie/'+id+'/videos?'+API_KEY
console.log('hi from script.js');

const BASE_URL = window.location.origin   //'https://api.themoviedb.org/3';
// const BASE_URL = 'netlify_url'
const API_URL = BASE_URL + '/discover/movie?sort_by=popularity.desc&'+API_KEY;
const IMG_URL = 'https://image.tmdb.org/t/p/w500';
const searchURL = 'http://127.0.0.1:8000/search/';
// const searchURL = BASE_URL + '/search/movie?'+API_KEY;

const genres = [
    {
      "id": 28,
      "name": "Action"
    },
    {
      "id": 12,
      "name": "Adventure"
    },
    {
      "id": 16,
      "name": "Animation"
    },
    {
      "id": 35,
      "name": "Comedy"
    },
    {
      "id": 80,
      "name": "Crime"
    },
    {
      "id": 99,
      "name": "Documentary"
    },
    {
      "id": 18,
      "name": "Drama"
    },
    {
      "id": 10751,
      "name": "Family"
    },
    {
      "id": 14,
      "name": "Fantasy"
    },
    {
      "id": 36,
      "name": "History"
    },
    {
      "id": 27,
      "name": "Horror"
    },
    {
      "id": 10402,
      "name": "Music"
    },
    {
      "id": 9648,
      "name": "Mystery"
    },
    {
      "id": 10749,
      "name": "Romance"
    },
    {
      "id": 878,
      "name": "Science Fiction"
    },
    {
      "id": 10770,
      "name": "TV Movie"
    },
    {
      "id": 53,
      "name": "Thriller"
    },
    {
      "id": 10752,
      "name": "War"
    },
    {
      "id": 37,
      "name": "Western"
    }
  ]

const main = document.getElementById('main');
const form =  document.getElementById('form');
const search = document.getElementById('search');
const tagsEl = document.getElementById('tags');

const prev = document.getElementById('prev')
const next = document.getElementById('next')
const current = document.getElementById('current')

var currentPage = 1;
var nextPage = 2;
var prevPage = 3;
var lastUrl = '';
var totalPages = 100;

var selectedGenre = []
console.log('setGenere not invoked');

function setGenre() {
  console.log('setGenere invoked');
  tagsEl.innerHTML= '';
  genres.forEach(genre => {
      const t = document.createElement('div');
      t.classList.add('tag');
      t.id=genre.id;
      t.innerText = genre.name;
      t.addEventListener('click', () => {
          if(selectedGenre.length == 0){
              selectedGenre.push(genre.id);
          }else{
              if(selectedGenre.includes(genre.id)){
                  selectedGenre.forEach((id, idx) => {
                      if(id == genre.id){
                          selectedGenre.splice(idx, 1);
                      }
                  })
              }else{
                  selectedGenre.push(genre.id);
              }
          }
          console.log(selectedGenre)
          getMovies(API_URL + '&with_genres='+encodeURI(selectedGenre.join(',')))
          highlightSelection()
      })
      tagsEl.append(t);
  })
}


setGenre();
function highlightSelection() {
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        tag.classList.remove('highlight')
    })
    clearBtn()
    if(selectedGenre.length !=0){   
        selectedGenre.forEach(id => {
            const hightlightedTag = document.getElementById(id);
            hightlightedTag.classList.add('highlight');
        })
    }

}

function clearBtn(){
    let clearBtn = document.getElementById('clear');
    if(clearBtn){
        clearBtn.classList.add('highlight')
    }else{
            
        let clear = document.createElement('div');
        clear.classList.add('tag','highlight');
        clear.id = 'clear';
        clear.innerText = 'Clear x';
        clear.addEventListener('click', () => {
            selectedGenre = [];
            setGenre();            
            getMovies(API_URL);
        })
        tagsEl.append(clear);
    }
    
}


/* Open when someone clicks on the span element */
function showTrailer(what, tmdb_id, original_title) {
  const overlayContent = document.getElementById('overlay-content');
  console.log(`\nknow-more tmdb_id: \'${tmdb_id}\'\n`);
  // let id = movie.id;
  // http://127.0.0.1:8000/trailer/?tmdb_id=550
  console.log(window.location.origin + '/trailer?tmdb_id=' + tmdb_id + '&what=' + what);
  fetch(window.location.origin + '/trailer?tmdb_id=' + tmdb_id).then(res => res.json()).then(videoData => {
    console.log(videoData);
    if(videoData){
      document.getElementById("myNav").style.width = "100%";
      if(videoData.results.length > 0){
        var embed = [];
        var dots = [];
        videoData.results.forEach((video, idx) => {
          let {name, key, site} = video
            console.log('name, key, site : ',name, key, site);
          if(site == 'YouTube'){
            const trailer_url = `https://www.youtube.com/embed/${key}`;
            console.log(`trailer_URL: ${trailer_url}`);
            embed.push(`
              <iframe width="560" height="315" src="${trailer_url}" title="${name}" class="embed hide" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          
          `)

            dots.push(`
              <span class="dot">${idx + 1}</span>
            `)
          }
        })
        
        var content = `
        <h1 class="no-results">${original_title}</h1>
        <br/>
        
        ${embed.join('')}
        <br/>

        <div class="dots">${dots.join('')}</div>
        
        `
        overlayContent.innerHTML = content;
        activeSlide=0;
        showVideos();
      }else{
        overlayContent.innerHTML = `<h1 class="no-results">No Results Found</h1>`
      }
    }
  })
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
  let floating_nav = document.getElementById("myNav").style.width = "0%"; // minimizing overlay conetnt
  document.getElementById('overlay-content').innerHTML='';  // deleting content of overlay
}

var activeSlide = 0;
var totalVideos = 0;

// Show the trailer video
function showVideos(){
  let embedClasses = document.querySelectorAll('.embed');
  let dots = document.querySelectorAll('.dot');

  totalVideos = embedClasses.length; 
  embedClasses.forEach((embedTag, idx) => {
    if(activeSlide == idx){
      embedTag.classList.add('show')
      embedTag.classList.remove('hide')

    }else{
      embedTag.classList.add('hide');
      embedTag.classList.remove('show')
    }
  })

  dots.forEach((dot, indx) => {
    if(activeSlide == indx){
      dot.classList.add('active');
    }else{
      dot.classList.remove('active')
    }
  })
}

const leftArrow = document.getElementById('left-arrow')
const rightArrow = document.getElementById('right-arrow')

leftArrow.addEventListener('click', () => {
  if(activeSlide > 0){
    activeSlide--;
  }else{
    activeSlide = totalVideos -1;
  }

  showVideos()
})

rightArrow.addEventListener('click', () => {
  if(activeSlide < (totalVideos -1)){
    activeSlide++;
  }else{
    activeSlide = 0;
  }
  showVideos()
})


function getColor(vote) {
  console.log('get_color')  
  if(vote>= 8){
        return 'green'
    }else if(vote >= 5){
        return "orange"
    }else{
        return 'red'
    }
}


prev.addEventListener('click', () => {
  if(prevPage > 0){
    pageCall(prevPage);
  }
})

next.addEventListener('click', () => {
  if(nextPage <= totalPages){
    pageCall(nextPage);
  }
})

function pageCall(page){
  let urlSplit = lastUrl.split('?');
  let queryParams = urlSplit[1].split('&');
  let key = queryParams[queryParams.length -1].split('=');
  if(key[0] != 'page'){
    let url = lastUrl + '&page='+page
    getMovies(url);
  }else{
    key[1] = page.toString();
    let a = key.join('=');
    queryParams[queryParams.length -1] = a;
    let b = queryParams.join('&');
    let url = urlSplit[0] +'?'+ b
    getMovies(url);
  }
}

// for series episodes
function colorCurrentEpisode(episode_id){
  let current_episode = document.getElementById('episode_'+episode_id);
  current_episode.className = "nav-link btn btn-sm btn-dark active"
}

// redirect to movie url
function redirectMovie(tmdb_id){
  window.location.href = BASE_URL + '/movie?tmdb_id=' + tmdb_id;
}

function redirectSeries(tmdb_id){
  window.location.href = BASE_URL + '/series?tmdb_id=' + tmdb_id + '&season=1&episode=1';
}

function changeSource(source){
  window.location.href = window.location.href + '&source=' + source;
}

