// Create a function to filter the table
function filterTable(event) {
    // Get the value of the search input
    var searchValue = event.target.value;
    
    
    // Iterate through the table rows
    var rows = document.querySelectorAll("table tr");
    for (var i = 1; i < rows.length; i++) {
      // Get the text of the current row
      var rowText = rows[i].textContent;
  
      // If the text of the current row contains the search value, show the row
      if (rowText.indexOf(searchValue) >= 0) {
        rows[i].style.display = "";
      } else {
        rows[i].style.display = "none";
      }
    }
    
  }
  
  // Add an event listener to the search input
  document.getElementById("selection").addEventListener("input", filterTable)