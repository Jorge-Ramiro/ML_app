$(document).ready(function () {
  var size = 400;
  var video = document.getElementById("video");
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d", { willReadFrequently: true });
  var currentStream = null;
  var modelo = null;
  document.getElementById("predict").onclick = function () {
    modelo = "start";
  };
  document.getElementById("stop_predict").onclick = function () {
    modelo = "stop";
  };

  window.onload = function () {
    showcamera();
      setInterval(predecir, 2500) // se corre cada 2.5 s
  };

  function showcamera() {
    var options = {
      audio: false,
      video: {
        width: size,
        height: size,
      },
    };
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia(options)
        .then(function (stream) {
          currentStream = stream;
          video.srcObject = currentStream;
          procesarcamara();
        })
        .catch(function (err) {
          alert("No se pudo utilizar la camara :(");
          console.log(err);
          alert(err);
        });
    } else {
      alert("No existe la función getUserMedia");
    }
  }
  function procesarcamara() {
    ctx.drawImage(video, 0, 0, size, size, 0, 0, size, size);
    setTimeout(procesarcamara, 10);
  }
  function predecir() {
    console.log("La función fue llamada")
    var objetivo = document.getElementById("raza");
    if (modelo == "start") {
      resample_single(canvas, 229, 229, otrocanvas);
      var ctx2 = otrocanvas.getContext("2d", { willReadFrequently: true });
      var imgData = ctx2.getImageData(0, 0, 229, 229);
      // hacer el arreglo
      var arr = [];
      var arr229 = [];

      for (var p = 0; p < imgData.data.length; p += 4) {
        var red = imgData.data[p] / 255;
        var green = imgData.data[p + 1] / 255;
        var blue = imgData.data[p + 2] / 255;

        arr229.push([red, green, blue]);
        if (arr229.length == 229) {
          arr.push(arr229);
          arr229 = [];
        }
      }
      arr = [arr];
      const dict_values = { arr }; //Pass the javascript variables to a dictionary.
      const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
      $.ajax({
        url: "/prediction",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(s),
      });
      $.getJSON("/prediction", function (data) {
        $.each(data, function (key, val) {
          objetivo.innerHTML = val;
        });
      });
    } else {
      objetivo.innerHTML = "";
    }}

  /**
   *
   * @param {HtmlElement} canvas
   * @param {int} width
   * @param {int} height
   * @param {boolean} resize_canvas if true, canvas will be resized. Optional.
   * Cambiado por RT, resize canvas ahora es donde se pone el chico
   */
  function resample_single(canvas, width, height, resize_canvas) {
    var width_source = canvas.width;
    var height_source = canvas.height;
    width = Math.round(width);
    height = Math.round(height);

    var ratio_w = width_source / width;
    var ratio_h = height_source / height;
    var ratio_w_half = Math.ceil(ratio_w / 2);
    var ratio_h_half = Math.ceil(ratio_h / 2);

    var ctx = canvas.getContext("2d", { willReadFrequently: true });
    var ctx2 = resize_canvas.getContext("2d", { willReadFrequently: true });
    var img = ctx.getImageData(0, 0, width_source, height_source);
    var img2 = ctx2.createImageData(width, height);
    var data = img.data;
    var data2 = img2.data;

    for (var j = 0; j < height; j++) {
      for (var i = 0; i < width; i++) {
        var x2 = (i + j * width) * 4;
        var weight = 0;
        var weights = 0;
        var weights_alpha = 0;
        var gx_r = 0;
        var gx_g = 0;
        var gx_b = 0;
        var gx_a = 0;
        var center_y = (j + 0.5) * ratio_h;
        var yy_start = Math.floor(j * ratio_h);
        var yy_stop = Math.ceil((j + 1) * ratio_h);
        for (var yy = yy_start; yy < yy_stop; yy++) {
          var dy = Math.abs(center_y - (yy + 0.5)) / ratio_h_half;
          var center_x = (i + 0.5) * ratio_w;
          var w0 = dy * dy; //pre-calc part of w
          var xx_start = Math.floor(i * ratio_w);
          var xx_stop = Math.ceil((i + 1) * ratio_w);
          for (var xx = xx_start; xx < xx_stop; xx++) {
            var dx = Math.abs(center_x - (xx + 0.5)) / ratio_w_half;
            var w = Math.sqrt(w0 + dx * dx);
            if (w >= 1) {
              //pixel too far
              continue;
            }
            //hermite filter
            weight = 2 * w * w * w - 3 * w * w + 1;
            var pos_x = 4 * (xx + yy * width_source);
            //alpha
            gx_a += weight * data[pos_x + 3];
            weights_alpha += weight;
            //colors
            if (data[pos_x + 3] < 255)
              weight = (weight * data[pos_x + 3]) / 250;
            gx_r += weight * data[pos_x];
            gx_g += weight * data[pos_x + 1];
            gx_b += weight * data[pos_x + 2];
            weights += weight;
          }
        }
        data2[x2] = gx_r / weights;
        data2[x2 + 1] = gx_g / weights;
        data2[x2 + 2] = gx_b / weights;
        data2[x2 + 3] = gx_a / weights_alpha;
      }
    }
    ctx2.putImageData(img2, 0, 0);
  }
});
