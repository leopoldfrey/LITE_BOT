var sentencesData;
var $sentences = $("#sentences");
var sentences = new Array();
var mod = false;
var max = 0;
var defNbLines = 20;
var nbLines;
var from = 0;
var currRow;

function modified(m) {
  mod = m;
  if(mod) {
    $("#save").addClass('btn-warning');
    rowNum = parseInt(currRow.children("th").first().html());
    a = [];
    if(currRow.children(".check1").html().includes("span"))
      a.push(1);
    if(currRow.children(".check2").html().includes("span"))
      a.push(2);
    if(currRow.children(".check3").html().includes("span"))
      a.push(3);
    if(currRow.children(".check4").html().includes("span"))
      a.push(4);
    if(currRow.children(".check5").html().includes("span"))
      a.push(5);
    // if(currRow.children(".check6").html().includes("span"))
    //   a.push(6);

    //console.log("NUM", rowNum, " ", a);
    $.ajax({
        url: "/mod",
        type: "POST",
        data: JSON.stringify({
          "num": rowNum,
          "val": a
        }),
        success: function(response) {
            console.log(response['msg']);
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        }
    });
  } else {
    $("#save").removeClass('btn-warning');
  }
}

function sel(o) {
  currRow.removeClass("selected");
  currRow = o;
  currRow.addClass("selected");
  $("html, body").animate({ scrollTop: currRow.position.top });
}

function change(o) {
  if(o.html().includes("span"))
    o.html("");
  else
    o.html("<span class='icon-check'>");
}

function set(o) {
  o.html("<span class='icon-check'>");
}

function clear(o) {
  o.html("");
}

function save()
{
  $.ajax({
    url: "/save",
    type: "GET",
    success: function(response) {
        console.log(response['msg']);
    },
    error: function(jqXHR, textStatus, errorMessage) {
        console.log(errorMessage); // Optional
    }
  });
  modified(false);
}

