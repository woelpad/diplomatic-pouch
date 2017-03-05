<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	if ( isset( $_POST[ 'username' ] ) )
	{
		if ( $_POST[ 'password' ] != $_POST[ 'confirm_password' ] )
		{
			$error = "Please enter the same password in both boxes";
		}
		else if ( $_POST[ 'email' ] != $_POST[ 'confirm_email' ] )
		{
			$error = "Please enter the same e-mail address in both boxes";
		}
		else if ( ( $_POST[ 'username' ] == "" )
			   || ( $_POST[ 'password' ] == "" )
			   || ( $_POST[ 'email' ] == "" )
			   || ( $_POST[ 'real_name' ] == "" ) )
		{
			$error = "Please complete all fields";
		}
		else
		{
			$result = query_sql( "select * from user where username = '" . $_POST[ 'username' ] 
					. "'", $db_connection );

			if ( mysql_num_rows( $result ) != 0 )
			{
				mysql_free_result( $result );

				$error = "Username is already taken";
			}
			else
			{
				mysql_free_result( $result );

				$new_key = get_new_key( "user", $db_connection );

				query_sql( "insert into user values( " . $new_key . ", '" 
						. mysql_real_escape_string( $_POST[ 'username' ], $db_connection )
						. "', md5( '" . $_POST[ 'password' ] . "' ), '"
						. mysql_real_escape_string( $_POST[ 'real_name' ], $db_connection )
						. "', '" . mysql_real_escape_string( $_POST[ 'email' ], $db_connection )
						. "', false, false, false, false, 0, '2000-01-01'  )", $db_connection );

				$_SESSION['user_id'] = $new_key;

				mysql_close( $db_connection );

				goto_page( "maintain.php" );
			}
		}
	}

	mysql_close( $db_connection );
?>

<html>
	<head>
		<title>
			Register User
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Register a New User</h1></p>

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
					<td>Confirm Password</td>
					<td>
						<input type="password" name="confirm_password" value="" size=30>
					</td>
				</tr>
				<tr>
					<td>Real Name</td>
					<td>
						<input type="text" name="real_name" value="" size=30>
					</td>
				</tr>
				<tr>
					<td>E-mail</td>
					<td>
						<input type="text" name="email" value="" size=30>
					</td>
				</tr>
				<tr>
					<td>Confirm E-mail</td>
					<td>
						<input type="text" name="confirm_email" value="" size=30>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<input type="submit" name="Submit" value="Register">
					</td>
				</tr>
			</table>
		</form>
	</body>
</html>
