function valid(){
	var pwd = document.getElementById("cpass");
	var cpwd = document.getElementById("ccpass");

	
	if(pwd.value >= 6 || cpwd.value >=6){
		alert("password Must be minimum of 6 character");
		return false;
	}
	
	else if(pwd.value != cpwd.value){
		alert("Password does't Match");
		return false;
	}
	return true;
	  
}