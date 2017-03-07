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
			   || ( $_POST[ 'email' ] == "" )
			   || ( $_POST[ 'real_name' ] == "" ) )
		{
			$error = "Please complete all fields";
		}
		else
		{
			$result = query_sql( "select * from user where username = '" . $_POST[ 'username' ] 
					. "' and id <> " . $_SESSION[ 'user_id' ], $db_connection );

			if ( mysql_num_rows( $result ) != 0 )
			{
				mysql_free_result( $result );

				$error = "Username is already taken";
			}
			else
			{
				mysql_free_result( $result );

				query_sql( "update user set username='"
						. mysql_real_escape_string( $_POST[ 'username' ], $db_connection )
						. "', name='"
						. mysql_real_escape_string( $_POST[ 'real_name' ], $db_connection )
						. "', email='" 
						. mysql_real_escape_string( $_POST[ 'email' ], $db_connection )
						. "' where id=" . $_SESSION[ 'user_id' ], $db_connection );

				if ( $_POST[ 'password' ] != "" )
				{
					query_sql( "update user set password=md5('"
							. mysql_real_escape_string( $_POST[ 'password' ], $db_connection )
							. "') where id=" . $_SESSION[ 'user_id' ], $db_connection );
				}

				mysql_close( $db_connection );

				goto_page( "maintain.php" );
			}
		}
	}
?>

<html>
	<head>
		<title>
			Modify Account
		</title>
	</head>
	<body>
		<?php
			report_error( $error );

			$result = query_sql( "select * from user where id = " . $_SESSION[ 'user_id' ], 
					$db_connection );

			$row = mysql_fetch_array( $result );
		?>

		<p><h1>Modify Account</h1></p>

		<form action="<?php link_to_self(); ?>" method="post">
			<table>
				<tr>
					<td>Username</td>
					<td>
						<?php
							form_input( "username", $row[ 'username' ], 30 );
						?>
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
						<?php
							form_input( "real_name", $row[ 'name' ], 30 );
						?>
					</td>
				</tr>
				<tr>
					<td>E-mail</td>
					<td>
						<?php
							form_input( "email", $row[ 'email' ], 30 );
						?>
					</td>
				</tr>
				<tr>
					<td>Confirm E-mail</td>
					<td>
						<?php
							form_input( "confirm_email", $row[ 'email' ], 30 );
						?>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<input type="submit" name="Submit" value="Modify">
					</td>
				</tr>
			</table>
		</form>
	</body>
</html>

<?php
	mysql_close( $db_connection );
?>
