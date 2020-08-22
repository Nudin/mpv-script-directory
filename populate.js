var main = (function () {
  const getCellValue = (tr, idx) => tr.children[idx].dataset['sortvalue'] || tr.children[idx].innerText || tr.children[idx].textContent

  const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v2 - v1 : v1.toString().localeCompare(v2)
  )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx))

  // load and parse the mpv script directory and update the table
  var load = function () {
    return new Promise(function (resolve, reject) {
      var xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
      xhttp.open('GET', 'https://raw.githubusercontent.com/Nudin/mpv-script-directory/master/mpv_script_directory.json', true)
      xhttp.onload = function () {
        if (xhttp.status === 200) {
          var rows = JSON.parse(xhttp.response)
          addrows(rows)
          updatefilters()
          search()
          resolve()
        } else {
          reject(Error(xhttp.response))
        }
      }
      xhttp.send()
    })
  }

  var shortenType = {
    'javascript': 'javascript', // eslint-disable-line quote-props
    'lua script': 'lua',
    'user shader': 'shader',
    'C plugin': 'C',
    'other': 'other', // eslint-disable-line quote-props
    'vapoursynth script': 'other'
  }

  // Add a table row for each script
  var addrows = function (scripts) {
    var tbody = document.getElementById('tbody')
    var t = document.querySelector('#scriptrow')
    var tr = t.content.querySelector('tr')
    var link = t.content.querySelector('.name')
    var scriptid = t.content.querySelector('.scriptid')
    var stars = t.content.querySelector('.stars')
    var desc = t.content.querySelector('.desc')
    for (var id in scripts) {
      var script = scripts[id]
      scriptid.innerText = id
      link.innerText = script.name
      desc.innerText = script.desc
      link.href = script.url
      stars.innerText = script.stars || ''
      if (!('os' in script) || script.os.length === 0) {
        tr.classList = ['Portable']
      } else {
        tr.className = ''
        tr.classList.add(...script.os)
      }
      tr.classList.add(shortenType[script.type])
      if (script.sharedrepo && script.stars) {
        stars.innerText += '*'
      }
      stars.dataset['sortvalue'] = script.stars || 0
      tbody.appendChild(document.importNode(t.content, true))
    }
    updatefilters()
  }

  // Limit the shown rows to those matching the search term
  var search = function () {
    var filter = document.getElementById('search').value.toUpperCase()
    var trList = document.querySelectorAll('#main tbody tr')

    // Loop through all table rows, and hide those who don't match the search query
    trList.forEach(tr => {
      var txtValue =
        tr.querySelector('.scriptid').textContent +
        '\n' +
        tr.querySelector('.desc').textContent
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr.classList.remove('hidden-by-search')
      } else {
        tr.classList.add('hidden-by-search')
      }
    })
    updateZebra()
  }

  // Limit the shown rows to those matching the filters
  var updatefilters = function (filter) {
    document.querySelectorAll('tbody tr').forEach(tr => {
      var cl = Array.from(tr.classList)

      tr.classList.add('hidden-by-os-filter')
      document.querySelectorAll('.osfilter:checked').forEach(function (filter) {
        if (cl.includes(filter.id)) {
          tr.classList.remove('hidden-by-os-filter')
        }
      })

      tr.classList.add('hidden-by-type-filter')
      document.querySelectorAll('.typefilter:checked').forEach(function (filter) {
        if (cl.includes(filter.id)) {
          tr.classList.remove('hidden-by-type-filter')
        }
      })
    })
    updateZebra()
  }

  // Update zebra
  var updateZebra = function () {
    var zebracount = 0
    document.querySelectorAll(
      'tbody tr' +
      ':not(.hidden-by-os-filter)' +
      ':not(.hidden-by-type-filter)' +
      ':not(.hidden-by-search)').forEach(tr => {
      if (zebracount % 2 === 0) {
        tr.style.backgroundColor = '#eee'
      } else {
        tr.style.backgroundColor = ''
      }
      zebracount++
    }
    )
  }

  // Sort table by selected column
  // based on https://stackoverflow.com/a/19947532
  var sortRows = function () {
    var th = this
    const table = th.closest('table').querySelector('tbody')
    Array.from(table.querySelectorAll('tr:nth-child(n+1)'))
      .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
      .forEach(tr => table.appendChild(tr))
    updateZebra()
  }

  var init = function () {
    load()
    document.querySelector('#search').onkeyup = search
    document.querySelectorAll('th').forEach(th => th.addEventListener('click', sortRows))
    document.querySelectorAll('.filter').forEach(filter => { filter.onclick = updatefilters })
  }

  return {
    init: init
  }
})()

document.addEventListener('DOMContentLoaded', function () {
  main.init()
})
