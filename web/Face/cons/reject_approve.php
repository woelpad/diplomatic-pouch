<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "rights_approve", $_GET[ 'con_id' ], $db_connection );

	$result = query_sql( "select * from convention where id = " . $_GET[ 'con_id' ], 
			$db_connection );

	$row = mysql_fetch_array( $result );

	if ( $row )
	{
		$modified_from = $row[ 'modified_from' ];

		mysql_free_result( $result );

		if ( $modified_from > 0 )
		{
			// Rejecting a modification

			query_sql( "delete from rights where convention_id = " 
					. $_GET[ 'con_id' ], $db_connection );

			query_sql( "update log set convention_id = " . $modified_from
					. " where convention_id = " . $_GET[ 'con_id' ], $db_connection );

			query_sql("delete from convention where id = " 
					. $_GET[ 'con_id' ], $db_connection );

			query_sql( "insert into log values ( " . $_SESSION[ 'user_id' ] . ", " 
					. $modified_from . ", now(), 'Rejected', '' )", $db_connection );
		}
		else
		{
			// Rejecting an addition

			query_sql( "delete from rights where convention_id = " 
					. $_GET[ 'con_id' ], $db_connection );

			query_sql( "delete from log where convention_id = " 
					. $_GET[ 'con_id' ], $db_connection );

			query_sql("delete from convention where id = " 
					. $_GET[ 'con_id' ], $db_connection );
		}

		goto_page( "maintain.php" );
	}
	else
	{
		echo("Convention not found to reject");

		link_to_page( "maintain.php", "Return to maintenance page" );
	}
?>
