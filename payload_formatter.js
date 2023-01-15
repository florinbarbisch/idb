function decodeUplink(input) {
  var bytes = input.bytes;
  var string = String.fromCharCode(...bytes)

  var stringSplit = string.split(";");
  var co2, temperature, humidity;
  var warnings = [];
  var errors = [];
  
  try {
    co2 = parseInt(stringSplit[0]);
    temperature = parseFloat(stringSplit[1] / 100);
    humidity = parseFloat(stringSplit[2] / 100);
  } catch (err) {
    errors.push("Error parsing input bytes: " + err);
  }
  
  if (isNaN(co2) || isNaN(temperature) || isNaN(humidity)) {
    errors.push("Invalid input bytes: expected numbers but got " + byteArray[0] + "," + byteArray[1] + "," + byteArray[2]);
  }
  
  return {
    data: {
      co2: co2,
      temperature: temperature,
      humidity: humidity
    },
    warnings: warnings,
    errors: errors
  };
}
