<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "", 0, $db_connection );
?>

<html>
	<head>
		<title>
			Modify Convention
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Select a Convention to Modify</h1></p>

		<p><table border>
			<tr>
				<td>Name</td>
				<td>Date</td>
				<td>Location</td>
				<td></td>
			</tr>
			<?php
				$result = query_sql( get_convention_details_sql() 
						. "where t1.country_id = t2.id and end_date > current_date() "
						. "and approved = true order by day_count", $db_connection );

				$row = mysql_fetch_array( $result );

				while ( $row )
				{
					echo( "<tr><td>" );
					echo( $row[ 'name' ] );
					echo( "</td><td>" );
					echo( $row[ 'start_date' ] . " - " . $row[ 'end_date' ] );
					echo( "</td><td>" );
					echo( $row[ 'location' ] . ", " . $row[ 'country_name' ] );
					echo( "</td><td>" );

					$mod_result = query_sql( "select * from convention where modified_from = " 
							. $row[ 'id' ], $db_connection );

					if ( mysql_num_rows( $mod_result ) == 0 )
					{
						link_to_page_with_params( "modify2.php", "con_id=" . $row[ 'id' ], "Modify" );
					}
					else
					{
						echo("Awaiting approval");
					}

					mysql_free_result( $mod_result );

					echo( "</td></tr>" );

					$row = mysql_fetch_array( $result );
				}

				mysql_free_result( $result );

				mysql_close( $db_connection );
			?>
		</table></p>
	</body>
</html>

