
var websites_list = document.getElementById("websitescontainer");

demo_input = [{"id":1, "name":"The Guardian", "image_url":"https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png", "url": "https://www.theguardian.com"},
          {"id":2, "name":"CNET", "image_url":"https://gcp-assets-origin-fly.cnet.com/bundles/cnetcss/images/core/logo/cnet_og.png", "url": "https://www.cnet.com/"},
          {"id":3, "name":"Wired", "image_url":"https://www.wired.com/wp-content/uploads/2018/06/favicon.png", "url":"https://www.wired.com/"},
          {"id":4, "name":"BBC News", "image_url":"https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif", "url": "https://www.bbc.co.uk/news/"},
          {"id":5, "name":"The New York Times", "image_url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png", "url":"https://www.nytimes.com/"}]

function load_pages(channels_list){
  localStorage.clear();
  //let data = sessionStorage.getItem("key");
  var channels = [];
  for(chan in channels_list){
    image_url = channels_list[chan]["image_url"];
    if (image_url === null){
      image_url = "static/images/newspaper_image.png"
    }
    channels.push(`<div class="websiteItem"><button class="button-items" onclick="optionFunc(${channels_list[chan]["id"]})" title="Show news from this website">
      <img src=${image_url} class="web-icon" alt="Website Icon"><h3>${channels_list[chan]["name"]}</h3></button>
      <a href=${channels_list[chan]["url"]} target="_blank" class="link-page"" title="Go to the website"><img src="static/images/file-link.png"></img></a></div>`);
  }
  let output = channels.join("");
  websites_list.innerHTML = output;
}

function optionFunc(a){
  console.log(`Option chosen ${a}`);
  localStorage.setItem('option_chosen', a);
  window.location.href = "news_view.html";
}

async function fetch_from_API(){
  const data = await fetch('api/get_websites_list')
    .then((response) => response.json());
  load_pages(data);
}

function fetch_demo(){
  load_pages(demo_input);
}

load_pages(demo_input);
// fetch_from_API();
