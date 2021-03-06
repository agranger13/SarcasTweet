var list_icon = []
var dict_text = {}
if(typeof browser === "undefined"){
  var browser = chrome
}
function display_popup(event){
  if(this.id){
    var tooltip = document.getElementById("tooltip_" + this.id)
  }else{
    var tooltip = document.getElementById(this.parentNode.id)
  }
  console.log(tooltip)
  if(tooltip.style.visibility == "hidden"){
    console.log("to block")
    tooltip.style.visibility = "visible"
  }else{
    console.log("to none")
    tooltip.style.visibility = "hidden"
  }
  console.log(tooltip.style.display)
}

function create_tooltip(id) {
  var tooltipElement = document.createElement("div")
  tooltipElement.id = "tooltip_" + id
  tooltipElement.style.visibility="hidden"
  tooltipElement.className = "tooltipElement"

  var tooltipTitle = document.createElement("p")
  tooltipTitle.id = "tooltip_score_" + id
  tooltipTitle.className = "tooltipTitle"

  var tooltipLegend = document.createElement("p")
  tooltipLegend.innerHTML = "Send feedback"
  tooltipLegend.className = "tooltipLegend"

  var tooltipSurvey = document.createElement("div")
  tooltipSurvey.style.textAlign = "center"

  var tooltipClose = document.createElement("span")
  tooltipClose.className = "close"

  var tooltipDislikeImg = document.createElement("img");
  tooltipDislikeImg.src = browser.extension.getURL("assets/icons/icons-moins.png");
  tooltipDislikeImg.className = "tooltipDislike"
  tooltipDislikeImg.addEventListener("click",function(e) {
        document.getElementById("tooltip_" + id).style.visibility="hidden"
        send_feedback(dict_text[id],0);
        alert("Merci de votre feedback et de contribuer à l'amélioration de Sarcastweet")
      },false)

  var tooltipLikeImg = document.createElement("img");
  tooltipLikeImg.src = browser.extension.getURL("assets/icons/icons-plus.png");
  tooltipLikeImg.className = "tooltipLike"
  tooltipLikeImg.addEventListener("click",function(e) {
    document.getElementById("tooltip_" + id).style.visibility="hidden"
    send_feedback(dict_text[id],1);
    alert("Merci de votre feedback et de contribuer à l'amélioration de Sarcastweet")
  },false)

  tooltipSurvey.appendChild(tooltipDislikeImg)
  tooltipSurvey.appendChild(tooltipLikeImg)

  tooltipElement.appendChild(tooltipClose)
  tooltipElement.appendChild(tooltipTitle)
  tooltipElement.appendChild(tooltipSurvey)
  tooltipElement.appendChild(tooltipLegend)

  return tooltipElement
}

function add_listener(){
  list_score_item = document.querySelectorAll("[id^=SarcasTweet_score_]")
  for (item of list_score_item){
    item.addEventListener("click",display_popup)
    list_icon.push(item.id)
  }

  list_score_item = document.querySelectorAll("[id^=tooltip_SarcasTweet_score_]")
  for (item of list_score_item){
    item.addEventListener("click",function(e) {
        e.preventDefault();
      },false)
  }

  list_score_item = document.querySelectorAll("[id^=tooltip_SarcasTweet_score_]>.close")
  for (item of list_score_item){
    item.addEventListener("click",display_popup,false)
  }
}

