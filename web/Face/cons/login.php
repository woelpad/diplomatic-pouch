<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	if ( isset( $_POST['username'] ) )
	{
		$db_connection = connect_to_database();

		$username = $_POST['username'];
		$password = $_POST['password'];
		
		$result = query_sql( "select * from user where deleted = false and "
				. "username = '" . $username . "' and "
				. "password = md5( '" . $password . "')", $db_connection );

		$row = mysql_fetch_array( $result );

		if ( $row )
		{
			// Login successful
			$_SESSION['user_id'] = $row[ 'id' ];

			mysql_free_result( $result );

			$sql = 'update user set notifications = 0, last_notification = "2000-01-02" '
				 . 'where id = ' . $_SESSION['user_id'];

			query_sql( $sql, $db_connection );

			mysql_close( $db_connection );

			goto_page( "maintain.php" );
		}
		else
		{
			// Login failed
			$error = "Incorrect username or password";

			mysql_free_result( $result );

			mysql_close( $db_connection );
		}
	}
?>

<html>
	<head>
		<title>
			Login
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Login</h1></p>

		<table border>
			<tr><td>
				<P><h2 align=center>Existing Users</h2></P>

				<form action="<?php link_to_self(); ?>" method="post">
					<table>
						<tr>
							<td>Username</td>
							<td>
								<input type="text" name="username" value="" size=30>
							</td>
						</tr>
						<tr>
							<td>Password</td>
							<td>
								<input type="password" name="password" value="" size=30>
							</td>
						</tr>
						<tr>
							<td colspan=2 align=center>
								<input type="submit" name="Submit" value="Login">
							</td>
						</tr>
					</table>
				</form>
			</td><tr>

			<tr><td>
				<P><h2 align=center>New Users</h2></P>

				<P align=center><B><A HREF="register.php">Create a new account</A></B></P>
			</td></tr>
		</table>
	</body>
</html>
