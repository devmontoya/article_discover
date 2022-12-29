 
var websites_list = document.getElementById("websitescontainer");

input = [ {"name":"The Guardian", "image_url":"https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png", "url": "https://www.theguardian.com"},
          {"name":"CNET", "image_url":"https://gcp-assets-origin-fly.cnet.com/bundles/cnetcss/images/core/logo/cnet_og.png", "url": "https://www.cnet.com/"},
          {"name":"Wired", "image_url":"https://www.wired.com/wp-content/uploads/2018/06/favicon.png", "url":"https://www.wired.com/"},
          {"name":"BBC News", "image_url":"https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif", "url": "https://www.bbc.co.uk/news/"},
          {"name":"The New York Times", "image_url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png", "url":"https://www.nytimes.com/"}]

function load_pages(){
  var channels = [];
  for(chan in input){
    channels.push(`<div class="websiteItem"><a href=${input[chan]["url"]} id="link-api" target="_blank" rel="nofollow">
      <img src=${input[chan]["image_url"]} alt="Website Icon"><h3>${input[chan]["name"]}</h3></a>
      <a href=${input[chan]["url"]} target="_blank" id="link-page""><img src="./images/file-link.png"></img></a></div>`);
  }
  let output = channels.join("");
  websites_list.innerHTML = output;
  console.log(input);
}

load_pages();