function load()
{
  if(from < 0)
    from = 0;
  else if(from + nbLines > max) {
    from = max - nbLines;
  }
  urlFromTo = "/getSentences/"+from+"/"+(from+nbLines);
  console.log("LOAD "+urlFromTo, max);
  history.pushState({}, null, "index.html?from="+from+"&max="+nbLines);
  $.ajax({
      url: urlFromTo,
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
}

function loadPrevPage() {
  from -= nbLines;
  load();
}

function loadNextPage() {
  from += nbLines;
  load();
}

function fillSentences(data) {
  $sentences.empty();
  sentencesData = data;
  len = Object.keys(sentencesData).length;
  Object.keys(sentencesData).forEach((item, i) => {
    sentence = sentencesData[item];
    ii = parseInt(item)
    $sentences.append(
      "<tr class='sentenceRow'><th class='sentenceNum' scope='row'>" + ii + "</th>" +
      "<td class='sentenceElem'>" + sentence['txt'] + "</td>"+
      "<td class='sentenceElem check check1'>"+(sentence['in'].includes(1) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check2'>"+(sentence['in'].includes(2) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check3'>"+(sentence['in'].includes(3) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check4'>"+(sentence['in'].includes(4) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check5'>"+(sentence['in'].includes(5) ? "<span class='icon-check'>" : "")+"</td>"+
      /*"<td class='sentenceElem check check6'>"+(sentence['in'].includes(6) ? "<span class='icon-check'>" : "")+"</td>"+*/
      "</tr>");
  });

  $('.check').dblclick(function() {
    change($(this));
    modified(true);
  });

  currRow = $('.sentenceRow').first();
  currRow.addClass("selected");
  $('.sentenceRow').click(function() {
    sel($(this));
  });
}

function next() {
  c = currRow.next();
  if (c.length > 0) {
      sel(c);
  } else {
    loadNextPage();
  }
}

function prev() {
  c = currRow.prev();
  if (c.length > 0) {
      sel(c);
  } else {
    loadPrevPage();
  }
}

$(window).keydown(function (e) {
    //console.log(e.which);
    shifted = e.shiftKey;
    var c = "";
    if (e.which == 38) { // Up Arrow
      prev();
    } else if (e.which == 40 || e.which == 32) { // Down Arrow
      next();
    } else if (e.which == 37) { // < Arrow
      loadPrevPage();
    } else if (e.which == 39) { // > Arrow
      loadNextPage();
    } else if (e.which == 49) {
      set(currRow.children(".check1"));
      if(!e.shiftKey) {
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
        //clear(currRow.children(".check6"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 50) {
      set(currRow.children(".check2"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
        //clear(currRow.children(".check6"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 51) {
      set(currRow.children(".check3"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
        //clear(currRow.children(".check6"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 52) {
      set(currRow.children(".check4"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check5"));
        //clear(currRow.children(".check6"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 53) {
      set(currRow.children(".check5"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        //clear(currRow.children(".check6"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 54) {
      //set(currRow.children(".check6"));
      //if(currRow.children(".check6").html().includes("span")) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
      //}
      modified(true);
      next();
    } else if (e.which == 83 && e.shiftKey) {
      //save();
    }
});

$(window).on('load', function() {
  // connectToWS();
  url = new URL(window.location.href);
  from = parseInt(url.searchParams.get('from'));
  nbLines = parseInt(url.searchParams.get('max'));
  if(!from)
    from = 0;
  if(!nbLines)
    nbLines = defNbLines;
  console.log("from", from," nbLines", nbLines);
  $.ajax({
    url: "/getMax",
    type: "GET",
    success: function(response) {
        max = response['max'];
        load();
    },
    error: function(jqXHR, textStatus, errorMessage) {
        console.log(errorMessage); // Optional
    }
  });
});

$('#open').click(function() {
  load();
});

$('#save').click(function() {
  save();
});

$('#prev').click(function() {
  loadPrevPage();
});

$('#next').click(function() {
  loadNextPage();
});

$('#upload').click(function() {
  console.log("TODO UPLOAD");
  $('#jsonfile-input').trigger('click');
});

$('#jsonfile-input').on('change', function(){
  //console.log("UPLOAD JSON FILE", $('#jsonfile-input').val())
  uploadFile($('#jsonfile-input').val(), $('#jsonfile-input').prop('files')[0]);
});

function uploadFile(fname, file) {
  console.log("Uploading snd file", fname);
  var formData = new FormData();
  formData.append("jsonFile", file);

  $(".progress").show();
  $(".progress-bar").css("width", 0);

  $.ajax({
      xhr: function() {
          var xhr = new window.XMLHttpRequest();

          // Upload progress
          xhr.upload.addEventListener("progress", function(evt){
              if (evt.lengthComputable) {
                  var percentComplete = evt.loaded / evt.total;
                  $(".progress-bar").css("width", percentComplete*100+"%");
              }
         }, false);

         // Download progress
         xhr.addEventListener("progress", function(evt){
             if (evt.lengthComputable) {
                 var percentComplete = evt.loaded / evt.total;
                 $(".progress-bar").css("width", 100+"%");
             }
         }, false);

         return xhr;
      },
      url: "/upload",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $(".progress").hide();
        console.log(response);
        load();
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
}

$('#download').click(function() {
  $.ajax({
    url: "/download",
    type: "GET",
    success: function(response) {
        var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(response, undefined, 2));
        var a = document.createElement('a');
        a.href = 'data:' + data;
        a.download = 'festinTri.json';
        a.innerHTML = 'download JSON';
        a.style = 'display: none';
        document.getElementById('topContainer').appendChild(a);
        a.click();
    },
    error: function(jqXHR, textStatus, errorMessage) {
        console.log(errorMessage); // Optional
    }
  });
  modified(false);
});
//
// function connectToWS() {
//   // Connect to websocket server
//   ws = new WebSocket(wsServer);
//
//   // Log messages from the server
//   ws.onmessage = function (e) {
//       if(e.data == "uploadStart") {
//         $(".progress-bar").css("width", 0);
//         $("#progress").show();
//       } else if(e.data == "uploadStop") {
//         $("#progress").hide();
//         $(".progress-bar").css("width", 0);
//       } else if(e.data.startsWith("upload")) {
//         v = e.data.split("=")[1];
//         //console.log("UPLOAD", v);
//         $("#progress").show();
//         $(".progress-bar").css("width", v);
//       } else {
//         console.log("| WS Received message: " + e.data);
//       }
//   };
//
//   // Log errors
//   ws.onerror = function (error) {
//       console.error("WebSocket Error " + error.stack);
//   };
//
//   ws.onopen = function (event) {
//       console.log("- Connected to ws server");
//   };
//
//   ws.onclose = function (event) {
//       console.log("- Connection to ws server CLOSED!!!");
//   };
// }
