<html><body>
<script>
var myNumbers = {
	"tal1": 10,
	"tal2": 15
}

var jsonObj = JSON.stringify(myNumbers);

$.post( "http://hampus.simulations.io/add", jsonObj, function( result ) {
	//Detta exekveras nar svar har fatts

	console.log(result.summa); //Skriv ut summan

}, "json"); //Denna fjarte parameter till $.post() auto-decodar JSON sa man slipper gora det sjalv
</body></script>
</html>
