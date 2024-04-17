document.addEventListener('DOMContentLoaded', function () {
     
    // Load default content on page load
    loadContent('main');

//-------------------------------------------------------------------------------------------------------------------
   //user button attribute start here
/** 
  // Get the user maps link
const userMapsLink = document.getElementById("user");

// Get the content area
const contentArea = document.getElementById("content");

// Add click event listener to the user maps link
userMapsLink.addEventListener("click", function(event) {
    // Prevent the default behavior of the link
    event.preventDefault();

    // Fetch the content to be displayed
    fetch("./components/user.html")
        .then(response => response.text())
        .then(data => {
            // Replace the content area with the fetched content
            contentArea.innerHTML = data;
        })
        .catch(error => console.error("Error fetching content:", error));


       


    });
*/
   
//user button attribute end here

//-------------------------------------------------------------------------------------------------------------------   


document.getElementById('about').addEventListener('click', function (event) {
    event.preventDefault();
    loadContent('about');
});



    document.getElementById('alert').addEventListener('click', function (event) {
        event.preventDefault();
        loadContent('alert');
    });
});

  
// Function to load content dynamically

function loadContent(page) {
    fetch('components/' + page + '.html')  // Adjust the path here
        .then(response => response.text())
        .then(data => document.getElementById('content').innerHTML = data)
        .catch(error => console.log('Error fetching content: ', error));
}


/**function loadContent(page) {
    fetch('components/js' + page + '.js')  // Adjust the path here
        .then(response => response.text())
        .then(data => document.getElementById('content').innerHTML = data)
        .catch(error => console.log('Error fetching content: ', error));
}*/