function add_icon() {
  var tweets = document.querySelectorAll('[data-testid="tweet"]>div:nth-child(2)>div:nth-child(2)>div:last-child')
  var template = tweets[0].childNodes[0]
  for (tweet of tweets) {
    if (Array.from(tweet.childNodes[0].childNodes).filter(div => div.id && div.id.match(/SarcasTweet_score.*/g)).length == 0){
      console.log("tweet find")
      var div_top = document.createElement("button")
      div_top.className = "css-1dbjc4n r-18u37iz r-1h0z5md SarcasTweet_score"
      my_id = Math.random().toString(36).substr(2, 9)
      div_top.id = "SarcasTweet_score_" + my_id
      // div_top.style.background = "none"
      var div_middle = document.createElement("div")
      div_middle.className = "css-18t94o4 css-1dbjc4n r-1777fci r-bt1l66 r-1ny4l3l r-bztko3 r-lrvibr"

      var div_middle_bot = document.createElement("div")
      div_middle_bot.className = "css-901oao r-1awozwy r-m0bqgq r-6koalj r-1qd0xha r-a023e6 r-16dba41 r-1h0z5md r-rjixqe r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0"
      var percent = document.createElement("p")

      percent.id = "percent_" + div_top.id
      var tweet_text = function (tweet) {
        var text_element = tweet.previousSibling.previousSibling
        result = ""
        for (elem of text_element.childNodes[0].childNodes) {
          if (elem.tagName == "SPAN" && elem.childElementCount == 0) {
            result += elem.innerHTML + " "
          }else if(elem.tagName == "SPAN" && elem.childElementCount == 1){
            result += elem.childNodes[0].innerHTML + " "
          }
        }
        return result
      }
      dict_text[div_top.id]=tweet_text(tweet)

      // percent.innerHTML="89%"
      percent.style.paddingLeft = "0.2em"

      var div_bot = document.createElement("div")
      div_bot.className = "css-1dbjc4n r-xoduu5"

      var div_back_icon = document.createElement("div")
      div_back_icon.className = "css-1dbjc4n r-1niwhzg r-sdzlij r-1p0dtai r-xoduu5 r-1d2f490 r-xf4iuw r-1ny4l3l r-u8s1d r-zchlnj r-ipm5af r-o7ynqc r-6416eg"

      var new_icon = document.createElement("div");
      new_icon.innerHTML = '<svg class="r-4qtqp9 r-yyyyoo r-1xvli5t r-dnmrzs r-bnwqim r-1plcrui r-lrvibr r-1hdv0qi" enable-background="new 0 0 64 64" height="512" viewBox="0 0 64 64" width="512" xmlns="http://www.w3.org/2000/svg"><path d="m34.306 17.72 1.389-1.439c-3.141-3.029-8.248-3.029-11.389 0l1.389 1.439c2.374-2.291 6.236-2.291 8.611 0z"/><path d="m19.694 16.28c-3.141-3.029-8.248-3.029-11.389 0l1.389 1.439c2.375-2.291 6.236-2.291 8.611 0z"/><path d="m61.517 18.144c-.299-.182-.671-.192-.982-.028-6.281 3.306-13.222 4.806-20.109 4.533 1.044-3.199 1.574-6.438 1.574-9.649v-11c0-.351-.184-.675-.483-.856-.3-.181-.674-.19-.982-.028-5.694 2.999-12.103 4.584-18.535 4.584s-12.841-1.585-18.534-4.585c-.308-.163-.683-.153-.983.029s-.483.505-.483.856v11c0 8.008 3.366 16.228 9.736 23.771 4.782 5.663 9.5 8.919 9.699 9.055.17.115.368.174.565.174.196 0 .393-.058.562-.173.052-.036 1.094-.752 2.666-2.07 1.599 3.415 3.774 6.777 6.507 10.013 4.782 5.663 9.5 8.919 9.699 9.055.171.116.369.175.566.175s.395-.059.564-.175c.199-.136 4.917-3.392 9.699-9.055 6.371-7.542 9.737-15.762 9.737-23.77v-11c0-.351-.184-.675-.483-.856zm-39.515 25.622c-3.107-2.325-18.002-14.328-18.002-30.766v-9.38c5.603 2.674 11.791 4.08 18 4.08s12.397-1.406 18-4.08v9.38c0 3.16-.557 6.355-1.643 9.511-5.133-.472-10.197-1.925-14.891-4.396-.312-.164-.684-.153-.982.028-.3.182-.484.506-.484.857v11c0 .331.015.664.026.995-2.019.017-3.938-.599-5.319-1.703-.39-.39-1.018-.386-1.409.005-.193.193-.29.448-.291.703 0 .144.03.287.091.42.224.541 2.44 5.58 6.902 5.58.202 0 .407-.024.612-.046.4 1.967.998 3.933 1.784 5.886-1.03.883-1.878 1.543-2.394 1.926zm.154-10.775c.034.326.081.653.126.98-1.335.086-2.512-.547-3.37-1.391 1.033.292 2.128.43 3.244.411zm37.844-2.991c0 16.415-14.889 28.433-18 30.764-3.114-2.329-18-14.329-18-30.764v-9.38c11.385 5.436 24.615 5.436 36 0z"/><path d="m54.306 34.72 1.389-1.439c-3.141-3.029-8.248-3.029-11.389 0l1.389 1.439c2.374-2.291 6.236-2.291 8.611 0z"/><path d="m39.694 33.28c-3.141-3.029-8.248-3.029-11.389 0l1.389 1.439c2.375-2.291 6.236-2.291 8.611 0z"/><path d="m47.373 46.221c-2.963 2.383-7.783 2.383-10.746 0-.354-.283-.857-.293-1.222-.024-.365.271-.503.753-.334 1.175.092.23 2.305 5.628 6.929 5.628s6.837-5.398 6.929-5.629c.169-.422.031-.904-.334-1.175-.365-.269-.867-.259-1.222.025zm-5.373 4.779c-1.261 0-2.301-.645-3.104-1.439 2.011.563 4.214.563 6.221-.004-.804.797-1.847 1.443-3.117 1.443z"/></svg>'


      var tooltipElement = create_tooltip(div_top.id)
      console.log("add element : ")

      div_bot.appendChild(new_icon)
      div_bot.appendChild(div_back_icon)

      div_middle_bot.appendChild(div_bot)
      div_middle_bot.appendChild(percent)

      div_middle.appendChild(div_middle_bot)

      div_top.appendChild(div_middle)
      tweet.childNodes[0].appendChild(div_top)
      tweet.childNodes[0].appendChild(tooltipElement)

      evaluate_sarcasm(div_top.id)
    }
  }
  add_listener()
}

