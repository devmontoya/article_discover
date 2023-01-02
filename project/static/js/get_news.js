
let news_container = document.getElementById("newscontainer");

function load_news(news_list){
  let news = [];
  for(item in news_list){

    news.push(`<div class="newsItem">
        <div class="div-news-info">
          <h4>${news_list[item]["Title"]}</h4>
          <a href=${news_list[item]["url"]} target="_blank" class="link-news" title="Go to the original source"><img src="static/images/file-link.png"></img></a>
          <h6>${news_list[item]["published"]}</h6>
        </div>
        <div class="text-container">
        </div>
      </div>`);

  }
  let output = news.join("");
  news_container.innerHTML = output;
}

async function get_news_list(website_id){
  const data = await fetch(`api/get_news_list/${website_id}`)
    .then((response) => response.json());
  load_news(data);
}

let website_id= localStorage.getItem('option_chosen');

let news_list = get_news_list(website_id);

load_news(news_list);
