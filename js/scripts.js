var sentencesData;
var $sentences = $("#sentences");
var modalSentence = $('#modalSentence');
var newSentence = $('#newSentence')
var sentences = new Array();
var mod = false;
var max = 0;
var defNbLines = 100;
var nbLines;
var from = 0;
var cat = -1;
var currRow;
var editing = false;

function modified(m) {
  mod = m;
  if(mod) {
    $("#download").addClass('btn-warning');
    rowNum = parseInt(currRow.children("th").first().html());
    txt = currRow.children(".sentenceEdit").html();
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

    // console.log("NUM", rowNum, " ", a, " ", txt);
    $.ajax({
        url: "/mod",
        type: "POST",
        data: JSON.stringify({
          "num": rowNum,
          "txt": escape(txt.replaceAll('\n','')),//JSON.stringify(txt.replaceAll(',','_COMMA_').replaceAll(';','_COMMADOT_').replaceAll('\'','_QUOT1_').replaceAll('\"','_QUOT2_')),
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
    $("#download").removeClass('btn-warning');
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
  else if(from + nbLines >= max) {
    from = max - nbLines + 1;
  }
  if(cat >= 0) {
    urlFromTo = "/getCat"+cat;
    console.log("LOAD Category "+cat);
    history.pushState({}, null, "index.html?cat="+cat);
  } else {
    urlFromTo = "/getSentences/"+from+"/"+(from+nbLines);
    console.log("LOAD "+urlFromTo, max);
    history.pushState({}, null, "index.html?from="+from+"&max="+nbLines);
  }
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
  console.log("Length", len);

  switch(cat){
    case -1:
      $("#info").html(from + " > " +(from+nbLines-1)+" / "+max);
      break;
    case 0:
      $("#info").html("All ("+len+")");
      break;
    case 1:
      $("#info").html("Introduction ("+len+")");
      break;
    case 2:
      $("#info").html("Séduction ("+len+")");
      break;
    case 3:
      $("#info").html("Provocation ("+len+")");
      break;
    case 4:
      $("#info").html("Fuite ("+len+")");
      break;
    case 5:
      $("#info").html("Passe-partout ("+len+")");
      break;
  }

  Object.keys(sentencesData).forEach((item, i) => {
    sentence = sentencesData[item];
    ii = parseInt(item);
    txt = unescape(sentence['txt']).replaceAll('’','\'').replaceAll('\n','').replace(new RegExp(String.fromCharCode(160), "g"), " ");
    $sentences.append(
      "<tr class='sentenceRow'><th class='sentenceNum' scope='row'>" + ii + "</th>" +
      "<td class='sentenceElem sentenceEdit' id='sentence"+ii+"'>" + txt + "</td>"+
      "<td class='sentenceElem check check1'>"+(sentence['in'].includes(1) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check2'>"+(sentence['in'].includes(2) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check3'>"+(sentence['in'].includes(3) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check4'>"+(sentence['in'].includes(4) ? "<span class='icon-check'>" : "")+"</td>"+
      "<td class='sentenceElem check check5'>"+(sentence['in'].includes(5) ? "<span class='icon-check'>" : "")+"</td>"+
      "</tr>");
  });

  $('.check').dblclick(function() {
    change($(this));
    modified(true);
  });

  $('.sentenceEdit').dblclick(function() {
    edit();
  });

  currRow = $('.sentenceRow').first();
  currRow.addClass("selected");
  $('.sentenceRow').click(function() {
    sel($(this));
  });
}

function edit()
{
  editing = true;
  var sentence = currRow.children(".sentenceEdit").html();
  newSentence.val(sentence);
  setTimeout(function(){newSentence.focus();}, 500);
  modalSentence.modal('show');
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
    if(editing)
      return;
    // console.log(e.which);
    shifted = e.shiftKey;
    var c = "";
    if (e.which == 13) { // Enter
      edit();
    } else if (e.which == 38) { // Up Arrow
      prev();
    } else if (e.which == 40 || e.which == 32) { // Down Arrow
      next();
    } else if (e.which == 37) { // < Arrow
      loadPrevPage();
    } else if (e.which == 39) { // > Arrow
      loadNextPage();
    } else if (e.which == 49) { // 1
      set(currRow.children(".check1"));
      if(!e.shiftKey) {
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 50) { // 2
      set(currRow.children(".check2"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 51) { // 3
      set(currRow.children(".check3"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check4"));
        clear(currRow.children(".check5"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 52) { // 4
      set(currRow.children(".check4"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check5"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 53) { // 5
      set(currRow.children(".check5"));
      if(!e.shiftKey) {
        clear(currRow.children(".check1"));
        clear(currRow.children(".check2"));
        clear(currRow.children(".check3"));
        clear(currRow.children(".check4"));
      }
      modified(true);
      if(!e.shiftKey)
        next();
    } else if (e.which == 54) { // 6
      clear(currRow.children(".check1"));
      clear(currRow.children(".check2"));
      clear(currRow.children(".check3"));
      clear(currRow.children(".check4"));
      clear(currRow.children(".check5"));
      modified(true);
      next();
    } else if (e.which == 55) { //7
      set(currRow.children(".check1"));
      set(currRow.children(".check2"));
      set(currRow.children(".check3"));
      set(currRow.children(".check4"));
      set(currRow.children(".check5"));
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
  cat = parseInt(url.searchParams.get('cat'));
  if(!from)
    from = 0;
  if(!nbLines)
    nbLines = defNbLines;
  console.log("from", from," nbLines", nbLines);
  if(!cat)
    cat = -1;
  console.log("cat", cat);
  $.ajax({
    url: "/getMax",
    type: "GET",
    success: function(response) {
        max = parseInt(response['max']);
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
  // console.log("TODO UPLOAD");
  $('#jsonfile-input').trigger('click');
});

$('#jsonfile-input').on('change', function(){
  //console.log("UPLOAD JSON FILE", $('#jsonfile-input').val())
  uploadFile($('#jsonfile-input').val(), $('#jsonfile-input').prop('files')[0]);
});

$("#all").click(function(){
  console.log("Tri all");
  cat = 0;
  history.pushState({}, null, "index.html?cat=0");
  $.ajax({
      url: "/getCat0",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#cat1").click(function(){
  console.log("Tri cat1");
  cat = 1;
  history.pushState({}, null, "index.html?cat=1");
  $.ajax({
      url: "/getCat1",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#cat2").click(function(){
  console.log("Tri cat2");
  cat = 2;
  history.pushState({}, null, "index.html?cat=2");
  $.ajax({
      url: "/getCat2",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#cat3").click(function(){
  console.log("Tri cat3");
  cat = 3;
  history.pushState({}, null, "index.html?cat=3");
  $.ajax({
      url: "/getCat3",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#cat4").click(function(){
  console.log("Tri cat4");
  cat = 4;
  history.pushState({}, null, "index.html?cat=4");
  $.ajax({
      url: "/getCat4",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#cat5").click(function(){
  console.log("Tri cat5");
  cat = 5;
  history.pushState({}, null, "index.html?cat=5");
  $.ajax({
      url: "/getCat5",
      type: "GET",
      success: function(response) {
          fillSentences(response);
          $("html, body").animate({ scrollTop: 0 });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
});

$("#plus").click(function(){
  // console.log("PLUS !", cat);
  currRow.removeClass("selected");

  idx = max + 1;
  $sentences.append(
    "<tr class='sentenceRow' onclick='sel($(this));'><th class='sentenceNum' scope='row'>" + idx + "</th>" +
    "<td class='sentenceElem sentenceEdit' id='sentence"+idx+"' ondblclick='edit();'></td>"+
    "<td class='sentenceElem check check1' ondblclick='change($(this)); modified(true);'>"+(cat == 1 ? "<span class='icon-check'>" : "")+"</td>"+
    "<td class='sentenceElem check check2' ondblclick='change($(this)); modified(true);'>"+(cat == 2 ? "<span class='icon-check'>" : "")+"</td>"+
    "<td class='sentenceElem check check3' ondblclick='change($(this)); modified(true);'>"+(cat == 3 ? "<span class='icon-check'>" : "")+"</td>"+
    "<td class='sentenceElem check check4' ondblclick='change($(this)); modified(true);'>"+(cat == 4 ? "<span class='icon-check'>" : "")+"</td>"+
    "<td class='sentenceElem check check5' ondblclick='change($(this)); modified(true);'>"+(cat == 5 ? "<span class='icon-check'>" : "")+"</td>"+
    "</tr>");

  currRow = $('.sentenceRow').last();
  currRow.addClass("selected");
  max++;
  currRow.get(0).scrollIntoView();
  setTimeout(function(){
    edit();
  }, 1000);
});

$("#del").click(function(){
  idx = currRow.children(".sentenceNum").html();
  console.log("Delete", idx);
  $("#download").addClass('btn-warning');
  $.ajax({
      url: "/del",
      type: "POST",
      data: JSON.stringify({
        "num": idx
      }),
      success: function(response) {
          console.log(response['msg']);
          // load();
          $.ajax({
            url: "/getMax",
            type: "GET",
            success: function(response) {
                max = parseInt(response['max']);
                load();
            },
            error: function(jqXHR, textStatus, errorMessage) {
                console.log(errorMessage); // Optional
            }
          });
      },
      error: function(jqXHR, textStatus, errorMessage) {
          console.log(errorMessage); // Optional
      }
  });
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
    url: "/save",
    type: "GET",
    success: function(response) {
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
    },
    error: function(jqXHR, textStatus, errorMessage) {
        console.log(errorMessage); // Optional
    }
  });
  modified(false);
});

// MODAL SENTENCE INPUT

function validSentence(ev) {
  ev.preventDefault();
  currRow.children(".sentenceEdit").html(newSentence.val());
  // console.log("VALID", currRow);
  modalSentence.modal('hide');
  modified(true);
}

function cancel(ev) {
  //
}

modalSentence.on("hide.bs.modal", function(){
  // console.log("HIDE", $('.sentenceRow').last().is(currRow), "("+newSentence.val()+")");
  if($('.sentenceRow').last().is(currRow) && newSentence.val() == "")
  {
    idx = currRow.children(".sentenceNum").html();
    currRow.remove()
    console.log("REMOVE LAST", idx);
  }
  editing = false;
});

$("#Close").click(function(ev)
{
  // console.log("CLOSE");
  cancel(ev);
});

$('#Cancel').click(function(ev)
{
  // console.log("CANCEL");
  cancel(ev);
});

modalSentence.submit(function(ev)
{
  // console.log("SUBMIT");
  validSentence(ev);
});


$('#Ok').click(function(ev)
{
  // console.log("OK");
  validSentence(ev);
});
