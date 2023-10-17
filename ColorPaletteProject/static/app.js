const form = document.querySelector('#form');
form.addEventListener("submit",function(e){
    // prevent the default behaviour of the form
    e.preventDefault();
    // get the query from the input
    const query = form.elements.query.value;
    // call the API
    fetch("palette",{
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams( {
            query: query
        })
    })
    // convert the response to JSON
    .then(res => res.json())
    // use the data to create the color boxes
    .then(data => {
        const colors = data.colors;
        const container = document.querySelector('.container');
        // clear the container
        container.innerHTML = "";
        for(const color of colors){
            // create a div with the color for the background
            const div = document.createElement('div');
            div.classList.add('color');
            div.style.backgroundColor = color;
            div.style.width = `calc(100% / ${colors.length})`;

            // add a click event to copy the color to the clipboard
            div.addEventListener("click",function(){
                navigator.clipboard.writeText(color);
            })
            const span = document.createElement('span');
            span.innerText = color;
            div.appendChild(span);
            container.appendChild(div);
        }
    })

})