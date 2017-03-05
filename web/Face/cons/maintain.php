<?php
	session_start();

	require_once( 'utils.php' );

	$db_connection = connect_to_database();

	check_page( "", 0, $db_connection );
?>

<html>
	<head>
		<title>
			Maintain Convention Database
		</title>
	</head>
	<body>
		<p><h1>Maintain Convention Database</h1></p>

		<p><h2>Make changes</h2>

		<?php
			echo ("<P>");

			link_to_page( "add_convention.php", "Add Convention" );

			echo( "</P>" );

			echo ("<P>");

			link_to_page( "modify_convention.php", "Modify Convention" );

			echo( "</P>" );

			$approve_rights = check_rights( "rights_approve", 0, $db_connection );

			if ( $approve_rights )
			{
				$add_result = query_sql( "select * from convention where approved = false and "
						. "modified_from is null", $db_connection );

				$mod_result = query_sql( "select * from convention where approved = false and "
						. "modified_from is not null", $db_connection );
			}
			else
			{
				// Create an empty result
				$add_result = query_sql( "select * from convention where true = false", 
						$db_connection );

				$mod_result = query_sql( "select t1.id, t1.name, t1.start_date, t1.end_date, "
						. "t1.location, t1.country_id, t1.contact, t1.comments, t1.email, "
						. "t1.url, t1.modified_from, t1.cancelled, t1.approved, t2.user_id, "
						. "t2.rights_modify, t2.rights_approve, t2.rights_maintain "
						. "from convention as t1, rights as t2 where t1.id = t2.convention_id "
						. "and approved = false and modified_from is not null "
						. "and user_id = " . $_SESSION['user_id'] . " and rights_approve = true", 
						$db_connection );
			}

			if ( ( mysql_num_rows( $add_result ) > 0 ) || ( mysql_num_rows( $mod_result ) > 0 ) )
			{
				echo( "<p><h2>Conventions requiring approval</h2></p>" );

				echo( "<table>" );

				if ( mysql_num_rows( $add_result ) > 0 )
				{
					$row = mysql_fetch_array( $add_result );

					while ( $row )
					{
						echo( "<tr><td>" );

						link_to_page_with_params( "approve_convention.php", "con_id=" . $row[ "id" ],
								$row[ "name" ] );

						echo( "</td></tr>" );

						$row = mysql_fetch_array( $add_result );
					}
				}

				if ( mysql_num_rows( $mod_result ) > 0 )
				{
					$row = mysql_fetch_array( $mod_result );

					while ( $row )
					{
						echo( "<tr><td>" );

						link_to_page_with_params( "approve_convention.php", "con_id=" . $row[ "id" ],
								$row[ "name" ] );

						echo( "</td></tr>" );

						$row = mysql_fetch_array( $mod_result );
					}
				}

				echo( "</table>" );
			}

			mysql_free_result( $add_result );
			
			mysql_free_result( $mod_result );

			echo( "<p><h2>Users</h2></p>" );

			echo( "<p>" );

			link_to_page( "modify_self.php", "Modify own account" );

			echo( "</p>" );

			if ( check_rights( "rights_maintain", 0, $db_connection ) )
			{
				echo( "<p>" );

				link_to_page( "modify_others.php", "Modify other user's account" );

				echo( "</p>" );
			}

			echo( '<p><a href="index.php">Logout</a></p>' );

			mysql_close( $db_connection );
		?>
	</body>
</html>
