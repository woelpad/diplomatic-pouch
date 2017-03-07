<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "rights_maintain", 0, $db_connection );

	if ( isset( $_POST['country'] ) )
	{
		$continent = $_POST['continent'];
		$country = $_POST['country'];

		$result = query_sql( "select * from country where name = '" . $country . "'", $db_connection );

		if ( mysql_num_rows( $result ) > 0 )
		{
			$error = "Country already exists";
		}

		mysql_free_result( $result );

		if ( $error == "" )
		{
			$new_key = get_new_key( "country", $db_connection );

			$result = query_sql( "insert into country values ( " . $new_key . ", '" . $country 
						. "', null, " . $continent . " )", $db_connection );

			mysql_free_result( $result );

			goto_page( "maintain.php" );
		}
	}

	mysql_close( $db_connection );
?>

<html>
	<head>
		<title>
			Add New Country
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Add a new country to the database</h1></p>

		<form action="<?php link_to_self(); ?>" method="post">
			<table>
				<tr>
					<td>Continent</td>
					<td>
						<select name="continent">
							<option value="0">--- Select Continent ---</option>

							<?php
								$db_connection = connect_to_database();

								$result = query_sql( "select * from continent order by id", 
											$db_connection );

								$row = mysql_fetch_array( $result );

								while ( $row )
								{
									echo('<option value="' .$row[ "id" ] . '">' . $row[ "name" ] 
											. '</option>\n');

									$row = mysql_fetch_array( $result );
								}

								mysql_free_result( $result );

								mysql_close( $db_connection );
							?>
						</select>
					</td>
				</tr>
				<tr>
					<td>Country</td>
					<td>
						<input type="text" name="country" value="" size=30>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<input type="submit" name="Submit" value="Continue">
					</td>
				</tr>
			</table>
		</form>
	</body>
</html>
