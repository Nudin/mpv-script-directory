
function Search() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  table = document.getElementById("main");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

var main = (function () {

  const getCellValue = (tr, idx) => tr.children[idx].dataset["sortvalue"] || tr.children[idx].innerText || tr.children[idx].textContent;

  const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v2 - v1 : v1.toString().localeCompare(v2)
  )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

  var load = function () {
    return new Promise(function (resolve, reject) {
      var xhttp = new XMLHttpRequest()
      xhttp.open('GET', './mpv_script_directory.json', true)
      xhttp.onload = function () {
        if (xhttp.status === 200) {
          var rows = JSON.parse(xhttp.response)
          addrows(rows)
          resolve()
        } else {
          reject(Error(xhttp.response))
        }
      }
      xhttp.send()
    })
  }

  var addrows = function(rows) {
    var tbody = document.getElementById("tbody")
    var t = document.querySelector('#scriptrow'),
    link = t.content.querySelector(".name");
    stars = t.content.querySelector(".stars");
    desc = t.content.querySelector(".desc");
    for (var id in rows) {
      row = rows[id]
      link.href = row.url
      link.innerText = row.name
      stars.innerText = row.stars || ""
      if (row.sharedrepo && row.stars) {
        stars.innerText += '*'
      }
      stars.dataset["sortvalue"] = row.stars || 0
      desc.innerText = row.desc
      tbody.appendChild(document.importNode(t.content, true))
    }
  }

  var init = function () {
    load()
    // sortable table, based on https://stackoverflow.com/a/19947532
    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
      console.log(th);
      const table = th.closest('table').querySelector("tbody");
      Array.from(table.querySelectorAll('tr:nth-child(n+1)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr) );
    })));

  }

  return {
    init: init,
  }
})()

document.addEventListener('DOMContentLoaded', function () {
  main.init()
})
