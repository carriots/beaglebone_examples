var https = require('https');
var bones = require('bonescript');


var send_stream = function(device, apikey, data){
    var stream = '{"protocol":"v2","device":"'+device+'","at":"now","data":'+data+'}'

    var options = {
      host: 'api.carriots.com',
      path: '/streams',
      method: 'POST',
      headers: {'User-Agent': 'NodeJS-Carriots',
                'Content-Type' : 'application/vnd.carriots.api.v2+json;q=7',
                'Accept': 'application/vnd.carriots.api.v2+json;q=7',
               'Content-Length': stream.length,
                'Carriots.apikey': apikey}
    };

    var req = https.request(options, function(response) {
      console.log('STATUS: ' + response.statusCode);
      //console.log('HEADERS: ' + JSON.stringify(response.headers));
      response.setEncoding('utf8');
      response.on('data', function (chunk) {
        console.log('BODY: ' + chunk);
      });
    });

    req.on('error', function(e) {
      console.log('problem with request: ' + e.message);
    });

    req.write(stream);
    req.end();
};

var main = function(){
    var gpiopin = "P9_33";

    var on = "ON"
    var off = "OFF"

    var device = 'your device id_developer here'
    var apikey = 'your apikey here'
    var data = ''

    var lights = off
    var new_lights = lights

    setInterval(read_analog_pin, 500);

    function read_analog_pin() {
        bones.analogRead(gpiopin, get_status);
        function get_status(x) {
            var n_status = x.value * 1000

            if (n_status > 2.0) {
                new_lights = off
            } else {
                new_lights = on
            }
            console.log(new_lights);

            if (lights != new_lights){
                lights = new_lights
                data = '{"light": "'+ new_lights +'"}'
                console.log(data);
                send_stream(device, apikey, data);
            }
        }
    }
}

main()
