<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "rights_maintain", 0, $db_connection );
?>

<html>
	<head>
		<title>
			Modify User
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Select the User to Modify</h1></p>

		<p><table border>
			<tr>
				<td>Username</td>
				<td>Name</td>
				<td>E-mail</td>
				<td>Change without<br/>peer review</td>
				<td>Approve Changes</td>
				<td>Modify Users</td>
				<td></td>
			</tr>
			<?php
				$result = query_sql( "select * from user where deleted = 0", $db_connection );

				$row = mysql_fetch_array( $result );

				while ( $row )
				{
					echo( "<tr><td>" );
					echo( $row[ 'username' ] );
					echo( "</td><td>" );
					echo( $row[ 'name' ] );
					echo( "</td><td>" );
					echo( $row[ 'email' ] );
					echo( "</td><td>" );
					echo( $row[ 'rights_modify' ] == 0 ? "No" : "Yes" );
					echo( "</td><td>" );
					echo( $row[ 'rights_approve' ] == 0 ? "No" : "Yes" );
					echo( "</td><td>" );
					echo( $row[ 'rights_maintain' ] == 0 ? "No" : "Yes" );
					echo( "</td><td>" );

					link_to_page_with_params( "modify_other2.php", "user_id=" . $row[ 'id' ], "Modify" );

					echo( "</td></tr>" );

					$row = mysql_fetch_array( $result );
				}

				mysql_free_result( $result );

				mysql_close( $db_connection );
			?>
		</table></p>
	</body>
</html>

