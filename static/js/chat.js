var ws = new WebSocket("ws://172.16.0.129:8000/chat");
ws.onmessage = function (evt) {
	var JSONObject = evt.data;
	console.log(JSONObject);
};
ws.onclose = function(){
	console.log('websocket close')
}
ms.onclick = function() {
	ws.send(['test','ddate','command']);
};
