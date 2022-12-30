 
var websites_list = document.getElementById("websitescontainer");

input = [ {"name":"The Guardian", "image_url":"https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png", "url": "https://www.theguardian.com"},
          {"name":"CNET", "image_url":"https://gcp-assets-origin-fly.cnet.com/bundles/cnetcss/images/core/logo/cnet_og.png", "url": "https://www.cnet.com/"},
          {"name":"Wired", "image_url":"https://www.wired.com/wp-content/uploads/2018/06/favicon.png", "url":"https://www.wired.com/"},
          {"name":"BBC News", "image_url":"https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif", "url": "https://www.bbc.co.uk/news/"},
          {"name":"The New York Times", "image_url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png", "url":"https://www.nytimes.com/"}]

function load_pages(){
  localStorage.clear();
  //let data = sessionStorage.getItem("key");
  var channels = [];
  for(chan in input){
    channels.push(`<div class="websiteItem"><button class="button-items" onclick="optionFunc(${chan})">
      <img src=${input[chan]["image_url"]} class="web-icon" alt="Website Icon"><h3>${input[chan]["name"]}</h3></button>
      <a href=${input[chan]["url"]} target="_blank" class="link-page""><img src="static/images/file-link.png"></img></a></div>`);
  }
  let output = channels.join("");
  websites_list.innerHTML = output;
}

function optionFunc(a){
  console.log(`Option chosen ${a}`);
  localStorage.setItem('option_chosen', a);
  window.location.href = "news_view.html";
}

load_pages();

