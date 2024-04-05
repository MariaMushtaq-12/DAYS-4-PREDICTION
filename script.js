// Function to load content dynamically

function loadContent(page) {
    fetch('components/' + page + '.html')  // Adjust the path here
        .then(response => response.text())
        .then(data => document.getElementById('content').innerHTML = data)
        .catch(error => console.log('Error fetching content: ', error));
}


document.addEventListener('DOMContentLoaded', function () {
      // Load default content on page load
     // loadContent('prediction');

      // Event listeners for navbar links
    /*  document.getElementById('main').addEventListener('click', function (event) {
          event.preventDefault();
          loadContent('main');
      });
*/
    // Load default content on page load
    loadContent('main');


    /*document.getElementById('main').addEventListener('click', function (event) {
        event.preventDefault();
        loadContent('main');
    });*/
    // Event listeners for navbar links
    
    // document.getElementById('Maps').addEventListener('click', function (event) {
    //     event.preventDefault();
    //     loadContent('maps');
    // });



    document.getElementById('user').addEventListener('click', function (event) {
        event.preventDefault();
        loadContent('user');
    });
    



   

    document.getElementById('alert').addEventListener('click', function (event) {
        event.preventDefault();
        loadContent('alert');
    });
});

document.getElementById('about').addEventListener('click', function (event) {
    event.preventDefault();
    loadContent('about');
});

/*function loadContent(page) {
    fetch('components/' + page + '.css')  // Adjust the path here
        .then(response => response.text())
        .then(data => document.getElementById('content').innerHTML = data)
        .catch(error => console.log('Error fetching content: ', error));
}
*/


