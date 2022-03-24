var is_logged = false;

function check_login(){
  console.log("check_login");
  a = new window.XMLHttpRequest;
  a.open("POST", "/is_logged");
  a.onload = function(b){
    resp = JSON.parse(b.currentTarget.response);
    is_logged = resp != false;
    display_login();
  };
  a.send("");
}

function click_login(){
  console.log("click_login");
  a = new window.XMLHttpRequest;
  a.open("HEAD", "/login");
  a.onload = function(b){
    is_logged = true;
    display_login();
  };
  a.send("");
}

function click_logout(){
  console.log("click_logout");
  a = new window.XMLHttpRequest;
  a.open("HEAD", "/login", !0, "logout", (new Date).getTime().toString());
  a.onload = function(b){
    is_logged = false;
    display_login();
  };
  a.send("");
}

function display_login() {
  is_logged ? load_login() : unload_login();
}

function load_login() {
  $(".logged_only").show();
  $(".logged_hide").hide();
}

function unload_login() {
  $(".logged_only").hide();
  $(".logged_hide").show();
}

function send_new_song() {
  var name = $("#newSong").val();
  if (name == "") {
    alert("Cannot add unnamed song");
  } else {
    $.post("/new_song", {name: name}).done(function(data) {
      console.log(data);
      $("#songs").empty();
      loadSongList();
    });
  }
}

function del_song() {
  var name = $("#songSelect").val();
  if (name != "nochoice" && confirm("Are you sure you want to remove " + name +
              "? This action cannot be canceled.")) {
    $.post("/del_song", {name: name}).done(function(data) {
      console.log(data);
      $("#songs").empty();
      loadSongList();
    });
  }
}

function delTrack(trackName) {
  var name = $("#songSelect").val();
  console.log("removing", trackName, name);
  if (name != "nochoice" && confirm("Are you sure you want to remove " + trackName +
              "? This action cannot be canceled.")) {
    $.post("/del_track", {name: name, trackName: trackName}).done(function(data) {
      console.log(data);
      loadSong($("#songSelect").val());
    });
  }
}

function addNewTrack() {
  $("#iaddTrack").click();
}

function send_files_recurs(song, files) {
  console.log(files)
  var file_data = files.pop();
  var form_data = new FormData();
  form_data.append('file', file_data);
  form_data.append('song', song);
  console.log(form_data);
  $.ajax({
    url: '/add_track',
    dataType: 'json',
    cache: false,
    contentType: false,
    processData: false,
    data: form_data,
    type: 'post',
    success: function(php_script_response){
      console.log(php_script_response);
      if (files.length > 0) {
        send_files_recurs(song, files);
      } else {
        currentSong.name = ""
        $("#songSelect").change();
      }
    }
  });
}

function updatedTracks() {
  var name = $("#songSelect").val();
  if (name != "nochoice") {
    send_files_recurs(name, Array.from($('#iaddTrack').prop('files')))
  } else {
    alert("Please choose a song name to upload tracks.")
  }
}
