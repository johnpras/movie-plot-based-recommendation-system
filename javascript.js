var test = {};
var k =0;

function startnow_button(){  
    var mydiv = document.getElementsByClassName("front_text_content");
    mydiv.item(0).style.display = "none";
    mydiv.item(1).style.visibility = "visible";
}  

function getmovieinfo(movieTitle) {
    return fetch(`https://www.omdbapi.com/?t=${movieTitle}&apikey=3861f60e`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        return data;
      });
}

class Movie {
    constructor(data){
      Object.assign(this, data);
    }
      
    renderMovie() {
    return ` 
    <div class="printcycle" style="overflow:hidden; align-items: center;" >
    <div class="image-container" style=" display: inline-block;">
            <img width="150" height="200" src='${this.Poster}'/>
    </div>
    <div class="movie-content-container" style=" display: inline-block; height: 200px; width: 600px; overflow: auto;">
        <div class="title">
        <h4>${this.Title}</h4>
        </div>
        <div class="movie-desc" style="text-align: left;">
        <p>${this.Plot}</p>
        </div>
    </div>
    </div>

    <div class="buttondivclass" style="display: inline-block";>
    <button class="button" style="border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 20px;
    margin: 4px 2px;
    cursor: pointer;
    background-color: rgba(231,76,60,1);
    font-weight:bold" onclick="printcyclereccomendations()">Get another recommendation!</button>
    <button class="button" style="border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 20px;
    margin: 4px 2px;
    cursor: pointer;
    background-color: rgba(231,76,60,1);
    font-weight:bold" onclick="window.location.reload(true)">Start over</button>
    </div>
    </div>
    
    <br><br>
    `;
    }
}

function senddata(){
	var text = document.getElementById('input_text_area').value;
    var mydiv = document.getElementsByClassName("front_text_content");

	if (!text) {
        alert("Please enter some text to continue.");
		return false;
	}

    var jsonData = JSON.stringify({
		"text" : text
	});

    fetch('http://127.0.0.1:8000/run-script1/', {
        method: 'POST',
        body: jsonData,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        //console.log(data);
    })
    .catch(error => console.error(error));


    mydiv.item(1).style.display = "none";
    mydiv.item(2).style.visibility = "visible";

    fetch("http://127.0.0.1:8000/run-script2")
    .then(response => response.text())
    .then(data => {
        // The data variable now contains the response data
        //alert(data)
        console.log(data);
        mydiv.item(2).style.display = "none";
        var botc = document.getElementsByClassName("bottom_text_content");
        botc.item(0).style.display = "none";

        const items = JSON.parse(data);
        const dataArray = items[0].split(", ");

        for(let i=0;i<dataArray.length;i++){
            dataArray[i] = dataArray[i].replace(/^"|"$/g, "").replace(/^\\"|\\"$/g, "");
        }

        test.a = dataArray;
        getmovieinfo(dataArray[k]).then((res) => {
            mydiv.item(3).innerHTML += new Movie(res).renderMovie();
        });

        mydiv.item(3).style.visibility = "visible";

    })
    .catch(error => 
        alert("An error occured. Please reload the page."));
}

function printcyclereccomendations(){   
    var mydiv = document.getElementsByClassName("printcycle").item(0);
    var dataArrayl = test.a;
    k = (k+1)%(dataArrayl.length);

    getmovieinfo(dataArrayl[k]).then((res) => {
        mydiv.innerHTML = new Movie(res).renderMovie();
        document.getElementsByClassName("buttondivclass").item(1).style.display = "none";
    });

}