function evaluate_sarcasm(id){
  var tootltipID = "tooltip_score_" + id
  var iconID = "percent_" + id
  console.log(iconID)
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "POST", "https://ec2-18-117-242-83.us-east-2.compute.amazonaws.com:5000/evaluate_sarcasm", true ); // false for synchronous request
  xmlHttp.setRequestHeader('Content-Type', 'application/json');

  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState === 4 && xmlHttp.status == 200) {
      console.log(xmlHttp.response); // Par défault une DOMString
      var tweet_score = document.getElementById(iconID)
      var tootltip_score = document.getElementById(tootltipID)

      var responseJSON = JSON.parse(xmlHttp.response)
      var percent = Math.round(parseFloat(responseJSON.label))
      tootltip_score.innerHTML="Sarcasm Rate <br><b>"+percent+"%</b>"
      tweet_score.innerHTML=percent+"% sarcastic"
      if(percent>60){
        tweet_score.parentElement.className=tweet_score.parentElement.className + " isSarcasm"
      }else if (40<=percent && percent<=60){
        tweet_score.parentElement.className=tweet_score.parentElement.className + " isNeutral"
      }else{
        tweet_score.parentElement.className=tweet_score.parentElement.className + " isNotSarcasm"
      }
    }else {
      console.log(xmlHttp.status);
    }
  }

  xmlHttp.send( JSON.stringify({ Tweet : dict_text[id] }) );
}

function send_feedback(text, label){
  console.log(text + " => " + label)
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "POST", "https://ec2-18-117-242-83.us-east-2.compute.amazonaws.com:5000/send_feedback", true ); // false for synchronous request
  xmlHttp.setRequestHeader('Content-Type', 'application/json');

  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState === 4 && xmlHttp.status == 200) {
      console.log(xmlHttp.response);
    }else {
      console.log(xmlHttp.status);
    }
  }

  xmlHttp.send( JSON.stringify({ Tweet : text, label: label }) );
}
setInterval(add_icon,2000)