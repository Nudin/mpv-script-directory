
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
      xhttp.open('GET', 'https://raw.githubusercontent.com/Nudin/mpv-script-directory/master/mpv_script_directory.json', true)
      xhttp.onload = function () {
        if (xhttp.status === 200) {
          var rows = JSON.parse(xhttp.response)
          addrows(rows)
          updatefilters()
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
    tr = t.content.querySelector("tr");
    link = t.content.querySelector(".name");
    scriptid = t.content.querySelector(".scriptid");
    stars = t.content.querySelector(".stars");
    desc = t.content.querySelector(".desc");
    for (var id in rows) {
      row = rows[id]
      if ( !("os" in row) || row.os.length == 0) {
        tr.classList = ["Portable"]
      }
      else {
        tr.className = ""
        tr.classList.add(...row.os)
      }
      var type = row.type.split(' ')[0]
      if ( type === "user" ) { type = "shader" ; }
      tr.classList.add(type)
      scriptid.innerText = id
      scriptid.title = "ScriptID"
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

  var updatefilters = function (filter) {
    zebracount = 0
    document.querySelectorAll("tbody tr").forEach(tr => {
      var cl = Array.from(tr.classList)
      tr.style.display = "none"
      tr.style.backgroundColor = null
      var hide = true
      document.querySelectorAll('.osfilter:checked').forEach(function(filter) {
        if (cl.includes(filter.id)) {
          hide = false
        }
      } )
      if (hide) {
        return
      }
      var hide = true
      document.querySelectorAll('.typefilter:checked').forEach(function(filter) {
        if (cl.includes(filter.id)) {
          hide = false
        }
      } )
      if (!hide) {
        tr.style.display = "";
        if (zebracount % 2 == 0) {
          tr.style.backgroundColor = "#eee"
        }
        zebracount++;
      }
    })
  }

  var init = function () {
    load()
    // sortable table, based on https://stackoverflow.com/a/19947532
    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
      const table = th.closest('table').querySelector("tbody");
      Array.from(table.querySelectorAll('tr:nth-child(n+1)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr) );
    })));

    document.querySelectorAll('.filter').forEach(filter => filter.onclick = updatefilters)
  }

  return {
    init: init,
  }
})()

document.addEventListener('DOMContentLoaded', function () {
  main.init()
})
