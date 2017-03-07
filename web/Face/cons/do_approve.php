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
			// Approving a modification

			query_sql( "update convention set approved = true, modified_from = null " 
					. "where id = " . $_GET[ 'con_id' ], $db_connection );

			query_sql( "update rights set convention_id = " . $_GET[ 'con_id' ]
					. " where convention_id = " . $modified_from, $db_connection );

			query_sql( "update log set convention_id = " . $_GET[ 'con_id' ]
					. " where convention_id = " . $modified_from, $db_connection );

			query_sql( "delete from convention where id = " . $modified_from, $db_connection );
		}
		else
		{
			// Approving an addition

			query_sql("update convention set approved = true where id = " . $_GET[ 'con_id' ], 
					$db_connection );
		}

		query_sql( "insert into log values ( " . $_SESSION[ 'user_id' ] . ", " . $_GET[ 'con_id' ]
				. ", now(), 'Approved', '' )", $db_connection );

		goto_page( "maintain.php" );
	}
	else
	{
		echo("Convention not found to approve");

		link_to_page( "maintain.php", "Return to maintenance page" );
	}
?>
