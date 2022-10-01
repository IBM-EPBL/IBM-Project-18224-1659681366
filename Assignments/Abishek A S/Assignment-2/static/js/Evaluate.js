function Evaluate(){
	var password = document.getElementById("password");
	var confirm = document.getElementById("confirmpassword");

	
	if(password.value != confirm.value){
		alert("Password does't Match");
		return false;
	}
	
	else if(password.value >= 6 || confirm.value >=6){
        alert("password Must be minimum of 6 character");
		return false;
	}
	return true;
}