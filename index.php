<?php

$username = $password = $error = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	$username = test_input($_POST["username"])
	$password = test_input($_POST["password"])
	if ($username == "admin" && $password == "password") {
		header("Location: http://localhost:80/test/success.php");
	}
	else {
		$error = "Incorrect Credentials";
	}
}

?>

<form action="index.php" method="POST">
	<h1>Enterprise Server Login</h1>
	<?php 
		if (!empty($error)) {
			echo "<h2>" . $error . "</h2>";
		}
	?>
	<label for="fname">Username:</label><br>
	<input type="text" id="username" name="username"><br>
	<label for="password">Password:</label><br>
	<input type="text" id="password" name="password"><br>
	<br>
	<input type="submit" value="Submit">
</form>