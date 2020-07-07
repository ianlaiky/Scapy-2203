<?php

$username = $password = $error = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	file_put_contents('php://stderr', print_r("phisheduser: ".$username."\n", TRUE));
	file_put_contents('php://stderr', print_r("phishedpass: ".$password."\n", TRUE));
	if ($username == "admin" && $password == "password") {
		header("Location: success-phish.php");
	}
	else {
		$error = "Incorrect Credentials";
	}
}

?>

<form action="index-phish.php" method="POST">
	<h1>Enterprise Server Login (NOT REAL!)</h1>
	<?php 
		if (!empty($error)) {
			echo "<h2>" . $error . "</h2>";
		}
	?>
	<label for="fname">Username:</label><br>
	<input type="text" id="username" name="username"><br>
	<label for="password">Password:</label><br>
	<input type="password" id="password" name="password"><br>
	<br>
	<input type="submit" value="Submit">
</form>
